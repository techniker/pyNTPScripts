# Simple script that gathers information from a NTP server and graphs its offset using matplotlib
# Bjoern Heller <tec(att)sixtopia.net>

import ntplib
import matplotlib.pyplot as plt
from time import ctime, sleep
from collections import deque

def query_ntp_server(server):
    try:
        client = ntplib.NTPClient()
        response = client.request(server)
        return response
    except Exception as e:
        print("Error:", e)
        return None

def get_server_type(ref_id):
    # Here, you can add checks to identify specific server types based on ref_id values.
    # For example, if the ref_id starts with "PZF", you can classify it as a PZF type server.
    # Add more conditions as per your knowledge about the ref_id patterns for different server types.
    if ref_id.startswith(b"PZF"):
        return "PZF"
    elif ref_id.startswith(b"GPS"):
        return "GPS"
    # Add more conditions for other types if you have specific patterns to check.
    else:
        return "Unknown"

def display_ntp_info(response):
    if response is None:
        print("Failed to retrieve NTP information.")
        return

    print("NTP Server:", response.host)
    print("Leap:", response.leap)
    print("Version:", response.version)
    print("Mode:", response.mode)
    print("Stratum:", response.stratum)
    print("Delay (ms):", response.delay)
    print("Offset (ms):", response.offset)
    print("Reference Time:", ctime(response.ref_time))
    print("Originate Time:", ctime(response.orig_time))
    print("Receive Time:", ctime(response.recv_time))
    print("Transmit Time:", ctime(response.tx_time))

    server_type = get_server_type(response.ref_id)
    print("Server Type:", server_type)

def update_plot(offset_values):
    plt.clf()
    plt.plot(offset_values)
    plt.xlabel("Time (s)")
    plt.ylabel("Offset (ms)")
    plt.title("NTP Server Offset")
    plt.pause(0.01)

def main():
    ntp_server = "ntp01.sixtopia.net"  # Change this to the NTP server you want to query

    offset_values = deque(maxlen=100)  # Keep the last 100 offset values
    plt.ion()  # Turn on interactive mode for real-time plotting

    while True:
        response = query_ntp_server(ntp_server)
        if response:
            offset_ms = response.offset * 1000  # Convert offset to milliseconds
            offset_values.append(offset_ms)
            print(f"Offset (ms): {offset_ms:.2f}")

        update_plot(offset_values)
        sleep(0.5)  # Update the plot every 500 millisecond

if __name__ == "__main__":
    main()
