import logger
import settings
import socket
import subprocess
import utility
from credentials import SAMPLE_NMAP_OUTPUT
from models import ConnectedDevice
from typing import List
from uuid import getnode

def get_ip_address() -> str:
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect((settings.IP_FOR_SOCKET, 1))
    local_ip_address = s.getsockname()[0]
    s.close()
    return local_ip_address

def get_connected_devices() -> List[ConnectedDevice]:
    ip_address: str = get_ip_address()
    ip_address_base: str = utility.parse_base_ip_address(ip_address)
    
    nmap_output_lines: List[str] = run_nmap(ip_address_base)

    connected_devices: List[ConnectedDevice] = get_devices_from_nmap(nmap_output_lines, ip_address)
    
    return connected_devices

# Returns the result of an nmap command where each line is split into it's own string. The nmap command
# is for the provided base_ip_address which should be the first three octets of this devices IP Address.
def run_nmap(base_ip_address: str) -> List[str]:    
    # Commenting this out as it takes a bit to run -- hardcoding a sample result for now
    logger.log('Querying network...')
    completed_process = subprocess.run(['sudo', 'nmap', '-sn', base_ip_address + '.0/24'], stdout=subprocess.PIPE, text=True)
    logger.log('Query complete.')
    completed_process_output = completed_process.stdout

    #completed_process_output = SAMPLE_NMAP_OUTPUT

    nmap_output_lines: List[str] = completed_process_output.split('\n')
    
    return nmap_output_lines


def get_devices_from_nmap(nmap_output_lines: List[str], this_ip_address: str) -> List[ConnectedDevice]:
    # There are 5 different lines which get printed.
    # 1. Starting line: Starting Nmap 7.70 ( https://nmap.org ) at 2022-12-30 12:47 EST
    # 2. For each device: 'Nmap scan report for ...'
    # 3. For each device: 'Host is up (0.010s latency).'
    # *4. For each device: 'MAC Address'
    # 5. Final line: Nmap done: 256 IP addresses (16 hosts up) scanned in 24.14 seconds 
    # * This line is not present for the device doing the scanning.
    
    connected_devices: List[ConnectedDevice] = []
    connected_device: ConnectedDevice = ConnectedDevice()   
    
    # Skip lines which are the 1st, 3rd, or 5th type. 
    lines_to_ignore: List[str] = ['Starting Nmap', 'Host is up', 'Nmap done']

    for line in nmap_output_lines:
        if any(text_to_ignore in line for text_to_ignore in lines_to_ignore):
            continue
        
        if "Nmap scan report" in line:
            device_name_and_ip_address = utility.get_device_name_and_ip_address(line)
            connected_device.device_name = device_name_and_ip_address[0]
            connected_device.ip_address = device_name_and_ip_address[1]
            # If this is the device we are running this on, there won't be a "Mac Address" line.
            # Set the MAC Address and manufacturer name separately.
            if this_ip_address in line:
                connected_device.mac_address = get_this_mac_address()
                connected_device.device_name = settings.THIS_DEVICE_NAME
                connected_device.manufacturer_name = settings.THIS_MANUFACTURER_NAME
                connected_devices.append(connected_device)
                connected_device = ConnectedDevice()
        if "MAC Address" in line:
            mac_address_and_manufacturer = utility.get_mac_address_and_manufacturer(line)
            connected_device.mac_address = mac_address_and_manufacturer[0]
            connected_device.manufacturer_name = mac_address_and_manufacturer[1]
            connected_devices.append(connected_device)
            connected_device = ConnectedDevice()

    return connected_devices

def get_this_mac_address() -> str:
    mac_as_int = getnode()
    mac_as_hex = hex(mac_as_int)
    # value will be '0x' followed by 12 hex characters
    mac_address = mac_as_hex[2:]
    mac_address_formatted = ''
    for i in range(len(mac_address)):
        mac_address_formatted += mac_address[i]
        # every second character except the last, add a ':'
        if (i + 1) % 2 == 0 and i != len(mac_address) - 1:
            mac_address_formatted += ':'
    
    return mac_address_formatted