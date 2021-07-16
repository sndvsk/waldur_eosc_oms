import json
import os
import sys
from datetime import datetime
from datetime import timedelta

from oms_jira import MPClient

from client_waldur import create_project, create_order
from src.client_eosc import get_project_item_from_eosc, get_project_from_eosc

EOSC_URL = "https://marketplace-3.docker-fid.grid.cyf-kr.edu.pl/"  # polling url
TOKEN = os.environ.get('TOKEN')
OMS_ID = os.environ.get('OMS_ID')

mp = MPClient(endpoint_url=EOSC_URL, oms_id=OMS_ID, auth_token=TOKEN)


def get_time(time_delta=timedelta(days=20)):
    now = datetime.now()
    test_time = now - time_delta  # because polling is not working with time that is "now"
    return test_time


def get_events():
    events = mp.list_events(get_time(), limit=None)
    return events


# TODO using get_events()
def sync_projects(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        data = json.load(f)
        for event in data['events']:
            if event['resource'] == 'project':
                if event['type'] == 'create':
                    project_data = mp.get_project(event['project_id'])
                    create_project(customer_id="1f8643e30e424c8cbfbb960301c20fb0",  # hardcoded uuid
                                   name=project_data.attributes.name, backend_id=project_data.id)
                if event['type'] == 'update':
                    # TODO
                    pass
                if event['type'] == 'delete':
                    # TODO
                    pass
                else:
                    pass


# TODO using get_events()
def sync_orders(filename, project_id):
    with open(filename, 'r', encoding='utf-8') as f:
        data = json.load(f)
        for event in data['events']:
            if event['resource'] == 'project_item' and event['project_id'] == project_id:
                if event['type'] == 'create':
                    order_data = mp.get_project_item(project_id=project_id,
                                                     project_item_id=1)  # hardcoded
                    create_order(project="73201e09c2724b4db6634fda8a3f7787",  # hardcoded
                                 offering="8eea8a6825da45a6bc0342574cdb0a97",  # hardcoded
                                 plan="f8afe3975cfa4dcc9a199b7ccf7c71bb",  # hardcoded
                                 attributes=None, limits=None)  # does not work if attributes are not None
                if event['type'] == 'update':
                    # TODO
                    pass
                if event['type'] == 'delete':
                    # TODO
                    pass
                else:
                    pass


def sync_organization():
    pass
