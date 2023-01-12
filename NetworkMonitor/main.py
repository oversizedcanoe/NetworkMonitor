import data_access
import logger
import network_manager
import time
import settings
from datetime import datetime
from models import ConnectedDevice
from typing import List

def start_monitor():
    logger.log('Application started. Monitoring network.')
    
    previous_connected_devices: List[ConnectedDevice] = []
    
    while True:    
        connected_devices: List[ConnectedDevice] = network_manager.get_connected_devices()
        logger.log('Found ' + str(len(connected_devices)) + ' devices.')
        
        newly_connected_devices: List[ConnectedDevice] = get_new_devices(previous_connected_devices, connected_devices)
        
        if len(newly_connected_devices) > 0:
            logger.log(str(len(newly_connected_devices)) + ' new device(s) connected.') 
            
            #for new_dev in newly_connected_devices:
            #    logger.log(str(new_dev) + ' is now connected.')
                
            handle_new_devices(newly_connected_devices)            
        else:       
            logger.log('No new devices connected.')
                       
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
    
    logger.log(f"{len(connected_devices)} new device(s) connected since last scan. Checking if they exist...")
    for device in connected_devices:
        found_device = data_access.find_device_by_mac(device.mac_address)
        
        if found_device is None:
            logger.log(f"Device does not exist in DB. Adding it.")
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
                
    logger.log(f"{len(notify_devices)} devices to notify for. They are:")
    for dev in notify_devices:
        logger.log(dev)
        
    logger.log("Sleeping for " + str(settings.SLEEP_TIME) + " seconds...")
    
    # DO SOMETHING WITH notify_devices: email, text, check if specific MAC Address is connected and
    # run Alexa skill etc
    
def log_prev_and_current(previous_devices, current_devices):
    logger.log('Prev:')
    for p in previous_devices.sort(key=lambda x: x.ip_address):
        logger.log(str(p))
    logger.log('Current:')                
    for p in current_devices.sort(key=lambda x: x.ip_address):
        logger.log(str(p))
    

if __name__ == "__main__":
    #data_access.test()
    start_monitor()