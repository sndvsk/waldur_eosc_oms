import urllib

import requests
import os
import urllib.parse
from datetime import datetime
from datetime import timedelta
from oms_jira import MPClient
from waldur_client import WaldurClient

EOSC_URL = "https://marketplace-3.docker-fid.grid.cyf-kr.edu.pl/"  # polling url
# BETA_URL = "https://beta.marketplace.eosc-portal.eu/"
TOKEN = os.environ.get('TOKEN')
OMS_ID = os.environ.get('OMS_ID')

USERNAME = os.environ.get('USERNAME')
PASSWORD = os.environ.get('PASSWORD')
WALDUR_URL = os.environ.get('WALDUR_URL')
WALDUR_API = urllib.parse.urljoin(WALDUR_URL, 'api/')
WALDUR_API_AUTH = urllib.parse.urljoin(WALDUR_URL, 'api-auth/password/')


def get_waldur_token():
    WALDUR_AUTH = {'username': USERNAME, 'password': PASSWORD}
    re = requests.post(WALDUR_API_AUTH, data=WALDUR_AUTH)
    content = re.json()
    return content['token']


WALDUR_TOKEN = get_waldur_token()

wc = WaldurClient(WALDUR_API, WALDUR_TOKEN)
mp = MPClient(endpoint_url=EOSC_URL, oms_id=OMS_ID, auth_token=TOKEN)


def get_time(time_delta=timedelta(days=20)):
    now = datetime.now()
    test_time = now - time_delta  # because polling is not working with time that is "now"
    return test_time


def get_events():
    events = mp.list_events(get_time(), limit=None)
    return events


# TODO
# if there are old events, that are already created, pass
# sync_organization(), sync_members()


def sync_customer(project_id):
    project_data = mp.get_project(project_id=project_id)
    wc.create_customer(name=project_data.attributes.name,
                       email=project_data.owner.email,
                       address=None,
                       registration_code=None,
                       backend_id=None,
                       abbreviation=None,
                       bank_account=None,
                       bank_name=None,
                       contact_details=project_data.attributes.organization,
                       country=project_data.attributes.country,
                       display_name=project_data.attributes.name,
                       domain=project_data.attributes.scientific_domains[0],
                       homepage=project_data.attributes.department_webpage,
                       native_name=project_data.owner.name,
                       latitude=None,
                       longitude=None,
                       owners=project_data.owner,
                       phone_number=None,
                       postal=None,
                       support_users=None,
                       vat_code=None)
    # TODO
    pass


def sync_projects():
    for event in get_events():
        if event.resource == 'project':
            sync_customer(project_id=event.project_id)
            if event.type == 'create':
                project_data = mp.get_project(event.project_id)
                wc.create_project(customer_uuid="1f8643e30e424c8cbfbb960301c20fb0",  # hardcoded uuid
                                  name=project_data.attributes.name,
                                  backend_id=project_data.id)
                sync_orders(project_id_=event.project_id,
                            project_name=project_data.attributes.name)
            if event.type == 'update':
                # TODO
                pass
            if event.type == 'delete':
                # TODO
                wc.delete_project(project=event.project_id)
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
                wc.create_marketplace_order(project=project_name,
                                            offering=wc._get_offering(order_data.attributes.service,
                                                                      project_name)['uuid'],
                                            # offering name must match with waldur offering
                                            plan=wc._get_offering(order_data.attributes.service,
                                                                  project_name)['plans'][0]['uuid'],
                                            # 0 is index of the plan
                                            attributes=wc._get_offering(order_data.attributes.service,
                                                                        project_name)['attributes'],
                                            limits=None)
            if event.type == 'update':
                # TODO
                pass
            if event.type == 'delete':
                # TODO
                pass
            else:
                pass


def sync_members():
    # TODO
    pass


def check_project_existence(project_id):
    pass


def check_order_existence(project_id, project_item_id):
    pass


def check_customer_existence(customer_id):
    pass


