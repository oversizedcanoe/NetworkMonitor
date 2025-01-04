import json
import utility
from dataclasses import dataclass, asdict
from datetime import datetime

@dataclass
class ConnectedDevice:
    def __init__(self):
        self._friendly_name = ''
        self._device_name = ''
        self._vendor_name = ''
        self._ip_address = ''
        self._mac_address = ''
        self._last_connected_date = None
    
    def __str__(self):
        return f"Device Name: '{self._device_name}'. Vendor: '{self._vendor_name}'. IP Address: '{self._ip_address}'. MAC Address: '{self._mac_address}'"
    
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
    def vendor_name(self) -> str:
        return self._vendor_name
    @vendor_name.setter
    def vendor_name(self, value) -> None:
        self._vendor_name = value
    
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
    
    
    def to_json(self):
        return json.dumps({"friendly_name": self.friendly_name, 
                     "device_name" : self.device_name,
                     "vendor_name": self.vendor_name,
                     "ip_address": self.ip_address,
                     "mac_address": self.mac_address,
                     "last_connected_date": utility.date_to_ticks(self.last_connected_date),
    })