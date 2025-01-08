from logging import getLogger
import time
import traceback
from flask import Flask, render_template
from shared import data_access
from web_old.filters.datetimefilter import datetimefilter

__logger = getLogger(__name__)

app = Flask(__name__)

app.jinja_env.filters['datetimefilter'] = datetimefilter

@app.route("/")
def index():
    connected_devices = data_access.get_all_devices()
    last_query_time = data_access.get_last_query_time()
    return render_template('index.html', devices = connected_devices, last_query_time = last_query_time)

def serve():
    try:
        __logger.info('Server starting up')
        # TODO app.run should not be used in production
        app.run(debug=True, host='0.0.0.0', port=5000)
    except Exception as e:
        __logger.fatal('Unexpected shutdown')
        __logger.fatal(traceback.format_exc())
        raise e
    
serve()
