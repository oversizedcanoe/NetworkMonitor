from logging import getLogger
import logging
import data_access
import json
import network_manager
import time
import settings
from datetime import datetime
from models import ConnectedDevice
from typing import List
import traceback
import sys

__logger = getLogger(__name__)

def start_monitor():
    __logger.info('Monitoring network')
    __logger.debug('Debug stuff')
    
    previous_connected_devices: List[ConnectedDevice] = []

    while False:    
        connected_devices: List[ConnectedDevice] = network_manager.get_connected_devices()
        __logger.debug('Found %s devices.', str(len(connected_devices)))
        
        newly_connected_devices: List[ConnectedDevice] = get_new_devices(previous_connected_devices, connected_devices)
        
        if len(newly_connected_devices) > 0:
            __logger.debug('%s new device(s) connected.', str(len(newly_connected_devices))) 
            
            #for new_dev in newly_connected_devices:
            #    __logger.debug('%s is now connected.', str(new_dev))
                
            handle_new_devices(newly_connected_devices)            
        else:       
            __logger.debug('No new devices connected.')
                       
        # Set this scans result to previous result 
        previous_connected_devices = connected_devices
        
        # Sleep for required time, repeat ad infinitum.
        time.sleep(settings.SLEEP_TIME)

def get_new_devices(previous: List[ConnectedDevice], current: List[ConnectedDevice]) -> List[ConnectedDevice]:
    result: List[ConnectedDevice] = []

    for current_device in current:
        current_device_is_new: bool = True
        # if any previous device has current device's mac address, it's not new.
        # since IPs can change and device names can be unknown, mac address is the only reliable unique identifier.
        for previous_device in previous:
            if previous_device.mac_address == current_device.mac_address:
                current_device_is_new = False
                break

        if current_device_is_new:
            result.append(current_device)
            
    return result

def handle_new_devices(connected_devices: List[ConnectedDevice]) -> None:
    # We need a list of which devices to notify 
    # Brand new devices default to have notify_on_connect to True.
    # Exisitng devices will have notify_on_connect saved in DB, so need to check.
    notify_devices: List[ConnectedDevice] = []
    
    __logger.debug("%s new device(s) connected since last scan. Checking if they exist...", len(connected_devices))

    for device in connected_devices:
        found_device = data_access.find_device_by_mac(device.mac_address)
        
        if found_device is None:
            __logger.log(f"Device does not exist in DB. Adding it.")
            # Device doesn't exist yet. Add it to DB and notify_devices list
            device.last_connected_date = datetime.utcnow()
            device.notify_on_connect = True
            data_access.add_new_device(device)
            notify_devices.append(device)
        else:
            # Device exists in DB, update last connected date/ip and add to notify_devices list
            utc_now: datetime = datetime.utcnow()            
            device.last_connected_date = utc_now
            data_access.update_device_on_connection(device.mac_address, utc_now, device.ip_address)
            
            if found_device.notify_on_connect == True:
                notify_devices.append(found_device)
                
    __logger.debug("%s devices to notify for. They are:", len(notify_devices))
    
    json_list = []

    for dev in notify_devices:
        __logger.log(dev)
        json_list.append(dev.to_json())

    __logger.debug("Sleeping for %s seconds...", str(settings.SLEEP_TIME))
    
def log_prev_and_current(previous_devices, current_devices):
    __logger.debug('Prev:')
    for p in previous_devices.sort(key=lambda x: x.ip_address):
        __logger.debug(str(p))
    __logger.debug('Current:')                
    for p in current_devices.sort(key=lambda x: x.ip_address):
        __logger.debug(str(p))

def get_log_level():
    log_level = logging.DEBUG

    if len(sys.argv) > 1:
        log_level_arg = sys.argv[1]
        log_level_value = getattr(logging, log_level_arg.upper(), None)
    
        if isinstance(log_level_value, int):
            log_level = log_level_value
            
    return log_level

if __name__ == "__main__":
    try:
        log_level = get_log_level()
        logging.basicConfig(format='%(asctime)s - %(levelname)s: %(message)s',
                            encoding='utf-8', 
                            level=log_level,
                            handlers=[
                                logging.FileHandler("log.log"),
                                logging.StreamHandler()])

        start_monitor()
    except:
        __logger.fatal('Unexpected shutdown')
        __logger.fatal(traceback.format_exc())
