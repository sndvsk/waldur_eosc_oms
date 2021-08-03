import logging
from flask import Flask
import utils as utils

app = Flask(__name__)

logging.getLogger("requests").setLevel(logging.WARNING)
logging.basicConfig(level=logging.INFO, format=f'[%(asctime)s] %(filename)s:%(lineno)d %(levelname)s - '
                                                f'%(message)s')


@app.route('/sync-projects')
def sync_projects():
    utils.sync_projects()
    return "The projects were synced"


@app.route('/sync-orders')
def sync_orders():
    utils.sync_orders()
    return "The orders were synced"


if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1')
