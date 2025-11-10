#!/usr/bin/python
import os
import time
import subprocess
from datetime import datetime, timezone
from astral import LocationInfo
from astral.sun import sun
import pytz  # pip install pytz

# Set your location
CITY_NAME = "Bodmin"
REGION = "Cornwall"
LATITUDE = 50.557838
LONGITUDE = -4.689610
TIMEZONE = "Europe/London"

# Brightness levels
NIGHT_BRIGHTNESS = 1
DAY_BRIGHTNESS = 10

# Check interval (seconds)
INTERVAL = 60

# Path to store last brightness
STATE_FILE = "/var/run/dimmer/brightness"

local_tz = pytz.timezone(TIMEZONE)


def get_sun_times():
    """Get local sunrise and sunset times."""
    location = LocationInfo(CITY_NAME, REGION, TIMEZONE, LATITUDE, LONGITUDE)
    s = sun(location.observer, date=datetime.now(timezone.utc))
    return (
        s["sunrise"].astimezone(local_tz),
        s["sunset"].astimezone(local_tz)
    )


def calculate_brightness():
    """Return target brightness based on current time."""
    sunrise, sunset = get_sun_times()
    now = datetime.now(local_tz)
    return DAY_BRIGHTNESS if sunrise <= now <= sunset else NIGHT_BRIGHTNESS


def get_last_brightness():
    """Read last brightness from file if available."""
    if os.path.exists(STATE_FILE):
        try:
            with open(STATE_FILE, "r") as f:
                return int(f.read().strip())
        except Exception:
            return None
    return None


def set_brightness(level):
    """Set the brightness via command line."""
    cmd = f"/usr/local/bin/Raspi_USB_Backlight_nogui -b {level}"
    subprocess.run(cmd, shell=True, check=False)


def save_brightness(level):
    """Save current brightness to file."""
    os.makedirs(os.path.dirname(STATE_FILE), exist_ok=True)
    with open(STATE_FILE, "w") as f:
        f.write(str(level))


def main():
    while True:
        new_brightness = calculate_brightness()
        last_brightness = get_last_brightness()

        # Only set if it's new or not previously set
        if last_brightness != new_brightness:
            set_brightness(new_brightness)
            save_brightness(new_brightness)
            # print(f"Brightness set to {new_brightness} at {datetime.now(local_tz)}")

        time.sleep(INTERVAL)


if __name__ == "__main__":
    main()
