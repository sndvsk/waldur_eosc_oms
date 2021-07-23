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


# TODO
# sync_members()


def check_project(project_data):
    # project_filter = wc.list_projects({'name': wc._get_project(project_data.attributes.name)['name']})
    # if len(wc.list_projects()) == 0:
    #     pass
    # else:
    #     for project in project_filter:
    #         if project_data.attributes.name == project['name']:
    #             return False
    #     else:
    #         return True
    if len(wc.list_projects()) == 0:
        pass
    else:
        for project in wc.list_projects():
            if project['uuid'] == wc._get_project(project_data.attributes.name)['uuid']:
                return False
            else:
                return True


def sync_customer(project_id):
    project_data = mp.get_project(project_id=project_id)
    customers_filter = wc.list_customers({'name': project_data.attributes.organization})
    if len(customers_filter) == 0:
        pass    # no customer with this name
    else:
        return customers_filter[0]  # data of existing customer with this name

    return wc.create_customer(name=project_data.attributes.organization,  # data of a new customer
                              email=project_data.owner.email,
                              address="Narva mnt 18",
                              registration_code=123,
                              backend_id=project_data.attributes.organization,
                              contact_details=project_data.attributes.organization,
                              country=pycountry.countries.get(name=project_data.attributes.country).alpha_2,
                              domain=project_data.attributes.department_webpage,
                              homepage=project_data.attributes.department_webpage,
                              native_name=project_data.owner.name,
                              )


def sync_projects():
    for event in get_events():
        if event.resource == 'project':
            project_data = mp.get_project(event.project_id)
            customer_data = sync_customer(project_id=event.project_id)
            if event.type == 'create':
                # TODO check if project already exists
                if check_project(project_data) is True:
                    continue
                else:
                    wc.create_project(customer_uuid=customer_data['uuid'],
                                      name=project_data.attributes.name,
                                      backend_id=project_data.id)
                    sync_orders(project_id=event.project_id,
                                project_name=project_data.attributes.name)
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


def sync_orders(project_id, project_name):
    for event in get_events():
        if event.resource == 'project_item' and event.project_id == project_id:
            if event.type == 'create':
                order_data = mp.get_project_item(project_id=project_id,
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
