#!/usr/bin/python
import gpiod
import time
import os
import subprocess
import logging

# Path to the log file
log_file_path = '/var/log/power_cut.log'

# Clear the log file
with open(log_file_path, 'w'):
    pass

# Setup logging
logging.basicConfig(filename=log_file_path, level=logging.INFO, format='%(asctime)s %(message)s')

# Define the GPIO pin
gpio_chip = "/dev/gpiochip0"
gpio_line_offset = 17

# Specify the user
user = "user"

# Path to dbus-send
dbus_send_path = "/usr/bin/dbus-send"  # Adjust this path if needed

# Command templates
turn_off_screen_cmd = f". /tmp/user_environment ; sudo -E -u {user} {dbus_send_path} --session --type=method_call --dest=org.kde.kglobalaccel /component/org_kde_powerdevil org.kde.kglobalaccel.Component.invokeShortcut string:'Turn Off Screen'"
turn_on_screen_cmd = f". /tmp/user_environment ; sudo -E -u {user} {dbus_send_path} --session --type=method_call --dest=local.org_kde_powerdevil /org/kde/Solid/PowerManagement org.kde.Solid.PowerManagement.wakeup"

# Callback function for power cut event
def power_cut_callback():
    logging.info("Power cut detected. Turning off screen and waiting for 9 minutes before shutdown...")
    try:
        # Turn off the screen
        subprocess.run(turn_off_screen_cmd, shell=True, check=True)
    except subprocess.CalledProcessError as e:
        logging.error(f"Failed to turn off the screen: {e}")

    for _ in range(540):  # 9 minutes (540 * 1 second)
        time.sleep(1)  # Sleep for 1 second
        if line.get_value() == 1:
            logging.info("Power restored during waiting period. Canceling shutdown.")
            return

    logging.info("Power still cut. Initiating shutdown.")
    try:
        subprocess.run(["sudo", "halt"], check=True)
    except subprocess.CalledProcessError as e:
        logging.error(f"Failed to halt the system: {e}")

# Callback function for power restore event
def power_restore_callback():
    logging.info("Power restored. Turning on screen...")
    try:
        # Wake up the screen
        subprocess.run(turn_on_screen_cmd, shell=True, check=True)
    except subprocess.CalledProcessError as e:
        logging.error(f"Failed to turn on the screen: {e}")

try:
    with gpiod.Chip(gpio_chip) as chip:
        line = chip.get_line(gpio_line_offset)
        line.request(consumer="power_cut", type=gpiod.LINE_REQ_EV_BOTH_EDGES)
        
        # Initialize previous state
        prev_state = line.get_value()
        logging.info(f"Initial GPIO state: {prev_state}")
        
        logging.info("Waiting for power cut or restore...")
        while True:
            time.sleep(0.1)  # Sleep for a short time to avoid busy loop
            current_state = line.get_value()
            if current_state != prev_state:  # Check if state has changed
                logging.info(f"GPIO state changed: {current_state}")
                if current_state == 0:
                    power_cut_callback()
                else:
                    power_restore_callback()
                prev_state = current_state  # Update previous state

except KeyboardInterrupt:
    logging.info("Script terminated by user.")
except Exception as e:
    logging.error(f"An error occurred: {e}")

