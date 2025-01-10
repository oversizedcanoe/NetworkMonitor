import logging
import falcon
from wsgiref import simple_server
from api.device_resource import DeviceResource
from api.monitor_resource import MonitorResource

app = falcon.App(cors_enable=True)
_logger = logging.getLogger(__name__)

CERT_FILE = ''
KEY_FILE = ''

device_resource = DeviceResource()
app.add_route('/device', device_resource)
app.add_route('/device/{id}', device_resource, suffix='id')

monitor_resource = MonitorResource()
app.add_route('/monitor/lastquerytime', monitor_resource, suffix='last_query_time')
app.add_route('/monitor/sleeptime', monitor_resource, suffix='sleep_time')


def serve():
    #context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    #context.load_cert_chain(certfile=CERT_FILE, keyfile=KEY_FILE)

    httpd = simple_server.make_server('0.0.0.0', 8080, app)

    # httpd.socket = context.wrap_socket(httpd.socket, server_side=True)

    _logger.debug('Serving on port 8080...')
    httpd.serve_forever()
    _logger.debug('Shutting down')
    
if __name__ == "__main__":
    logging.basicConfig(format='%(asctime)s [%(levelname)s] %(funcName)s(): %(message)s',
                        encoding='utf-8', 
                        level=logging.DEBUG,
                        handlers=[logging.StreamHandler()])
    
    serve()
