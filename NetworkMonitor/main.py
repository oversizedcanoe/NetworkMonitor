import network_manager
import subprocess
from typing import List
from utility import *

ip_address: str = network_manager.get_ip_address()
ip_address_base: str = get_base_ip_address(ip_address)

output = subprocess.run(['sudo', 'nmap', '-sn', ip_address_base + '.0/24'], stdout=subprocess.PIPE, text=True)

nmap_output_lines: List[str] = output.stdout.split('\n')

devices_read: List[str] = []

#for line in nmap_output_lines:
    
    
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
