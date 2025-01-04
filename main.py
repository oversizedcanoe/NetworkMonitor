from logging import getLogger
import logging
import sys
import service.network_monitor as network_monitor
import web.server as server
from multiprocessing import Process

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
    
    service_process = Process(target=network_monitor.monitor_network_forever)
    server_process = Process(target=server.serve)

    __logger.info('Starting NetworkMonitor Service and Server')
    service_process.run()
    server_process.run()