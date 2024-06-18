import RPi.GPIO as GPIO
import time
import os

# Define the GPIO pin
gpio_pin = 17

# Setup GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(gpio_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

# Callback function for power cut event
def power_cut_callback(channel):
    print("Power cut detected. Waiting for 9 minutes before shutdown...")
    time.sleep(10)  # 9 minutes
    if GPIO.input(gpio_pin) == GPIO.LOW:
        print("Power still cut. Initiating shutdown.")
        os.system("sudo shutdown now")
    else:
        print("Power restored. Shutdown canceled.")

# Add event detection
GPIO.add_event_detect(gpio_pin, GPIO.FALLING, callback=power_cut_callback, bouncetime=300)

try:
    print("Waiting for power cut...")
    while True:
        time.sleep(1)

except KeyboardInterrupt:
    print("\nScript terminated by user.")
    GPIO.cleanup()

finally:
    GPIO.cleanup()

