#!/usr/bin/python
import re
import socket
import subprocess
from datetime import datetime

# Path to the GNSS-share socket
SOCKET_PATH = '/var/run/gnss-share.sock'

# Regex to extract time and date from NMEA sentences
gprmc_pattern = re.compile(r'^\$GPRMC,(\d{6}\.\d+),.*?,(\d{6}),', re.MULTILINE)  # Extract time and date from GPRMC

# Function to convert NMEA time and date to "YYYY-MM-DD HH:MM:SS" format
def convert_to_datetime(nmea_time, nmea_date):
    # Parse NMEA time (HHMMSS.sss) and date (DDMMYY)
    time_str = f"{nmea_time[:2]}:{nmea_time[2:4]}:{nmea_time[4:6]}"
    date_str = f"20{nmea_date[4:]}-{nmea_date[2:4]}-{nmea_date[:2]}"
    return f"{date_str} {time_str}"

# Function to set system time using chronyc
def set_system_time(datetime_str):
    try:
        # Call 'chronyc' to set the time
        subprocess.run(["date", "-s", datetime_str], check=True)
        print(f"System time successfully set to {datetime_str}")
    except subprocess.CalledProcessError as e:
        print(f"Failed to set system time: {e}")

# Function to read NMEA data from the socket
def read_nmea_and_set_time(socket_path):
    try:
        with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as s:
            s.connect(socket_path)
            while True:
                data = s.recv(4096).decode('ascii')  # Read data from the socket
                if not data:
                    break

                # Search for GPRMC sentences to extract date and time
                gprmc_matches = gprmc_pattern.findall(data)

                for time, date in gprmc_matches:
                    # Convert NMEA time and date to the required format
                    datetime_str = convert_to_datetime(time, date)
                    print(f"Extracted Date-Time: {datetime_str}")

                    # Set system time
                    set_system_time(datetime_str)

    except FileNotFoundError:
        print(f"Socket not found: {socket_path}")
    except ConnectionError as e:
        print(f"Connection error: {e}")
    except KeyboardInterrupt:
        print("Stopped by user.")

# Main entry point
if __name__ == "__main__":
    print(f"Reading NMEA data from socket: {SOCKET_PATH}")
    read_nmea_and_set_time(SOCKET_PATH)

