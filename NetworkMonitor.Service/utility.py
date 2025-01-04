import re
from datetime import datetime, timedelta
from typing import List

# removes the last octet of a given IP Address so we are left with '192.168.X'
def parse_base_ip_address(ip_address:str) -> str:
    reversed_ip_address = ip_address[::-1]
    first_period_index = reversed_ip_address.index(".")
    last_period_index = (len(ip_address) - first_period_index - 1)
    ip_address_base = ip_address[0:last_period_index]
    return ip_address_base


# * Format is one of:
#  'Nmap scan report for IP_ADDRESS_HERE'
#  'Nmap scan report for DeviceName (IP_ADDRESS_HERE)'
#  'Nmap scan report for MAC_ADDRESS_HERE (IP_ADDRESS_HERE)'
def get_device_name_and_ip_address(nmapLine: str) -> List[str]:
    result: List[str] = ['','']
    # Get everything after the 'for '
    relevant_text: str = nmapLine[nmapLine.index("for") + 4:]
    
    ip_address_regex = "^((?:(?:[0-9]{1,3})\.{1}){3}(?:[0-9]{1,3}){1})$"
    device_name_regex = "^(.*)(?:\s)(?:\()((?:(?:[0-9]{1,3})\.{1}){3}(?:[0-9]{1,3}){1})(?:\))$"
    mac_address_regex = "^((?:[0-9A-Fa-f]{2}[:-]){5}(?:[0-9A-Fa-f]{2}))(?:\s)(?:\()((?:(?:[0-9]{1,3})\.{1}){3}(?:[0-9]{1,3}){1})(?:\))$"
    
    # Use regex and attempt to match from most specific to least specific. This is because the device_name_regex
    # will return a match for the MAC Address since it just looks for any character string.
    mac_address_search = re.search(mac_address_regex, relevant_text)
    if mac_address_search is not None:
        # group 0 is the whole match, 1 is MAC Address, 2 is IP Address
        result[1] = mac_address_search.group(2)
        return result
    
    device_name_search = re.search(device_name_regex, relevant_text)
    if device_name_search is not None:
        # 0 is the whole match, 1 is device name, 2 is IP Address
        result[0] = device_name_search.group(1)
        result[1] = device_name_search.group(2)
        return result
    
    ip_address_search = re.search(ip_address_regex, relevant_text)
    if ip_address_search is not None:
        # 0 is the whole match, 1 is IP Address
        result[1] = ip_address_search.group(1)
        return result
    
#   Format is:
#  'MAC Address: MAC_ADDRESS_HERE (DeviceVendor)'
# Device_Vendor may be the string 'Unknown'.
def get_mac_address_and_vendor(line: str) -> List[str]:
    result: List[str] = ['', '']
    
    #remove 'MAC Address: '
    relevant_text = line[13:]
    
    #MAC Address always 17 characters
    result[0] = relevant_text[0:17]
    
    #Vendor name will be 2 chars after MAC Address, until 2nd last char   
    result[1] = relevant_text[19:-1]
    
    return result

def ticks_to_date(ticks: int) -> datetime:
    return datetime(1, 1, 1) + timedelta(microseconds=ticks/10)


def date_to_ticks(date: datetime) -> int:
    start_of_ticks: datetime = datetime(1, 1, 1)
    return  (date - start_of_ticks).total_seconds() * 10000000
    