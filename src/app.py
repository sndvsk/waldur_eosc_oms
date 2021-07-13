from flask import Flask
import urllib3
import json
from client_eosc import get_events_from_eosc

app = Flask(__name__)

urllib3.disable_warnings()  # unverified request


def to_file(filename, json_content):
    with open(filename, 'w', encoding='utf-8') as f:  # data to json file
        json.dump(json_content, f, ensure_ascii=False, indent=4)  # file with nice markdown


res = get_events_from_eosc()
to_file('data.json', res)  # file is created in repository only after stopping the application


@app.route('/')
def run_script():
    pass


if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1')
