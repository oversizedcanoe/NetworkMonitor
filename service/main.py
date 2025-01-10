
from logging import getLogger
import logging
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import network_monitor

from shared import data_access

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
    __logger.info('Starting NetworkMonitor Service')

    network_monitor.monitor()