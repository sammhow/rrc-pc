#!/usr/bin/python
import time
import subprocess
from datetime import datetime, timezone
from astral import LocationInfo
from astral.sun import sun
import pytz  # Ensure you have this installed (pip install pytz)

# Set your location (replace with your city or lat/lon)
CITY_NAME = "Bodmin"
REGION = "Cornwall"
LATITUDE = 50.557838
LONGITUDE = -4.689610
TIMEZONE = "Europe/London"

# Define brightness levels
NIGHT_BRIGHTNESS = 1
DAY_BRIGHTNESS = 10

# How often to adjust brightness (seconds)
INTERVAL = 60

# Get the local timezone object
local_tz = pytz.timezone(TIMEZONE)

def get_sun_times():
    """Get sunrise and sunset times for the location in local timezone."""
    location = LocationInfo(CITY_NAME, REGION, TIMEZONE, LATITUDE, LONGITUDE)
    s = sun(location.observer, date=datetime.now(timezone.utc))

    # Convert sunrise and sunset times to local timezone
    sunrise_local = s["sunrise"].astimezone(local_tz)
    sunset_local = s["sunset"].astimezone(local_tz)

    return sunrise_local, sunset_local

def calculate_brightness():
    """Determine whether it should be bright or dim."""
    sunrise, sunset = get_sun_times()
    
    # Get current time in local timezone
    now = datetime.now(local_tz)

    return DAY_BRIGHTNESS if sunrise <= now <= sunset else NIGHT_BRIGHTNESS

def set_brightness(level):
    """Set the backlight brightness using the command-line tool."""
    cmd = f"/usr/local/bin/Raspi_USB_Backlight_nogui -b {level}"
    subprocess.run(cmd, shell=True)

def main():
    """Main loop to continuously adjust brightness."""
    while True:
        brightness = calculate_brightness()
        set_brightness(brightness)
        print(f"Set brightness to {brightness} at {datetime.now(local_tz).strftime('%H:%M:%S')}")
        time.sleep(INTERVAL)

if __name__ == "__main__":
    main()

