import urllib3
import json
import requests
import datetime

urllib3.disable_warnings()


timestamp_atm = datetime.datetime.now().isoformat()
my_url = "https://marketplace-3.docker-fid.grid.cyf-kr.edu.pl/api/v1/oms/2/events"
r_ = '<insert_token_here>'

headers = {
    'accept': 'application/json',
    'X-User-Token': r_,
}

params = (
    ('from_timestamp', timestamp_atm),
)

response = requests.get(my_url,
                        headers=headers,
                        params=params,
                        verify=False)

print(response.status_code)

json_data = json.loads(response.text)

print(json_data)