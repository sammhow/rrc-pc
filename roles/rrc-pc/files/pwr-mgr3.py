#!/usr/bin/python
import RPi.GPIO as GPIO
import time
import os
import subprocess
import logging
import signal

# Path to the log file
log_file_path = '/var/log/power_cut.log'

# Clear the log file
with open(log_file_path, 'w'):
    pass

# Setup logging
logging.basicConfig(filename=log_file_path, level=logging.INFO, format='%(asctime)s %(message)s')

# Define the GPIO pin
gpio_pin = 22

# Specify the user
user = "user"

# Path to dbus-send
dbus_send_path = "/usr/bin/dbus-send"  # Adjust this path if needed

# Command templates
turn_off_screen_cmd = f". /tmp/user_environment ; sudo -E -u {user} {dbus_send_path} --session --type=method_call --dest=org.kde.kglobalaccel /component/org_kde_powerdevil org.kde.kglobalaccel.Component.invokeShortcut string:'Turn Off Screen'"
turn_on_screen_cmd = f". /tmp/user_environment ; sudo -E -u {user} {dbus_send_path} --session --type=method_call --dest=local.org_kde_powerdevil /org/kde/Solid/PowerManagement org.kde.Solid.PowerManagement.wakeup"

def cleanup_and_exit(signum, frame):
    print("Received signal:", signum)
    GPIO.cleanup()
    print("GPIO cleaned up, exiting.")
    sys.exit(0)

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
        if GPIO.input(gpio_pin) == 1:
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
        # Unlock the session
        subprocess.run("loginctl unlock-session c1", shell=True, check=True)

    except subprocess.CalledProcessError as e:
        logging.error(f"Failed to turn on the screen: {e}")

# Setup GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(gpio_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Register signal handlers for SIGTERM and SIGINT
signal.signal(signal.SIGTERM, cleanup_and_exit)
signal.signal(signal.SIGINT, cleanup_and_exit)

# Initialize previous state
prev_state = GPIO.input(gpio_pin)
logging.info(f"Initial GPIO state: {prev_state}")

logging.info("Waiting for power cut or restore...")

try:
    while True:
        # Read the state of the pin
        current_state = GPIO.input(gpio_pin)
        if current_state != prev_state:
            logging.info(f"GPIO state changed: {current_state}")
            if current_state == 0:
                power_cut_callback()
            else:
                power_restore_callback()
            prev_state = current_state  # Update previous state
        # Wait for a short period before checking again
        time.sleep(1)

except KeyboardInterrupt:
    cleanup_and_exit(signal.SIGINT, None)
except Exception as e:
    logging.error(f"An error occurred: {e}")

finally:
    GPIO.cleanup()
    logging.info("GPIO cleaned up and script terminated.")

