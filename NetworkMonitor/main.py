import logger
import network_manager
import time
import settings
from datetime import datetime
from models import ConnectedDevice
from typing import List

def start_monitor():
    logger.log('Monitoring network...')
    
    previous_connected_devices: List[ConnectedDevice] = []
    
    while True:    
        connected_devices: List[ConnectedDevice] = network_manager.get_connected_devices()
        logger.log('Found ' + str(len(connected_devices)) + ' devices')
        
        newly_connected_devices: List[ConnectedDevice] = get_new_devices(previous_connected_devices, connected_devices)
        
        if len(newly_connected_devices) > 0:
            logger.log(str(len(newly_connected_devices)) + ' new device(s) connected')
            
            # Set this scans result to "previous" result since there are new/changed entries
            previous_connected_devices = connected_devices
            
            for new_dev in newly_connected_devices:
                print(str(new_dev) + ' is now connected')
        else:
            logger.log('No new devices connected.')
                       
        # Sleep for required time, repeat ad infinitum.
        time.sleep(settings.SLEEP_TIME)

def get_new_devices(previous: List[ConnectedDevice], current: List[ConnectedDevice]) -> List[ConnectedDevice]:
    result: List[ConnectedDevice] = []
    
    for current_device in current:
        current_device_is_new: bool = True
        # if any previous device has current device's mac address, it's not new.
        # since IPs can change and device names can be unknown, mac address is the only reliable 'ID'
        for previous_device in previous:
            if previous_device.mac_address == current_device.mac_address:
                current_device_is_new = False
                break

        if current_device_is_new:
            result.append(current_device)
            
    return result
start_monitor()