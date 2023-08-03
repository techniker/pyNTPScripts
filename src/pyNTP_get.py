# Simple script that gathers information from a NTP server using ntplib
# Bjoern Heller <tec(att)sixtopia.net>

import ntplib
from time import ctime

def query_ntp_server(server):
    try:
        client = ntplib.NTPClient()
        response = client.request(server)
        return response
    except Exception as e:
        print("Error:", e)
        return None

def display_ntp_info(response):
    if response is None:
        print("Failed to retrieve NTP information.")
        return

    #print("NTP Server:", response.host)
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

def main():
    ntp_server = "ntp01.sixtopia.net"  # Change this to the NTP server you want to query
    response = query_ntp_server(ntp_server)
    display_ntp_info(response)

if __name__ == "__main__":
    main()
