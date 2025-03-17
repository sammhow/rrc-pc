#!/usr/bin/python3.12
from pynmeagps import NMEAReader
import socket
import time
import subprocess

#SOCKET = 'gnss-share.sock'
SOCKET = '/var/run/gnss-share.sock'

def get_timedate():
    while True:
        try:
        #with open('/home/howard/mystuff/Python/gps-output.txt', 'rb') as stream:
            with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as stream:
                stream.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                stream.connect(SOCKET)
                nmr = NMEAReader(stream, nmeaonly=True)
                print(nmr)
                for _, parsed_data in nmr:
                    if hasattr(parsed_data, 'date'):
                        timedate = f"{parsed_data.date} {parsed_data.time}"
                        yield timedate
                stream.disconnect()
        except FileNotFoundError:
            time.sleep(1)
        except KeyboardInterrupt:
            print("Stopped by user.")
            break

def set_system_time(timestamp):
    try:
        subprocess.run(["date", "-s", timestamp], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error setting system time: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")

timestamp_generator = get_timedate()  # Initialize generator
timestamp = next(timestamp_generator)  # Get the first timestamp
#set_system_time(timestamp)  # Pass the correct value
print(timestamp)
