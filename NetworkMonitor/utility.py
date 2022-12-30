# removes the last octet of a given IP Address so we are left with '192.168.X'
def get_base_ip_address(ip_address:str) -> str:
    reversed_ip_address = ip_address[::-1]
    first_period_index = reversed_ip_address.index(".")
    last_period_index = (len(ip_address) - first_period_index - 1)
    ip_address_base = ip_address[0:last_period_index]
    return ip_address_base