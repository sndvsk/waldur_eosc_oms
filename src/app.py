import logging
from flask import Flask
import utils as utils

app = Flask(__name__)
logging.basicConfig(level=logging.DEBUG, format=f'%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')


@app.route('/sync-projects')
def sync_projects():
    utils.sync_projects()
    return "The projects were synced"


@app.route('/sync-orders')
def sync_orders():
    utils.sync_orders()
    return "The orders were synced"


if __name__ == '__main__':
    app_logger = app.logger

    app_logger.debug('Debug level log')
    app_logger.info('Info level log')
    app_logger.warning('Info level log')
    app_logger.error('Error level log')
    app_logger.critical('Critical level log')

    app.run(debug=True, host='127.0.0.1')
