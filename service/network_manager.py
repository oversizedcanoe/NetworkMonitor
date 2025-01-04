import settings
import socket
import service.parser as parser
from shared.models import ConnectedDevice
from typing import List
from uuid import getnode
import nmap_manager as nmap

def get_ip_address() -> str:
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect((settings.IP_FOR_SOCKET, 1))
    local_ip_address = s.getsockname()[0]
    s.close()
    return local_ip_address

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

def get_connected_devices() -> List[ConnectedDevice]:
    ip_address: str = get_ip_address()
    ip_address_base: str = parser.parse_base_ip_address(ip_address)
    
    nmap_output_lines: List[str] = nmap.run_nmap(ip_address_base)
    connected_devices: List[ConnectedDevice] = nmap.get_devices_from_nmap(nmap_output_lines, ip_address)
    
    return connected_devices