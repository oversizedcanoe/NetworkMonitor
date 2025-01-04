from logging import getLogger
import shared.data_access as data_access
from service import network_manager
import time
import settings
from datetime import datetime, timezone
from shared.models import ConnectedDevice
from typing import List
import traceback

__logger = getLogger(__name__)

def get_devices_to_notify(previous: List[ConnectedDevice], current: List[ConnectedDevice]) -> List[ConnectedDevice]:
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


def handle_connected_devices(query_time: datetime, connected_devices: List[ConnectedDevice]) -> List[ConnectedDevice]:
    all_devices = data_access.get_all_devices()
    devices_to_notify_for: List[ConnectedDevice] = []

    for device in connected_devices:
        existing_device = next((dev for dev in all_devices if dev.mac_address == device.mac_address), None)

        if existing_device == None:
            # Device doesn't exist yet. Add it to DB and notify_devices list
            device.last_connected_date = query_time
            device.notify_on_connect = True
            data_access.add_new_device(device)
            devices_to_notify_for.append(device)
        else:
            # Has previously been connected, updated connection date/updated ip address
            existing_device.last_connected_date = query_time
            data_access.update_device_on_connection(existing_device.mac_address, query_time, existing_device.ip_address)
            if existing_device.notify_on_connect:
                devices_to_notify_for.append(existing_device)

def notify_new_connections(query_time: datetime, connected_devices: List[ConnectedDevice]) -> None:
    # TODO email or something
    for device in connected_devices:
        __logger.info('New device connected at %s -- %s', query_time, device.to_json())
    pass

def monitor_network_forever():
    previous_connected_devices: List[ConnectedDevice] = []

    while True:
        query_time = datetime.now(timezone.utc)
        connected_devices: List[ConnectedDevice] = network_manager.get_connected_devices()
        __logger.debug('%s device(s) connected.', str(len(connected_devices)))

        # Add or update all connected devices
        notify_connected_devices: List[ConnectedDevice] = handle_connected_devices(query_time, connected_devices, )

        # 'notify_connected_devices' is all currently connected devices which should be notified when they connect
        # However only notify if they are NEWLY connected (were not part of previously connected devices)
        devices_requiring_notification: List[ConnectedDevice] = get_devices_to_notify(previous_connected_devices, notify_connected_devices)
        __logger.debug('%s device(s) newly connected requiring notification.', str(len(devices_requiring_notification))) 

        if len(devices_requiring_notification) > 0:
            notify_new_connections(query_time, devices_requiring_notification)            
                       
        # Set this scans result to previous result 
        previous_connected_devices = connected_devices
        
        time.sleep(settings.SLEEP_TIME)

# def log_prev_and_current(previous_devices, current_devices):
#     __logger.debug('Prev:')
#     for p in previous_devices.sort(key=lambda x: x.ip_address):
#         __logger.debug(str(p))
#     __logger.debug('Current:')                
#     for p in current_devices.sort(key=lambda x: x.ip_address):
#         __logger.debug(str(p))

def monitor(): 
    try:
        __logger.info('Service starting up')
        monitor_network_forever()
    except Exception as e:
        __logger.fatal('Unexpected shutdown')
        __logger.fatal(traceback.format_exc())
        raise e