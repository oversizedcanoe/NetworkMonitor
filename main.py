from logging import getLogger
import logging
import sys
from threading import Thread
import time
import api.server as server
import service.network_monitor as network_monitor
import shared.data_access as data_access

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
    logging.basicConfig(format='%(asctime)s [%(levelname)s] %(funcName)s(): %(message)s',
                        encoding='utf-8', 
                        level=log_level,
                        handlers=[
                            logging.FileHandler("log.log"),
                            logging.StreamHandler()])

    __logger.info('Application starting')
    data_access.initialize_db()
    

    service_thread = Thread(target=network_monitor.monitor, daemon=True)

    __logger.info('Starting NetworkMonitor Service and API')
    service_thread.start()
    server.serve()
    # TODO start Astro site
    
    try:
        while True:
            # Keep the main thread alive
            time.sleep(100)  
    except KeyboardInterrupt:
        __logger('Ctrl+C detected, shutting down')