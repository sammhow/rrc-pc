#!/usr/bin/python
import time
import subprocess
from datetime import datetime, timedelta, timezone
from astral import LocationInfo
from astral.sun import sun

# Set your location (replace with your city or lat/lon)
CITY_NAME = "Bodmin"
REGION = "Cornwall"
LATITUDE = -4.689610  # Replace with actual latitude
LONGITUDE = 50.557838  # Replace with actual longitude
TIMEZONE = "Europe/London"

# Define min and max brightness levels
MIN_BRIGHTNESS = 1
MAX_BRIGHTNESS = 10

# How often to adjust brightness (seconds)
INTERVAL = 60

def get_sun_times():
    """Get sunrise and sunset times for the location."""
    location = LocationInfo(CITY_NAME, REGION, TIMEZONE, LATITUDE, LONGITUDE)
    s = sun(location.observer, date=datetime.now())

    return s["sunrise"], s["sunset"]

def calculate_brightness():
    """Calculate the brightness level based on the time of day."""
    sunrise, sunset = get_sun_times()
    
    now = datetime.now(timezone.utc).astimezone()
    if now < sunrise:  # Before sunrise, use minimum brightness, timezonestimezone(
        return MIN_BRIGHTNESS
    elif now > sunset:  # After sunset, use minimum brightness
        return MIN_BRIGHTNESS
    else:
        # Scale brightness gradually between sunrise and sunset
        elapsed = (now - sunrise).total_seconds()
        total_daylight = (sunset - sunrise).total_seconds()
        brightness = MIN_BRIGHTNESS + (MAX_BRIGHTNESS - MIN_BRIGHTNESS) * (elapsed / total_daylight)
        return round(brightness)

def set_brightness(level):
    """Set the backlight brightness using the command-line tool."""
    cmd = f"/usr/local/bin/Raspi_USB_Backlight_nogui -b {level}"
    subprocess.run(cmd, shell=True)

def main():
    """Main loop to continuously adjust brightness."""
    while True:
        brightness = calculate_brightness()
        set_brightness(brightness)
        print(f"Set brightness to {brightness}")
        time.sleep(INTERVAL)

if __name__ == "__main__":
    main()

