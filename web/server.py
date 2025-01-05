from logging import getLogger
import time
import traceback

__logger = getLogger(__name__)

def serve():
    try:
        __logger.info('Server starting up')
        while True:
            __logger.debug('servin stuff')
            time.sleep(3)
    except Exception as e:
        __logger.fatal('Unexpected shutdown')
        __logger.fatal(traceback.format_exc())
        raise e