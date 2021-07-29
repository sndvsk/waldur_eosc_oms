from flask import Flask
import utils as utils

app = Flask(__name__)

utils.get_events()


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
