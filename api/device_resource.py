from logging import getLogger
import traceback
import json
import falcon
from shared import data_access

_logger = getLogger(__name__)

class DeviceResource:
    # Get all devices in the database
    def on_get(self, req, resp):
        try:
            _logger.debug('Incoming GET Request')
            devices = data_access.get_all_devices()
            resp.text = json.dumps([item.serialize_device() for item in devices], ensure_ascii=False, default=str)
            resp.status = falcon.HTTP_200
            resp.content_type = falcon.MEDIA_JSON
            # some_param = req.get_param_as_int('id')
            _logger.debug('GET Request complete')
        except Exception as e:
            _logger.error('Error occurred')
            _logger.error(traceback.format_exc())
            resp.status = falcon.HTTP_500

    # Update device, maybe this could be patch?
    def on_post_id(self, req, resp, id):
        try:
            _logger.debug('Incoming POST Request')
            #req_body = req.media
            _logger.log('POST Request complete')
        except Exception as e:
            _logger.error('Error occurred')
            _logger.error(traceback.format_exc())
            resp.status = falcon.HTTP_500