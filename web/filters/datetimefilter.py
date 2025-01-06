from datetime import datetime
from dateutil import tz

def datetimefilter(value: datetime) -> str:
    if value.tzinfo is None:
        value = value.replace(tzinfo=tz.tzutc())    
    to_zone = tz.tzlocal()
    local_time = value.astimezone(to_zone)
    return local_time.strftime('%Y-%m-%d %H:%M:%S')
