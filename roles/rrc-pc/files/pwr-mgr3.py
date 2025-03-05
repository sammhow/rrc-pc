#!/usr/bin/python3
# SPDX-License-Identifier: GPL-2.0-or-later
# SPDX-FileCopyrightText: 2023 Kent Gibson <warthog618@gmail.com>

import gpiod
from datetime import timedelta
from gpiod.line import Bias, Edge
import subprocess
import logging
import time
import threading

# Setup logging
log_file_path = "/var/log/power_cut.log"
# Clear the log file
with open(log_file_path, 'w'):
    pass
logging.basicConfig(filename=log_file_path, level=logging.INFO, format="%(asctime)s %(message)s")

# Define your user and dbus-send path
user = "user"
dbus_send_path = "/usr/bin/dbus-send"

# Define commands to turn the screen off and on
turn_off_screen_cmd = f". /tmp/user_environment ; sudo -E -u {user} {dbus_send_path} --session --type=method_call --dest=org.kde.kglobalaccel /component/org_kde_powerdevil org.kde.kglobalaccel.Component.invokeShortcut string:'Turn Off Screen'"
turn_on_screen_cmd = f". /tmp/user_environment ; sudo -E -u {user} {dbus_send_path} --session --type=method_call --dest=local.org_kde_powerdevil /org/kde/Solid/PowerManagement org.kde.Solid.PowerManagement.wakeup"

# Shutdown function
def shutdown_system():
    try:
        logging.info("Power still cut. Initiating shutdown.")
        subprocess.run(["sudo", "halt"], check=True)
    except subprocess.CalledProcessError as e:
        logging.error(f"Failed to halt the system: {e}")

# Function to handle the edge event types
def edge_type_str(event):
    """Return the edge type as a string."""
    if event.event_type is event.Type.RISING_EDGE:
        return "Rising"
    if event.event_type is event.Type.FALLING_EDGE:
        return "Falling"
    return "Unknown"


def watch_line_value(chip_path, line_offset, shutdown_delay=30):
    """Watch a specific GPIO pin for edge events and run commands based on the event."""
    # Assume a button connecting the pin to ground,
    # so pull it up and provide some debounce.
    with gpiod.request_lines(
        chip_path,
        consumer="watch-line-value",
        config={
            line_offset: gpiod.LineSettings(
                edge_detection=Edge.BOTH,  # Detect both rising and falling edges
                bias=Bias.PULL_UP,         # Enable pull-up resistor
                debounce_period=timedelta(milliseconds=10),  # Debounce
            )
        },
    ) as request:
        timer_thread = None  # Initialize the timer thread variable
        while True:
            # Blocks until at least one event is available
            for event in request.read_edge_events():
                edge_type = edge_type_str(event)
                logging.info(f"Edge detected: {edge_type} on GPIO pin {event.line_offset} event #{event.line_seqno}")
                
                # Falling edge: turn off the screen and start the shutdown timer
                if edge_type == "Falling":
                    logging.info("Executing Turn Off Screen command...")
                    try:
                        subprocess.run(turn_off_screen_cmd, shell=True, check=True)
                    except subprocess.CalledProcessError as e:
                        logging.error(f"Failed to execute Turn Off Screen command: {e}")
                    
                    # Start a timer to shut down the system after `shutdown_delay` seconds
                    if timer_thread is None or not timer_thread.is_alive():
                        timer_thread = threading.Timer(shutdown_delay, shutdown_system)
                        timer_thread.start()
                    else:
                        logging.info("Timer is already running.")
                
                # Rising edge: turn on the screen and cancel the shutdown timer if it exists
                elif edge_type == "Rising":
                    logging.info("Executing Turn On Screen command...")
                    try:
                        subprocess.run(turn_on_screen_cmd, shell=True, check=True)
                        subprocess.run("loginctl unlock-session c1", shell=True, check=True)
                        # Cancel the shutdown timer if the power is restored
                        if timer_thread and timer_thread.is_alive():
                            timer_thread.cancel()
                            logging.info("Shutdown timer cancelled due to power restoration.")
                    except subprocess.CalledProcessError as e:
                        logging.error(f"Failed to execute Turn On Screen command: {e}")


if __name__ == "__main__":
    try:
        # Monitor GPIO pin 26 on chip 0 (change to your pin if needed)
        watch_line_value("/dev/gpiochip0", 26, shutdown_delay=540)  # 9 minutes before shutdown
    except OSError as ex:
        print(ex, "\nCustomize the example configuration to suit your situation")

