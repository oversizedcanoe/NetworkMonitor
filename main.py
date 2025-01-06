from logging import getLogger
import logging
import sys
from threading import Thread
import time
import service.network_monitor as network_monitor
import web.server as server
import  shared.data_access as data_access
from werkzeug.serving import is_running_from_reloader

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
    data_access.initialize_db()
    __logger.info('Starting NetworkMonitor Service and Server')

    if not is_running_from_reloader():
        service_thread = Thread(target=network_monitor.monitor, daemon=True)
        service_thread.start()

    # Run flask server on the main thread, otherwise debugging/hot reload doesn't work
    server.serve()

    try:
        while True:
            # Keep the main thread alive
            time.sleep(10)  
    except KeyboardInterrupt:
        __logger.info("Ctrl+C detected. Exiting...")