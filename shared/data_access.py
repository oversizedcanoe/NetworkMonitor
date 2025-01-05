from logging import getLogger
import sqlite3
from datetime import datetime
from typing import List
from shared import helper
from shared.models import ConnectedDevice
from pathlib import Path

__logger = getLogger(__name__)
__base_path = str(Path(__file__).parent)

def get_db_connection() -> tuple[sqlite3.Connection, sqlite3.Cursor]:
    connection = sqlite3.connect(__base_path + '/Database/NetworkMonitor.db')
    cursor = connection.cursor()
    return (connection, cursor)

def create_db_if_not_exists():
    __logger.debug('Creating DB if not exists')
    f = open(__base_path + "/Database/CreateDatabase.sql", "r")
    __execute_command(f.read())

def __execute_command(command_text: str, args: tuple = ()) -> None:
    (connection, cursor) = get_db_connection()
    cursor.execute(command_text, args)
    connection.commit()
    connection.close()

def __execute_query(query_text: str, fetch_all: bool, args: tuple = ()) -> any:
    (connection, cursor) = get_db_connection()
    cursor.execute(query_text, args)
    
    result = None
    
    if fetch_all == True:
        result = cursor.fetchall()
    else:
        result = cursor.fetchone()
    
    connection.close()
    
    return result
    
def find_device_by_mac(mac_address: str) -> ConnectedDevice:
    query_text = """
                Select 
                FriendlyName, DeviceName, IPAddress,
                MACAddress, VendorName, NotifyOnConnect,
                LastConnectedDate
                from ConnectedDevice
                where MACAddress = ?
                """
    
    args = (mac_address,)
    
    result = __execute_query(query_text, False, args)
    
    device: ConnectedDevice = None
    
    if result is not None:
        print(device)
        device = ConnectedDevice()
        device.friendly_name = result[0]
        device.device_name = result[1]
        device.ip_address = result[2]
        device.mac_address = result[3]
        device.vendor_name = result[4]
        device.notify_on_connect = result[5]
        device.last_connected_date = helper.ticks_to_date(result[6])
        
    return device
    
def add_new_device(device: ConnectedDevice) -> None:
    command_text =  """
                    Insert into ConnectedDevice
                    (FriendlyName, DeviceName, IPAddress,
                    MACAddress, VendorName, NotifyOnConnect,
                    LastConnectedDate, DeviceType)
                    values 
                    (null, ?, ?, ?, ?, 1, ?, ?)
                    """
    
    args = (device.device_name, device.ip_address, device.mac_address, device.vendor_name, 
            helper.date_to_ticks(device.last_connected_date), int(device.device_type))
    
    __execute_command(command_text, args)
    
    return         
                   
def update_device_on_connection(mac_address: str, last_connected_date: datetime, updated_ip_address: str) -> None:
    command_text =  """
                    Update ConnectedDevice 
                    set 
                    LastConnectedDate = ?,
                    IPAddress = ? 
                    where MACAddress = ?
                    """

    args = (helper.date_to_ticks(last_connected_date), updated_ip_address, mac_address)
    
    __execute_command(command_text, args)
                   
    return

def get_all_devices() -> List[ConnectedDevice]:
    query_text = """
                Select 
                FriendlyName, DeviceName, IPAddress,
                MACAddress, VendorName, NotifyOnConnect,
                LastConnectedDate, DeviceType
                from ConnectedDevice
                """
    
    result = __execute_query(query_text, True)
    
    device: ConnectedDevice = None
    devices: List[ConnectedDevice] = []
    
    if result is not None:
        for row in result:
            device = ConnectedDevice()
            device.friendly_name = row[0]
            device.device_name = row[1]
            device.ip_address = row[2]
            device.mac_address = row[3]
            device.vendor_name = row[4]
            device.notify_on_connect = row[5]
            device.last_connected_date = helper.ticks_to_date(row[6])
            device.device_type = row[7]
            devices.append(device)
        
    return devices
    