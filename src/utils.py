import requests
import os
from datetime import datetime
from datetime import timedelta
from oms_jira import MPClient
from waldur_client import WaldurClient

EOSC_URL = "https://marketplace-3.docker-fid.grid.cyf-kr.edu.pl/"  # polling url
TOKEN = os.environ.get('TOKEN')
OMS_ID = os.environ.get('OMS_ID')

USERNAME = os.environ.get('USERNAME')
PASSWORD = os.environ.get('PASSWORD')
waldur_url = "http://localhost/api/"


def get_waldur_token():
    WALDUR_AUTH = {'username': USERNAME, 'password': PASSWORD}
    r = requests.post('http://localhost/api-auth/password/', data=WALDUR_AUTH)
    content = r.json()
    return content['token']


WALDUR_TOKEN = get_waldur_token()

wc = WaldurClient(waldur_url, WALDUR_TOKEN)
mp = MPClient(endpoint_url=EOSC_URL, oms_id=OMS_ID, auth_token=TOKEN)


def get_time(time_delta=timedelta(days=20)):
    now = datetime.now()
    test_time = now - time_delta  # because polling is not working with time that is "now"
    return test_time


def get_events():
    events = mp.list_events(get_time(), limit=None)
    return events


def sync_organization():
    pass


def sync_projects():
    for event in get_events():
        if event.resource == 'project':
            if event.type == 'create':
                project_data = mp.get_project(event.project_id)
                wc.create_project(customer_uuid="1f8643e30e424c8cbfbb960301c20fb0",  # hardcoded uuid
                                  name=project_data.attributes.name, backend_id=project_data.id)
                sync_orders(project_id_=event.project_id, project_name=project_data.attributes.name)
            if event.type == 'update':
                # TODO
                pass
            if event.type == 'delete':
                # TODO
                pass
            else:
                pass
    pass


def sync_orders(project_id_, project_name):
    for event in get_events():
        if event.resource == 'project_item' and event.project_id == project_id_:
            if event.type == 'create':
                order_data = mp.get_project_item(project_id=project_id_,
                                                 project_item_id=event.project_item_id)
                # project_uuid="73201e09c2724b4db6634fda8a3f7787",  # hardcoded
                # offering_uuid="8eea8a6825da45a6bc0342574cdb0a97",  # hardcoded
                # plan_uuid="f8afe3975cfa4dcc9a199b7ccf7c71bb",  # hardcoded
                wc.create_marketplace_order(project=project_name,
                                            offering="8eea8a6825da45a6bc0342574cdb0a97",    # hardcoded
                                            plan=None,  # None so it is better for testing
                                            attributes=None,
                                            limits=None)
            if event.type == 'update':
                # TODO
                pass
            if event.type == 'delete':
                # TODO
                pass
            else:
                pass
