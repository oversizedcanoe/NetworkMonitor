from datetime import datetime

def log(message: str) -> None:
    current_time = str(datetime.now())
    print(f'{current_time} - {message}')