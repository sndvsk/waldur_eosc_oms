import requests
import os
import pycountry
import urllib.parse
from datetime import datetime
from datetime import timedelta
from oms_jira import MPClient
from waldur_client import WaldurClient

EOSC_URL = "https://marketplace-3.docker-fid.grid.cyf-kr.edu.pl/"  # polling url
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


def get_or_create_project(project_data, customer_data):
    project_filter_list = wc.list_projects({'backend_id': str(project_data.id)})
    if len(project_filter_list) == 0:
        return wc.create_project(customer_uuid=customer_data['uuid'],
                                 name=project_data.attributes.name,
                                 backend_id=str(project_data.id))
    else:
        return project_filter_list[0]


def get_or_create_customer_for_project(project_data):
    customers_filter_list = wc.list_customers({'name_exact': project_data.attributes.organization})
    if len(customers_filter_list) != 0:
        return customers_filter_list[0]  # data of existing customer with this name

    return wc.create_customer(name=project_data.attributes.organization,  # data of a new customer
                              email=project_data.owner.email,
                              backend_id=project_data.attributes.organization,
                              country=pycountry.countries.get(name=project_data.attributes.country).alpha_2,
                              domain=project_data.attributes.department_webpage,
                              homepage=project_data.attributes.department_webpage,
                              native_name=project_data.attributes.organization,
                              )


def sync_projects():
    for event in get_events():
        if event.resource == 'project':
            project_data = mp.get_project(event.project_id)
            customer_data = get_or_create_customer_for_project(project_data=project_data)
            if event.type == 'create':
                get_or_create_project(project_data=project_data,
                                      customer_data=customer_data)
            if event.type == 'update':
                # TODO
                pass
            if event.type == 'delete':
                # TODO
                # there are no such events atm
                # wc.delete_project(project=wc.list_projects({'backend_id': str(event.project_id)})[0]['backend_id])
                pass
            else:
                pass
    pass


# TODO
def sync_orders():
    for event in get_events():
        if event.resource == 'project_item':
            project_data = mp.get_project(event.project_id)
            customer_data = get_or_create_customer_for_project(project_data=project_data)
            if event.type == 'create':
                offering_data = wc._get_offering(offering="3a878cee7bb749d0bb258d7b8442cb64")  # hardcoded
                project_data_for_order = get_or_create_project(project_data=project_data,
                                                     customer_data=customer_data)
                wc.create_marketplace_order(project=project_data_for_order['uuid'],
                                            offering=offering_data['uuid'],
                                            # offering name must match with waldur offering
                                            plan=offering_data['plans'][0]['uuid'],
                                            # 0 is index of the plan
                                            attributes=offering_data['attributes'],
                                            limits=None)
            if event.type == 'update':
                # TODO
                pass
            if event.type == 'delete':
                # TODO
                pass
            else:
                pass


# TODO
def sync_members():
    # TODO
    pass
