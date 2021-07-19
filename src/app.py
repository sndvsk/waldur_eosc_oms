from flask import Flask
import urllib3
import utils as utils

app = Flask(__name__)

urllib3.disable_warnings()  # unverified request


utils.get_events()


@app.route('/sync-projects')
def sync_projects():
    utils.sync_projects()
    return "The projects and orders were synced"


# @app.route('/sync-orders')
# def sync_orders():
#     utils.sync_orders(project_id_=1449)  # hardcoded
#     return "The orders were synced"


if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1')
