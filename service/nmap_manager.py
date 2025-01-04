
from logging import getLogger
import subprocess
from typing import List
from shared import helper
from service.network_manager import get_this_mac_address
import settings
from shared.models import ConnectedDevice
import parser

__logger = getLogger(__name__)

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
            device_name_and_ip_address = parser.parse_device_name_and_ip_address(line)
            connected_device.device_name = device_name_and_ip_address[0]
            connected_device.ip_address = device_name_and_ip_address[1]
            # If this is the device we are running this on, there won't be a "Mac Address" line.
            # Set the MAC Address and vendor separately.
            if this_ip_address in line:
                connected_device.mac_address = get_this_mac_address()
                connected_device.device_name = settings.THIS_DEVICE_NAME
                connected_device.vendor_name = settings.THIS_VENDOR_NAME
                connected_devices.append(connected_device)
                connected_device = ConnectedDevice()
        if "MAC Address" in line:
            mac_address_and_vendor = parser.parse_mac_address_and_vendor(line)
            connected_device.mac_address = mac_address_and_vendor[0]
            connected_device.vendor_name = mac_address_and_vendor[1]
            connected_devices.append(connected_device)
            connected_device = ConnectedDevice()

    return connected_devices

# Returns the result of an nmap command where each line is split into it's own string. The nmap command
# is for the provided base_ip_address which should be the first three octets of this devices IP Address.
def run_nmap(base_ip_address: str) -> List[str]:    
    __logger.debug('Querying network...')
    
    arg_array: List[str] = ['nmap', '-sn', base_ip_address + '.0/24']

    if helper.is_windows() == False:
        arg_array.insert(0, 'sudo')

    completed_process = subprocess.run(arg_array, stdout=subprocess.PIPE, text=True)
    __logger.debug('Query complete.')
    completed_process_output = completed_process.stdout

    #completed_process_output = SAMPLE_NMAP_OUTPUT

    nmap_output_lines: List[str] = completed_process_output.split('\n')
    
    return nmap_output_lines
