import inspect
import json
from dataclasses import dataclass
from datetime import datetime
from shared import helper
from enum import IntEnum

class DeviceType(IntEnum):
    UNKNOWN = 0
    NETWORK_MONITOR_SERVER = 1
    ROUTER = 2
    COMPUTER = 3
    PHONE = 4
    SMART_HOME_DEVICE = 5
    TV = 6
    GAME_CONSOLE = 7

@dataclass
class ConnectedDevice:
    def __init__(self):
        self._id = 0
        self._friendly_name = ''
        self._device_name = ''
        self._manufacturer = ''
        self._ip_address = ''
        self._mac_address = ''
        self._last_connected_date = None
        self._device_type = DeviceType.UNKNOWN
    
    def __str__(self):
        return f"Device Name: '{self._device_name}'. Manufacturer: '{self.manufacturer}'. IP Address: '{self._ip_address}'. MAC Address: '{self._mac_address}'"
    
    @property
    def id(self) -> int:
        return self._id
    @id.setter
    def id(self, value) -> None:
        self._id = value
    
    @property
    def friendly_name(self) -> str:
        return self._friendly_name
    @friendly_name.setter
    def friendly_name(self, value) -> None:
        self._friendly_name = value
    
    @property
    def device_name(self) -> str:
        return self._device_name
    @device_name.setter
    def device_name(self, value) -> None:
        self._device_name = value
        
    @property
    def manufacturer(self) -> str:
        return self._manufacturer
    @manufacturer.setter
    def manufacturer(self, value) -> None:
        self._manufacturer = value
    
    @property    
    def ip_address(self) -> str:
        return self._ip_address
    @ip_address.setter
    def ip_address(self, value) -> None:
        self._ip_address = value
    
    @property    
    def mac_address(self) -> str:
        return self._mac_address
    @mac_address.setter
    def mac_address(self, value) -> None:
        # for consistency, replace '-' with ':' and capitalize all letters
        self._mac_address = value.replace('-', ':').upper()
        
    @property
    def notify_on_connect(self) -> bool:
        return self._notify_on_connect
    @notify_on_connect.setter
    def notify_on_connect(self, value) -> None:
        self._notify_on_connect = value
    
    @property
    def last_connected_date(self) -> datetime:
        return self._last_connected_date
    @last_connected_date.setter
    def last_connected_date(self, value) -> None:
        self._last_connected_date = value
    
    @property
    def device_type(self) -> DeviceType:
        return self._device_type
    @device_type.setter
    def device_type(self, value) -> None:
        self._device_type = value
    
    def to_json(self):
        return json.dumps({"friendly_name": self.friendly_name, 
                     "device_name" : self.device_name,
                     "manufacturer": self.manufacturer,
                     "ip_address": self.ip_address,
                     "mac_address": self.mac_address,
                     "last_connected_date": helper.date_to_ticks(self.last_connected_date),
    })

    def serialize_device(self) -> dict:
        result = {}
        for name, member in inspect.getmembers(type(self), predicate=lambda m: isinstance(m, property)):
            result[name] = getattr(self, name)
        return result