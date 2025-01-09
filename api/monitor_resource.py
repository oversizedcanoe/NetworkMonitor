from logging import getLogger
import traceback
import json
import falcon

import settings
from shared import data_access

_logger = getLogger(__name__)

class MonitorResource:
    # Get last query time
    def on_get_last_query_time(self, req, resp):
        try:
            _logger.debug('Incoming GET Request')
            resp.text = data_access.get_last_query_time()
            resp.status = falcon.HTTP_200
            resp.content_type = falcon.MEDIA_JSON
            # some_param = req.get_param_as_int('id')
            _logger.debug('GET Request complete')
        except Exception as e:
            _logger.error('Error occurred')
            _logger.error(traceback.format_exc())
            resp.status = falcon.HTTP_500

    # Get last query time
    def on_get_sleep_time(self, req, resp):
        try:
            _logger.debug('Incoming GET Request')
            resp.text = settings.SLEEP_TIME
            resp.status = falcon.HTTP_200
            resp.content_type = falcon.MEDIA_JSON
            _logger.debug('GET Request complete')
        except Exception as e:
            _logger.error('Error occurred')
            _logger.error(traceback.format_exc())
            resp.status = falcon.HTTP_500
