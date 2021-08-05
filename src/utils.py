import requests
import os
import pycountry
import urllib.parse
from datetime import datetime
from datetime import timedelta
from oms_jira import MPClient
from oms_jira.services.mp import MPMessage, ScopeEnum, MessageAuthor, ProjectItemStatusEnum
from waldur_client import WaldurClient
from src.app import app

app_logger = app.logger

EOSC_URL = os.environ.get('EOSC_URL')  # polling url
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
    app_logger.info('GET WALDUR TOKEN')
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
    app_logger.info('GET events from EOSC MP')
    return events


def post_message(project_item_data, content):
    msg_author = MessageAuthor(email="test@example.com",
                               name="Test Admin",
                               role="provider")

    msg = MPMessage(project_id=project_item_data.project_id,
                    project_item_id=project_item_data.id,
                    author=msg_author,
                    content=content,
                    scope=ScopeEnum.public)

    # return mp.create_message(message=msg)
    try:
        post_message_data = mp.post(mp.endpoint.message_list, data=msg.dict())
    except ValueError:
        app_logger.error(f'Message for new order {project_item_data.id} for project '
                         f'{project_item_data.project_id} was NOT posted')
    else:
        app_logger.info(f'Message for new order {project_item_data.id} for project '
                        f'{project_item_data.project_id} was posted')
        return post_message_data


def patch_project_item(project_item_data):
    try:
        patch_project_item_data = mp.patch(mp.endpoint.project_item.format(
            project_id=project_item_data.project_id,
            project_item_id=project_item_data.id),
            verify=False,
            data={
                # "user_secrets": {"access credentials": WALDUR_TOKEN}
            },
        )
    except ValueError:
        app_logger.error(f'Project item {project_item_data.id} from project '
                         f'{project_item_data.project_id} was NOT patched. '
                         f'Value: {patch_project_item_data["data"]}')
    else:
        app_logger.info(f'Project item {project_item_data.id} from project '
                        f'{project_item_data.project_id} was patched. '
                        f'Value: {patch_project_item_data["data"]}')
        return patch_project_item_data


def update_project_item(project_item_data, event_data):
    # TODO check if was already updated
    for change in event_data.changes:
        # for testing purposes because of invalid test input in eosc mp
        try:
            update_project_item_data = mp.update_project_item(project_id=project_item_data.project_id,
                                                              project_item_id=project_item_data.id,
                                                              status=ProjectItemStatusEnum(change.after))
        except ValueError:
            app_logger.error(f'Project item {project_item_data.id} from project '
                             f'{project_item_data.project_id} was NOT updated. '
                             f'{change.field}: {change.before} -> {change.after}')
        else:
            app_logger.info(f'Project item {project_item_data.id} from project '
                            f'{project_item_data.project_id} was updated. '
                            f'{change.field}: {change.before} -> {change.after}')
            return update_project_item_data


def get_or_create_order(offering_data, project_data_for_order, project_item_data):
    order_filter_list = wc.list_orders({'project_uuid': str(project_data_for_order['uuid'])})
    if len(order_filter_list) != 0:
        return order_filter_list[0]

    order_data = wc.create_marketplace_order(project=project_data_for_order['uuid'],
                                             offering=offering_data['uuid'],
                                             plan=offering_data['plans'][0]['uuid'],
                                             attributes=offering_data['attributes'],
                                             limits=None)

    content = "Your request has been successfully processed. " \
              f"Please login to {WALDUR_URL} to get access to your resource. " \
              "Invitation has been sent to your email. "

    post_message(project_item_data=project_item_data,
                 content=content)

    patch_project_item(project_item_data=project_item_data)
    return order_data


def get_or_create_project(project_data, customer_data):
    project_filter_list = wc.list_projects({'backend_id': str(project_data.id)})
    if len(project_filter_list) != 0:
        app_logger.info(f'Project with backend_id {project_data.id} is already in WALDUR, '
                        f'name: {project_filter_list[0]["name"]}.')
        return project_filter_list[0]
    try:
        create_project_data = wc.create_project(customer_uuid=customer_data['uuid'],
                                                name=project_data.attributes.name,
                                                backend_id=str(project_data.id))
    except ValueError:
        app_logger.error(f'Cannot create project with id {project_data.id}')
    else:
        app_logger.info(f'Project with backend_id {project_data.id} was created in WALDUR. '
                        f'Name of the project: {project_data.attributes.name}. '
                        f'Customer name: {project_data.attributes.organization}.')
        return create_project_data


def get_or_create_customer_for_project(project_data):
    customers_filter_list = wc.list_customers({'name_exact': project_data.attributes.organization})
    if len(customers_filter_list) != 0:
        app_logger.info(f'Customer named {project_data.attributes.organization} is already in WALDUR.')
        return customers_filter_list[0]  # data of existing customer with this name
    try:
        create_customer_data = wc.create_customer(name=project_data.attributes.organization,  # data of a new customer
                                                  email=project_data.owner.email,
                                                  backend_id=project_data.attributes.organization,
                                                  country=pycountry.countries.get(
                                                      name=project_data.attributes.country).alpha_2,
                                                  domain=project_data.attributes.department_webpage,
                                                  homepage=project_data.attributes.department_webpage,
                                                  native_name=project_data.attributes.organization,
                                                  )
    except ValueError:
        app_logger.error(f'Cannot customer named {project_data.attributes.organization}.')
    else:
        app_logger.info(f'Customer named {project_data.attributes.organization} was created in WALDUR.')
        return create_customer_data


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
                # there are no such events atm (eosc marketplace -> project -> edit -> webpage edit (no new events))
                pass
            if event.type == 'delete':
                # TODO
                # there are no such events atm
                # wc.delete_project(project=wc.list_projects({'backend_id': str(event.project_id)})[0]['backend_id])
                pass
            else:
                pass
    pass


def sync_orders():
    for event in get_events():
        if event.resource == 'project_item':
            project_data = mp.get_project(event.project_id)
            customer_data = get_or_create_customer_for_project(project_data=project_data)
            if event.type == 'create':
                offering_data = wc._get_offering(offering="3a878cee7bb749d0bb258d7b8442cb64")  # hardcoded
                app_logger.info(f'Using offering {offering_data["name"]}.')
                project_data_for_order = get_or_create_project(project_data=project_data,
                                                               customer_data=customer_data)
                project_item_data = mp.get_project_item(event.project_id, event.project_item_id)
                get_or_create_order(offering_data=offering_data,
                                    project_data_for_order=project_data_for_order,
                                    project_item_data=project_item_data)
            if event.type == 'update':
                # Nothing in waldur
                # project_item_data = mp.get_project_item(event.project_id, event.project_item_id)
                # update_project_item(project_item_data=project_item_data, event_data=event)
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
