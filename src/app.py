import logging
from flask import Flask
import utils as utils
import schedule
import time

# https://pypi.org/project/python-crontab/

# TODO remove flask
app = Flask(__name__)

logging.getLogger("requests").setLevel(logging.WARNING)
logging.basicConfig(level=logging.INFO, format=f'[%(asctime)s] %(filename)s:%(lineno)d %(levelname)s - '
                                               f'%(message)s')


@app.route('/sync-projects')
def sync_projects():
    utils.sync_projects()
    logging.info('sync_projects is finished.')
    return "The projects were synced"


@app.route('/sync-orders')
def sync_orders():
    utils.sync_orders()
    logging.info('sync_orders is finished.')
    return "The orders were synced"


@app.route('/process-offerings')
def sync_offerings():
    utils.process_offerings()
    logging.info('process_resources is finished.')
    return "Offerings have been gotten"


if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1')


# # Time
# schedule.every(20).seconds.do(sync_projects)
# schedule.every(30).seconds.do(sync_orders)
#
#
# try:
#     while True:
#         schedule.run_pending()
#         time.sleep(1)
# except KeyboardInterrupt:
#     print('Interrupted!')
