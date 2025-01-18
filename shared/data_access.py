from logging import getLogger
import sqlite3
from datetime import datetime, timezone
from typing import List
from shared import helper
from shared.models import ConnectedDevice
from pathlib import Path
import glob
import os

__logger = getLogger(__name__)
__base_path = str(Path(__file__).parent)

def get_db_connection() -> tuple[sqlite3.Connection, sqlite3.Cursor]:
    connection = sqlite3.connect(__base_path + '/Database/NetworkMonitor.db')
    cursor = connection.cursor()
    return (connection, cursor)

def initialize_db():
    __logger.debug('Initializing DB and running migrations')
    directory = __base_path + '/Database/Migrations/'
    migration_name = "000_CreateMigrationTable.sql"
    f = open(directory + migration_name, "r")
    __execute_command(f.read())
    add_migration(migration_name)

    migrations_applied = get_migrations()

    migrations_available = glob.glob(directory + '*')
    migrations_available.sort()
    
    for migration in migrations_available:
        _, file_name = os.path.split(migration)
        if file_name not in migrations_applied:
            migration_file = open(migration, "r")
            __logger.debug('Applying migration: %s', file_name)
            __execute_command(migration_file.read())
            add_migration(file_name)

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

def get_migrations() -> List[str]:
    query_text = """
                Select
                MigrationName
                from Migrations
                """
    
    result = __execute_query(query_text, True)
    migrations = []

    for row in result:
        migrations.append(row[0])

    return migrations
    

def add_migration(migration_name: str) -> None:
    command_text = """
                    Insert into Migrations 
                    (MigrationName, AppliedDate)
                    values
                    (?, ?)
                    """
    
    args = (migration_name, helper.date_to_ticks(datetime.now(timezone.utc)))
    __execute_command(command_text, args)

def find_device_by_mac(mac_address: str) -> ConnectedDevice:
    query_text = """
                Select 
                ID, FriendlyName, DeviceName, IPAddress,
                MACAddress, Manufacturer, NotifyOnConnect,
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
        device.id = result[0]
        device.friendly_name = result[1]
        device.device_name = result[2]
        device.ip_address = result[3]
        device.mac_address = result[4]
        device.manufacturer = result[5]
        device.notify_on_connect = result[6]
        device.last_connected_date = helper.ticks_to_date(result[7])
        
    return device
    
def add_new_device(device: ConnectedDevice) -> None:
    command_text =  """
                    Insert into ConnectedDevice
                    (ID, FriendlyName, DeviceName, IPAddress,
                    MACAddress, Manufacturer, NotifyOnConnect,
                    LastConnectedDate, DeviceType)
                    values 
                    (null, null, ?, ?, ?, ?, 1, ?, ?)
                    """
    
    args = (device.device_name, device.ip_address, device.mac_address, device.manufacturer, 
            helper.date_to_ticks(device.last_connected_date), int(device.device_type))
    __execute_command(command_text, args)
                   
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

def update_device(device_id: int, device_name: str, device_type: int, notify: bool):
    command_text =  """
                    Update ConnectedDevice 
                    set 
                    FriendlyName = ?,
                    DeviceType = ?,
                    NotifyOnConnect = ? 
                    where ID = ?
                    """

    args = (device_name, device_type, notify, device_id)
    __execute_command(command_text, args)

def get_all_devices() -> List[ConnectedDevice]:
    query_text = """
                Select 
                ID, FriendlyName, DeviceName, IPAddress,
                MACAddress, Manufacturer, NotifyOnConnect,
                LastConnectedDate, DeviceType
                from ConnectedDevice
                """
    
    result = __execute_query(query_text, True)
    
    device: ConnectedDevice = None
    devices: List[ConnectedDevice] = []
    
    if result is not None:
        for row in result:
            device = ConnectedDevice()
            device.id = row[0]
            device.friendly_name = row[1]
            device.device_name = row[2]
            device.ip_address = row[3]
            device.mac_address = row[4]
            device.manufacturer = row[5]
            device.notify_on_connect = row[6]
            device.last_connected_date = helper.ticks_to_date(row[7])
            device.device_type = row[8]
            devices.append(device)
        
    return devices

def get_last_query_time() -> datetime:
    query_text = """
                Select 
                Value
                from LastQueryTime
                """
    
    result = __execute_query(query_text, False)

    if result is None:
        return datetime.min
    
    return helper.ticks_to_date(result[0])
    
def update_last_query_time(query_time) -> None:
    command_text = """
                    Update LastQueryTime 
                    set 
                    Value = ?
                    """

    args = (helper.date_to_ticks(query_time),)
    __execute_command(command_text, args)

