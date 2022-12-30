import network_manager
import subprocess
from typing import List
from utility import *
from models import *

ip_address: str = network_manager.get_ip_address()
ip_address_base: str = get_base_ip_address(ip_address)

output = subprocess.run(['sudo', 'nmap', '-sn', ip_address_base + '.0/24'], stdout=subprocess.PIPE, text=True)

nmap_output_lines: List[str] = output.stdout.split('\n')

# There are 5 different lines which get printed.
# 1. Starting line: Starting Nmap 7.70 ( https://nmap.org ) at 2022-12-30 12:47 EST
# *2. For each device: 'Nmap scan report for ...'
# 3. For each device: 'Host is up (0.010s latency).'
# **4. For each device: 'MAC Address'
# 5. Final line: Nmap done: 256 IP addresses (16 hosts up) scanned in 24.14 seconds 

# * Format is one of:
#  '...for IP_ADDRESS_HERE'
#  '...for DeviceName (IP_ADDRESS_HERE)'
#  '...for MAC_ADDRESS_HERE (IP_ADDRESS_HERE)'

# ** This line is not present for the device doing the scanning.
#   Format is:
#  'MAC Address: MAC_ADDRESS_HERE (DeviceManufacturer)'
# Device_Manufacturer may be the string 'Unknown'.

connected_devices: List[ConnectedDevice] = []
connected_device: ConnectedDevice = ConnectedDevice()

for line in nmap_output_lines:
    # Skip lines which are the 1st, 3rd, or 5th type. 
    if "Starting Nmap" in line or "Host is up" in line or "Nmap done" in line:
        continue
    
    # TODO:
    if "Nmap scan report" in line:
        current_device_string = line
        # Set IP Address and Device Name (if device name present)
        if ip_address in line:
            print('test')
            # Set MAC Address and manufacturer to this device
            # Add device to list
            # Reset connected_device object            
    if "MAC Address" in line:
        print('test')
        # Set MAC Address
        # Add device to list
        # Reset connected_device object

