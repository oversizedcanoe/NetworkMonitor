from logging import getLogger
import traceback
import json
import falcon
from shared import data_access

__logger = getLogger(__name__)

class DeviceResource:
    # Get all devices in the database
    def on_get(self, req, resp):
        try:
            __logger.log('Incoming GET Request')
            resp.text = data_access.get_all_devices()
            resp.status = falcon.HTTP_200
            resp.content_type = falcon.MEDIA_JSON
            # some_param = req.get_param_as_int('id')
            __logger.log('GET Request complete')
        except Exception as e:
            __logger.error('Error occurred')
            __logger.error(traceback.format_exc())
            resp.status = falcon.HTTP_500

    # Update device, maybe this could be patch?
    def on_post(self, req, resp, id):
        try:
            __logger.log('Incoming POST Request')
            #req_body = req.media
            __logger.log('POST Request complete')
        except Exception as e:
            __logger.error('Error occurred')
            __logger.error(traceback.format_exc())
            resp.status = falcon.HTTP_500