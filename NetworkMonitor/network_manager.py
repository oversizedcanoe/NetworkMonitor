import socket

GOOGLE_IP = '8.8.8.8'


def get_ip_address() -> str:
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect((GOOGLE_IP, 1))
    local_ip_address = s.getsockname()[0]
    s.close()
    return local_ip_address
