import logging
import requests
import os
import pycountry
import urllib.parse
from datetime import datetime
from datetime import timedelta
from oms_jira import MPClient
from oms_jira.services.mp import MPMessage, ScopeEnum, MessageAuthor, ProjectItemStatusEnum
from waldur_client import WaldurClient, ProjectRole

logging.getLogger("requests").setLevel(logging.WARNING)
logging.basicConfig(level=logging.INFO, format=f'[%(asctime)s] %(filename)s:%(lineno)d %(levelname)s - '
                                               f'%(message)s')

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
    response = requests.post(WALDUR_API_AUTH, data=WALDUR_AUTH)
    content = response.json()
    logging.info('GET WALDUR TOKEN')
    return content['token']


waldur_client = WaldurClient(WALDUR_API, get_waldur_token())
mp = MPClient(endpoint_url=EOSC_URL, oms_id=OMS_ID, auth_token=TOKEN)


# noinspection DuplicatedCode
def get_time(time_delta=timedelta(days=20)):
    now = datetime.now()
    test_time = now - time_delta  # because polling is not working with time that is "now"
    return test_time


def get_events():
    events = mp.list_events(get_time(), limit=None)
    logging.info('GET events from EOSC MP')
    return events


def get_waldur_offering_data(offering_uuid):
    offering_data = waldur_client._get_offering(offering=offering_uuid)
    # Nordic Test Resource 2 -> 5162bd1a4dc146bfa8576d62cca49e43
    # Nordic Test Resource 1 -> 3a878cee7bb749d0bb258d7b8442cb64
    return offering_data


def invite_user_to_project(email, project):
    waldur_client.create_project_invitation(email=email,
                                            project=project,
                                            project_role=ProjectRole.ADMINISTRATOR)


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
        logging.error(f'Message for new order {project_item_data.id} for project '
                      f'{project_item_data.project_id} was NOT posted')
    else:
        logging.info(f'Message for new order {project_item_data.id} for project '
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
        logging.error(f'Project item {project_item_data.id} from project '
                      f'{project_item_data.project_id} was NOT patched. '
                      'Value: error')
    else:
        logging.info(f'Project item {project_item_data.id} from project '
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
            logging.error(f'Project item {project_item_data.id} from project '
                          f'{project_item_data.project_id} was NOT updated. '
                          f'{change.field}: {change.before} -> {change.after}')
        else:
            logging.info(f'Project item {project_item_data.id} from project '
                         f'{project_item_data.project_id} was updated. '
                         f'{change.field}: {change.before} -> {change.after}')
            return update_project_item_data


def get_or_create_order(offering_data, project_data_for_order, project_item_data):
    order_filter_list = waldur_client.list_orders({'project_uuid': str(project_data_for_order['uuid'])})
    if len(order_filter_list) != 0:
        return order_filter_list[0]

    order_data = waldur_client.create_marketplace_order(project=project_data_for_order['uuid'],
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
    project_filter_list = waldur_client.list_projects({'backend_id': str(project_data.id)})
    if len(project_filter_list) != 0:
        logging.info(f'Project with backend_id {project_data.id} is already in WALDUR, '
                     f'name: {project_filter_list[0]["name"]}.')
        return project_filter_list[0]
    try:
        create_project_data = waldur_client.create_project(customer_uuid=customer_data['uuid'],
                                                           name=project_data.attributes.name,
                                                           backend_id=str(project_data.id))
    except ValueError:
        logging.error(f'Cannot create project with id {project_data.id}')
    else:
        logging.info(f'Project with backend_id {project_data.id} was created in WALDUR. '
                     f'Name of the project: {project_data.attributes.name}. '
                     f'Customer name: {project_data.attributes.organization}.')
        invite_user_to_project(email=project_data.owner.email,
                               project=project_filter_list[0]['uuid'])
        return create_project_data


def get_or_create_customer_for_project(project_data):
    customers_filter_list = waldur_client.list_customers({'name_exact': project_data.attributes.organization})
    if len(customers_filter_list) != 0:
        logging.info(f'Customer named {project_data.attributes.organization} is already in WALDUR.')
        return customers_filter_list[0]  # data of existing customer with this name
    try:
        customer_data = waldur_client.create_customer(name=project_data.attributes.organization,
                                                      # data of a new customer
                                                      email=project_data.owner.email,
                                                      backend_id=project_data.attributes.organization,
                                                      country=pycountry.countries.get(
                                                          name=project_data.attributes.country).alpha_2,
                                                      domain=project_data.attributes.department_webpage,
                                                      homepage=project_data.attributes.department_webpage,
                                                      native_name=project_data.attributes.organization,
                                                      )
    except ValueError:
        logging.error(f'Cannot customer named {project_data.attributes.organization}.')
    else:
        logging.info(f'Customer named {project_data.attributes.organization} was created in WALDUR.')
        return customer_data


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
                offering_data = get_waldur_offering_data("3a878cee7bb749d0bb258d7b8442cb64")
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
