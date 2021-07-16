import json

import requests
from flask import Flask
import urllib3
import utils as utils

app = Flask(__name__)

urllib3.disable_warnings()  # unverified request


def to_file(filename, json_content):
    with open(filename, 'w', encoding='utf-8') as f:  # data to json file
        json.dump(json_content, f, ensure_ascii=False, indent=4)  # file with nice markdown
        f.close()  # create file without closing the program


# to_file('data/event_list.json', ce.get_event_list_from_eosc())
utils.get_events()


@app.route('/sync-projects')
def sync_projects():
    utils.sync_projects('data/event_list.json')
    return "The projects were synced"


@app.route('/sync-orders')
def sync_orders():
    utils.sync_orders('data/event_list.json', project_id=1449)  # hardcoded
    return "The orders were synced"


if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1')
