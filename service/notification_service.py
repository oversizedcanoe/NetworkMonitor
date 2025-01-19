
from datetime import datetime
from logging import getLogger
from typing import List
from shared.models import ConnectedDevice
from service.email_service import send_email

__logger = getLogger(__name__)

def notify_new_connections(query_time: datetime, connected_devices: List[ConnectedDevice]) -> None:
    # Email
    subject = f"{len(connected_devices)} Device(s) Just Connected"
    contents = ""

    for device in connected_devices:
        if (device.friendly_name != None):
            contents += f"Named Device: {device.friendly_name}"
        else:
            contents += f"Unnamed Device (DeviceName: '{device.device_name}' Manufacturer: '{device.manufacturer}')"
        contents += '\n'

        __logger.info('Notifying new device connected at %s -- %s', query_time, device.to_json())

    send_email(subject, contents)