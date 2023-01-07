import sqlite3
import utility
from datetime import datetime
from models import ConnectedDevice

def get_db_cursor():
    return cursor

def execute_command(command_text: str, args: tuple) -> None:
    connection = sqlite3.connect("Database/NetworkMonitor.db")
    cursor = connection.cursor()
    cursor.execute(command_text, args)
    connection.commit()
    connection.close()
    
def execute_query(query_text: str, args: tuple, fetch_all:bool) -> any:
    connection = sqlite3.connect("Database/NetworkMonitor.db")
    cursor = connection.cursor()
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
    
    result = execute_query(query_text, args, False)
    
    device: ConnectedDevice = None
    
    if result is not None:
        device = ConnectedDevice()
        device.friendly_name = result[0]
        device.device_name = result[1]
        device.ip_address = result[2]
        device.mac_address = result[3]
        device.vendor_name = result[4]
        device.notify_on_connect = result[5]
        device.last_connected_date = utility.ticks_to_date(result[6])
        
    return device
    
def add_new_device(device: ConnectedDevice) -> None:
    command_text =  """
                    Insert into ConnectedDevice
                    (FriendlyName, DeviceName, IPAddress,
                    MACAddress, VendorName, NotifyOnConnect,
                    LastConnectedDate)
                    values 
                    (null, ?, ?, ?, ?, 1, ?)
                    """
    
    args = (device.device_name, device.ip_address, device.mac_address, device.vendor_name, utility.date_to_ticks(device.last_connected_date))
    
    execute_command(command_text, args)
    
    return         
                   
def update_device_on_connection(mac_address: str, date: datetime, ip_address: str) -> None:
    command_text =  """
                    Update ConnectedDevice 
                    set 
                    LastConnectedDate = ?,
                    IPAddress = ? 
                    where MACAddress = ?
                    """

    args = (date, ip_address, mac_address)
    
    execute_command(command_text, args)
                   
    return