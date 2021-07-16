import json
import os
import sys

from oms_jira import MPClient

from client_eosc import get_project_from_eosc
from client_waldur import create_project

EOSC_URL = "https://marketplace-3.docker-fid.grid.cyf-kr.edu.pl/"  # polling url
TOKEN = os.environ.get('TOKEN')
OMS_ID = os.environ.get('OMS_ID')

mp = MPClient(endpoint_url=EOSC_URL, oms_id=OMS_ID, auth_token=TOKEN)


def sync_projects(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        data = json.load(f)
        for event in data['events']:
            if event['resource'] == 'project':
                if event['type'] == 'create':
                    project_data = mp.get_project(event['project_id'])
                    json.dump(project_data, sys.stdout, indent=2)
                    create_project(customer_id="1f8643e30e424c8cbfbb960301c20fb0",  # hardcoded uuid
                                   name=project_data['attributes']['name'], backend_id=project_data['id'])
