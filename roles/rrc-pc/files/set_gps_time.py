#!/usr/bin/python
import re
import socket
import time
from datetime import datetime

# Path to the GNSS-share socket
SOCKET_PATH = '/var/run/gnss-share.sock'

# Regex to extract time and date from NMEA sentences
gprmc_pattern = re.compile(r'^\$GPRMC,(\d{6}\.\d+),.*?,(\d{6}),', re.MULTILINE)

def convert_to_datetime(nmea_time, nmea_date):
    """Convert NMEA time and date to 'YYYY-MM-DD HH:MM:SS' format."""
    time_str = f"{nmea_time[:2]}:{nmea_time[2:4]}:{nmea_time[4:6]}"
    date_str = f"20{nmea_date[4:]}-{nmea_date[2:4]}-{nmea_date[:2]}"
    return f"{date_str} {time_str}"

def set_system_time(datetime_str):
    """Set system time using the extracted GPS time (Currently just prints)."""
    try:
        # subprocess.run(["date", "-s", datetime_str], check=True)  # Uncomment to actually set the time
        print(f"System time successfully set to {datetime_str}")
    except Exception as e:
        print(f"Failed to set system time: {e}")

def read_nmea_and_set_time(socket_path):
    """Continuously read NMEA data from the GNSS-share socket and update system time."""
    while True:
        try:
            with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as s:
                print(f"Connecting to {socket_path}...")
                s.connect(socket_path)
                print(f"Connected to {socket_path}")

                while True:
                    data = s.recv(4096).decode('ascii')
                    if not data:
                        print("No data received. Reconnecting...")
                        break  # Exit inner loop to reconnect

                    gprmc_matches = gprmc_pattern.findall(data)
                    if not gprmc_matches:
                        print("No valid GPRMC sentence found.")

                    for time_val, date_val in gprmc_matches:
                        datetime_str = convert_to_datetime(time_val, date_val)
                        print(f"Extracted Date-Time: {datetime_str}")
                        set_system_time(datetime_str)
                        print("Time set successfully.")
                    
                    time.sleep(64)  # Prevent excessive looping
            
        except FileNotFoundError:
            print(f"Socket not found: {socket_path}. Retrying in 5 seconds...")
        except ConnectionError as e:
            print(f"Connection error: {e}. Retrying in 5 seconds...")
        except Exception as e:
            print(f"Unexpected error: {e}. Retrying in 5 seconds...")

        time.sleep(5)  # Delay before reconnecting

# Start the process
read_nmea_and_set_time(SOCKET_PATH)

