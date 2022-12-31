import network_manager
from models import ConnectedDevice
from typing import List

def start_monitor():
    # Every X seconds...
    # Get IP Address
    # Execute nmap to see other devices on network
    # If devices have changed since last time, do something
    connected_devices: List[ConnectedDevice] = network_manager.get_connected_devices()    
    
    for i in connected_devices:
        print(i)
        
        
start_monitor()