import network_manager
import subprocess
from typing import List
from utility import *
from models import *
from credentials import *

ip_address: str = network_manager.get_ip_address()
ip_address_base: str = get_base_ip_address(ip_address)

# Commenting this out as it takes a bit to run -- hardcoding a sample result for now
#completed_process = subprocess.run(['sudo', 'nmap', '-sn', ip_address_base + '.0/24'], stdout=subprocess.PIPE, text=True)
#completed_process_output = completed_process.stdout

completed_process_output = SAMPLE_NMAP_OUTPUT

nmap_output_lines: List[str] = completed_process_output.split('\n')

# There are 5 different lines which get printed.
# 1. Starting line: Starting Nmap 7.70 ( https://nmap.org ) at 2022-12-30 12:47 EST
# 2. For each device: 'Nmap scan report for ...'
# 3. For each device: 'Host is up (0.010s latency).'
# *4. For each device: 'MAC Address'
# 5. Final line: Nmap done: 256 IP addresses (16 hosts up) scanned in 24.14 seconds 
# * This line is not present for the device doing the scanning.

connected_devices: List[ConnectedDevice] = []
connected_device: ConnectedDevice = ConnectedDevice()

for line in nmap_output_lines:
    # Skip lines which are the 1st, 3rd, or 5th type. 
    if "Starting Nmap" in line or "Host is up" in line or "Nmap done" in line:
        continue
    
    if "Nmap scan report" in line:
        device_name_and_ip_address = get_device_name_and_ip_address(line)
        connected_device.device_name = device_name_and_ip_address[0]
        connected_device.ip_address = device_name_and_ip_address[1]
        # If this is the device we are running this on, there won't be a "Mac Address" line.
        # Set the MAC Address and manufacturer name separately.
        if ip_address in line:
            connected_device.mac_address = 'THIS MAC ADDRESS'
            connected_device.manufacturer_name = 'Raspberry Pi'
            connected_devices.append(connected_device)
            connected_device = ConnectedDevice()
    if "MAC Address" in line:
        mac_address_and_manufacturer = get_mac_address_and_manufacturer(line)
        connected_device.mac_address = mac_address_and_manufacturer[0]
        connected_device.manufacturer_name = mac_address_and_manufacturer[1]
        connected_devices.append(connected_device)
        connected_device = ConnectedDevice()

for i in connected_devices:
    print(i)
