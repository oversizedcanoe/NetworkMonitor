class ConnectedDevice:
    def __init__(self):
        self._device_name = ''
        self._manufacturer_name = ''
        self._ip_address = ''
        self._mac_address = ''
    
    def __str__(self):
        return f"Device Name: '{self._device_name}'. Manufacturer: '{self._manufacturer_name}'. IP Address: '{self._ip_address}'. MAC Address: '{self._mac_address}'"
    
    @property
    def device_name(self) -> str:
        return self._device_name
    
    @device_name.setter
    def device_name(self, value) -> None:
        self._device_name = value
        
    @property
    def manufacturer_name(self) -> str:
        return self._manufacturer_name
    
    @manufacturer_name.setter
    def manufacturer_name(self, value) -> None:
        self._manufacturer_name = value
    
    @property    
    def ip_address(self) -> str:
        return self._ip_address
    @ip_address.setter
    def ip_address(self, value) -> None:
        self._ip_address = value
    
    @property    
    def mac_address(self) -> str:
        return self._ip_address
    @mac_address.setter
    def mac_address(self, value) -> None:
        # for consistency, replace '-' with ':' and capitalize all letters
        self._mac_address = value.replace('-', ':').upper()
        
    