import socket
import re
from datetime import datetime

# Replace this with your GNSS-share socket path
SOCKET_PATH = '/path/to/gnss-share/socket'

# Regex to extract UTC time from NMEA sentences (e.g., GPRMC or GPGGA)
NMEA_REGEX = re.compile(r'^\$..RMC,\d{6}\.\d+,A,.*,\d{6}')

def get_time_from_nmea(nmea_sentence):
    parts = nmea_sentence.split(',')
    time_str = parts[1]  # HHMMSS format in $GPRMC or $GPGGA
    date_str = parts[9]  # DDMMYY format in $GPRMC (if available)
    
    # Convert NMEA time to UTC datetime
    time = datetime.strptime(time_str + date_str, "%H%M%S%d%m%y")
    return time

def read_gnss_socket():
    with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as s:
        s.connect(SOCKET_PATH)
        while True:
            data = s.recv(1024).decode('ascii')
            # Search for a valid NMEA sentence containing UTC time
            match = NMEA_REGEX.search(data)
            if match:
                nmea_sentence = match.group(0)
                return get_time_from_nmea(nmea_sentence)

if __name__ == "__main__":
    utc_time = read_gnss_socket()
    print("UTC Time from GNSS:", utc_time)

