from logging import getLogger
import logging
import sys
from threading import Thread
import time
import service.network_monitor as network_monitor
import web.server as server
from multiprocessing import Process
import  shared.data_access as data_access

__logger = getLogger(__name__)

def get_log_level():
    log_level = logging.DEBUG

    if len(sys.argv) > 1:
        log_level_arg = sys.argv[1]
        log_level_value = getattr(logging, log_level_arg.upper(), None)
    
        if isinstance(log_level_value, int):
            log_level = log_level_value
            
    return log_level

if __name__ == "__main__":
    log_level = get_log_level()
    logging.basicConfig(format='%(asctime)s - %(levelname)s: %(message)s',
                        encoding='utf-8', 
                        level=log_level,
                        handlers=[
                            logging.FileHandler("log.log"),
                            logging.StreamHandler()])

    __logger.info('Application starting')

    data_access.create_db_if_not_exists()
    service_thread = Thread(target=network_monitor.monitor, daemon=True)

    __logger.info('Starting NetworkMonitor Service and Server')

    service_thread.start()
    server.serve()

    try:
        while True:
            # Keep the main thread alive
            time.sleep(10)  
    except KeyboardInterrupt:
        __logger.info("Ctrl+C detected. Exiting...")