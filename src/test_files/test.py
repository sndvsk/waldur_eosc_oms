import urllib3
import json
import os
import requests
from datetime import datetime
from datetime import timedelta

urllib3.disable_warnings()  # unverified request

now = datetime.now()
test_time = now - timedelta(days=5)  # because polling is not working with time that is "now"
test_time = test_time.isoformat()

my_url = "https://marketplace-3.docker-fid.grid.cyf-kr.edu.pl/api/v1/oms/2/events"  # polling url
token = os.environ.get('TOKEN')

headers = {
    'accept': 'application/json',
    'X-User-Token': token,
}

params = (
    ('from_timestamp', test_time),
)

response = requests.get(my_url,
                        headers=headers,
                        params=params,
                        verify=False)  # because of _ssl.c:1124 [SSL: CERTIFICATE_VERIFY_FAILED]

packages_json = response.json()

with open('data.json', 'w', encoding='utf-8') as f:  # data to json file
    json.dump(packages_json, f, ensure_ascii=False, indent=4)  # file with nice markdown

# TODO client_waldur.py testing