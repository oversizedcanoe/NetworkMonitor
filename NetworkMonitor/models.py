class ConnectedDevice:
    def __init__(self):
        self.device_name = ''
        self.manufacturer_name = ''
        self.ip_address = ''
        self.mac_address = ''
    
    def __str__(self):
        return f"Device Name: '{self.device_name}'. Manufacturer: '{self.manufacturer_name}'. IP Address: '{self.ip_address}'. MAC Address: '{self.mac_address}'"
    
    def _get_device_name(self) -> str:
        return self.device_name
    def _set_device_name(self, value) -> None:
        self.device_name = value
    
    def _get_manufacturer_name(self) -> str:
        return self.manufacturer_name
    def _set_manufacturer_name(self, value) -> None:
        self.manufacturer_name = value
        
    def _get_ip_address(self) -> str:
        return self.ip_address
    def _set_ip_address(self, value) -> None:
        self.ip_address = value
        
    def _get_mac_address(self) -> str:
        return self.ip_address
    def _set_mac_address(self, value) -> None:
        self.mac_address = value
        
    