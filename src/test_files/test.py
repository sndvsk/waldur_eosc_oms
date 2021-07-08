import urllib3
import json
import requests
from datetime import datetime
from datetime import timedelta

urllib3.disable_warnings()  # unverified request

now = datetime.now()
test_time = now - timedelta(hours=12)    # because polling is not working with time that is "now"
test_time = test_time.isoformat()


my_url = "https://marketplace-3.docker-fid.grid.cyf-kr.edu.pl/api/v1/oms/2/events"  # polling url
token = '<insert_token>'
# <insert_token>

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
                        verify=False)   # because of _ssl.c:1124 [SSL: CERTIFICATE_VERIFY_FAILED]

packages_json = response.json()
packages_str = json.dumps(packages_json)

# print(response.status_code)
# print(packages_json)
# print(test_time)


with open('data.json', 'w', encoding='utf-8') as f:  # data to json file
    json.dump(packages_json, f, ensure_ascii=False, indent=4)   # file with nice markdown
