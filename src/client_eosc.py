import os
import requests
from datetime import datetime
from datetime import timedelta
import urllib.parse
from oms_jira.services.mp import MPClient


EOSC_URL = "https://marketplace-3.docker-fid.grid.cyf-kr.edu.pl/"  # polling url
TOKEN = os.environ.get('TOKEN')
OMS_ID = os.environ.get('OMS_ID')

mp = MPClient(endpoint_url=EOSC_URL, oms_id=OMS_ID, auth_token=TOKEN)


# from https://github.com/cyfronet-fid/oms-adapter-jira/blob/dd056e114fcd0f0e1259723c35819f1b9863b331/oms_jira
# /services/mp.py#L259
EVENT_LIST_URL = "/api/v1/oms/%s/events"
MESSAGE_LIST_URL = f"/api/v1/oms/{OMS_ID}/messages"
MESSAGE_URL = f"/api/v1/oms/{OMS_ID}/messages/{{message_id}}"
PROJECT_ITEM_LIST_URL = f"/api/v1/oms/{OMS_ID}/projects/{{project_id}}/project_items"
PROJECT_ITEM_URL = "/api/v1/oms/%s/projects/%s/project_items/%s"
PROJECT_LIST_URL = f"/api/v1/oms/{OMS_ID}/projects"
PROJECT_URL = "/api/v1/oms/%s/projects/%s"
OMS_LIST_URL = f"/api/v1/oms"
OMS_URL = f"/api/v1/oms/{OMS_ID}"


def headers_params(time_delta=timedelta(days=20)):
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

    return headers, params


def get_project_from_eosc(project_id):
    headers, params = headers_params()

    response = requests.get(urllib.parse.urljoin(EOSC_URL, PROJECT_URL % (OMS_ID, str(project_id))),
                            headers=headers,
                            params=params,
                            verify=False)  # because of _ssl.c:1124 [SSL: CERTIFICATE_VERIFY_FAILED]

    # noinspection PyBroadException
    try:
        return response.json()

    except:
        return None


def get_event_list_from_eosc():
    headers, params = headers_params()

    response = requests.get(urllib.parse.urljoin(EOSC_URL, EVENT_LIST_URL % OMS_ID),
                            headers=headers,
                            params=params,
                            verify=False)  # because of _ssl.c:1124 [SSL: CERTIFICATE_VERIFY_FAILED]

    # noinspection PyBroadException
    try:
        return response.json()

    except:
        return None


def get_message_list_from_eosc():  # TODO
    headers, params = headers_params()

    response = requests.get(urllib.parse.urljoin(EOSC_URL, MESSAGE_LIST_URL),
                            headers=headers,
                            params=params,
                            verify=False)  # because of _ssl.c:1124 [SSL: CERTIFICATE_VERIFY_FAILED]

    # noinspection PyBroadException
    try:
        return response.json()

    except:
        return None


def get_message_from_eosc():  # TODO
    headers, params = headers_params()

    response = requests.get(urllib.parse.urljoin(EOSC_URL, MESSAGE_URL),
                            headers=headers,
                            params=params,
                            verify=False)  # because of _ssl.c:1124 [SSL: CERTIFICATE_VERIFY_FAILED]

    # noinspection PyBroadException
    try:
        return response.json()

    except:
        return None


def get_project_item_list_from_eosc():  # TODO
    headers, params = headers_params()

    response = requests.get(urllib.parse.urljoin(EOSC_URL, PROJECT_ITEM_LIST_URL),
                            headers=headers,
                            params=params,
                            verify=False)  # because of _ssl.c:1124 [SSL: CERTIFICATE_VERIFY_FAILED]

    # noinspection PyBroadException
    try:
        return response.json()

    except:
        return None


def get_project_item_from_eosc(project_id, project_item_id):  # TODO
    headers, params = headers_params()

    response = requests.get(urllib.parse.urljoin(EOSC_URL, PROJECT_ITEM_URL % (OMS_ID, project_id, project_item_id)),
                            headers=headers,
                            params=params,
                            verify=False)  # because of _ssl.c:1124 [SSL: CERTIFICATE_VERIFY_FAILED]

    # noinspection PyBroadException
    try:
        return response.json()

    except:
        return None


def get_oms_list_from_eosc():  # TODO
    headers, params = headers_params()

    response = requests.get(urllib.parse.urljoin(EOSC_URL, OMS_LIST_URL),
                            headers=headers,
                            params=params,
                            verify=False)  # because of _ssl.c:1124 [SSL: CERTIFICATE_VERIFY_FAILED]

    # noinspection PyBroadException
    try:
        return response.json()

    except:
        return None


def get_oms_from_eosc():  # TODO
    headers, params = headers_params()

    response = requests.get(urllib.parse.urljoin(EOSC_URL, OMS_URL),
                            headers=headers,
                            params=params,
                            verify=False)  # because of _ssl.c:1124 [SSL: CERTIFICATE_VERIFY_FAILED]

    # noinspection PyBroadException
    try:
        return response.json()

    except:
        return None
