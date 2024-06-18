#!/usr/bin/python
import gpiod
import time
import os

# Define the GPIO pin
gpio_chip = "/dev/gpiochip0"
gpio_line_offset = 17

# Setup GPIO
chip = gpiod.Chip(gpio_chip)
line = chip.get_line(gpio_line_offset)
line.request(consumer="power_cut", type=gpiod.LINE_REQ_EV_FALLING_EDGE)

# Callback function for power cut event
def power_cut_callback():
    print("Power cut detected. Waiting for 9 minutes before shutdown...")
    time.sleep(540)  # 9 minutes
    if line.get_value() == 0:
        print("Power still cut. Initiating shutdown.")
        os.system("sudo halt")
    else:
        print("Power restored. Shutdown canceled.")

try:
    print("Waiting for power cut...")
    while True:
        event = line.event_wait(1)  # Wait for 0.1 seconds for an event
        if event is None:
            continue
        power_cut_callback()

except KeyboardInterrupt:
    print("\nScript terminated by user.")
    chip.close()

finally:
    chip.close()

