import os
import requests
from datetime import datetime
from datetime import timedelta

EOSC_URL = "https://marketplace-3.docker-fid.grid.cyf-kr.edu.pl/api/v1/oms/2/events"  # polling url
TOKEN = os.environ.get('TOKEN')


def get_events_from_eosc(time_delta=timedelta(days=5)):
    now = datetime.now()
    test_time = now - time_delta  # because polling is not working with time that is "now"
    test_time = test_time.isoformat()

    headers = {
        'accept': 'application/json',
        'X-User-Token': TOKEN,
    }

    params = (
        ('from_timestamp', test_time),
    )

    response = requests.get(EOSC_URL,
                            headers=headers,
                            params=params,
                            verify=False)  # because of _ssl.c:1124 [SSL: CERTIFICATE_VERIFY_FAILED]

    # noinspection PyBroadException
    # TODO: error handling (try/except block); by default, return [] or None
    try:
        return response.json()

    except:
        return None
