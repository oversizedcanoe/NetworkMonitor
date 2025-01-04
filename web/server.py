from logging import getLogger
import traceback

__logger = getLogger(__name__)

def serve():
    try:
        __logger.info('Server starting up')
        pass
    except Exception as e:
        __logger.fatal('Unexpected shutdown')
        __logger.fatal(traceback.format_exc())
        raise e