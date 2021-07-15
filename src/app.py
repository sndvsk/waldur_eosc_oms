from flask import Flask
import urllib3
import json
from client_eosc import *
from client_waldur import *

app = Flask(__name__)

urllib3.disable_warnings()  # unverified request


def to_file(filename, json_content):
    with open(filename, 'w', encoding='utf-8') as f:  # data to json file
        json.dump(json_content, f, ensure_ascii=False, indent=4)  # file with nice markdown


# file is created in repository only after stopping the application
# res = get_event_list_from_eosc()
to_file('data/event_list.json', get_event_list_from_eosc())
# to_file('data/message_list.json', get_message_list_from_eosc())
# to_file('data/messages/{{massage_id}}.json', get_massage_from_eosc())
# to_file('data/projects/{{project_id}}/project_items/project_items_list.json', get_project_item_list_from_eosc())
# to_file('data/projects/{{project_id}}/project_items/{{project_item_id}}.json', get_project_item_from_eosc())
# to_file('data/projects/{{project_id}}.json', get_project_from_eosc())
# to_file('data/oms/oms_list.json', get_oms_list_from_eosc())
# to_file('data/oms/{{oms_id}}.json', get_oms_from_eosc())


@app.route('/')
def run_script():
    pass


if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1')
