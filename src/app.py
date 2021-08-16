import logging
from flask import Flask
# import schedule
# import time
import utils_orders as utils_orders
import utils_offers as utils_offers

# TODO remove flask
app = Flask(__name__)

logging.getLogger("requests").setLevel(logging.WARNING)
logging.basicConfig(level=logging.INFO, format=f'[%(asctime)s] %(filename)s:%(lineno)d %(levelname)s - '
                                               f'%(message)s')


@app.route('/sync-projects')
def sync_projects():
    utils_orders.sync_projects()
    logging.info('sync_projects is finished.')
    return "The projects were synced"


@app.route('/sync-orders')
def sync_orders():
    utils_orders.sync_orders()
    logging.info('sync_orders is finished.')
    return "The orders were synced"


@app.route('/process-offerings')
def sync_offerings():
    utils_offers.process_offerings()
    logging.info('process_resources is finished.')
    return "Offerings have been processed"


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
