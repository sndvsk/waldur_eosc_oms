import json

from flask import Flask
import urllib3
import client_eosc as ce

app = Flask(__name__)

urllib3.disable_warnings()  # unverified request


def to_file(filename, json_content):
    with open(filename, 'w', encoding='utf-8') as f:  # data to json file
        json.dump(json_content, f, ensure_ascii=False, indent=4)  # file with nice markdown
        f.close()  # create file without closing the program


to_file('data/event_list.json', ce.get_event_list_from_eosc())


@app.route('/sync-projects')
def sync_projects():
    ce.sync_projects('data/event_list.json')
    return "The projects were synced"


if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1')
