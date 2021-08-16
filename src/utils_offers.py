import json
import logging
import os
import re
import urllib.parse
import requests

from src.utils_orders import EOSC_URL, get_waldur_offering_data


logging.getLogger("requests").setLevel(logging.WARNING)
logging.basicConfig(level=logging.INFO, format=f'[%(asctime)s] %(filename)s:%(lineno)d %(levelname)s - '
                                               f'%(message)s')


OFFERING_TOKEN = os.environ.get('OFFERING_TOKEN')
RESOURCE_LIST_URL = "/api/v1/resources/"
RESOURCE_URL = "/api/v1/resources/%s/"
OFFER_LIST_URL = "/api/v1/resources/%s/offers"
OFFER_URL = "/api/v1/resources/%s/offers/%s"


def resource_and_offering_request():
    headers = {
        'accept': 'application/json',
        'X-User-Token': OFFERING_TOKEN,
    }
    return headers


def offer_parameters(parameter_type, waldur_offering_data, plan, internal=True):
    full_data = []
    if parameter_type == 'attribute':
        full_data.append({
            "id": plan['uuid'],
            "label": plan['article_code'],  # plan['article_code'],    # "can't be blank"
            "description": re.sub('<[^<]+?>', '', plan['description']),  # plan['description'],   # "can't be blank"
            "type": parameter_type,
            "value": str(int(float(plan['unit_price']))),
            "value_type": "string"
        })
    if parameter_type == 'input':
        full_data.append({
            "id": plan['uuid'],
            "label": plan['article_code'],  # "can't be blank"
            "description": re.sub('<[^<]+?>', '', plan['description']),  # "can't be blank"
            "type": parameter_type,
            "unit": plan['unit'],
            "value_type": "string"
        })
    if parameter_type == 'select':
        full_data.append({
            "id": plan['uuid'],
            "label": plan['article_code'],  # "can't be blank"
            "description": re.sub('<[^<]+?>', '', plan['description']),  # "can't be blank"
            "type": parameter_type,
            "config": {
                "values": [
                ],
                "mode": "dropdown"
            },
            "value_type": "string",
            "unit": plan['unit']
        })
        for i in waldur_offering_data['components']:
            full_data[0]['config']['values'].append(i['name'])
    if parameter_type == 'multiselect':
        full_data.append({
            "id": plan['uuid'],
            "label": plan['article_code'],  # "can't be blank"
            "description": re.sub('<[^<]+?>', '', plan['description']),  # "can't be blank"
            "type": parameter_type,
            "config": {
                "values": [
                ],
                "minItems": len(waldur_offering_data['components']),
                "maxItems": len(waldur_offering_data['components'])
            },
            "value_type": "string",
            "unit": plan['unit']
        })
        for i in waldur_offering_data['components']:
            full_data[0]['config']['values'].append(i['name'])
    if parameter_type == 'date':
        full_data.append({
            "id": plan['uuid'],
            "label": plan['article_code'],  # "can't be blank"
            "description": re.sub('<[^<]+?>', '', plan['description']),  # "can't be blank"
            "type": parameter_type,
            "value_type": "string"
        })
    if parameter_type == 'range':
        full_data.append({
            "id": plan['uuid'],
            "label": plan['article_code'],  # "can't be blank"
            "description": re.sub('<[^<]+?>', '', plan['description']),  # "can't be blank"
            "type": parameter_type,
            "unit": plan['unit'],
            "value_type": "integer",
            "config": {
                "minimum": 0,
                "maximum": plan['max_amount'],
                "exclusiveMinimum": internal,
                "exclusiveMaximum": internal
            }
        })
    if parameter_type == 'quantity_price':
        full_data.append({
            "id": plan['uuid'],
            "label": plan['article_code'],  # "can't be blank"
            "description": re.sub('<[^<]+?>', '', plan['description']),  # "can't be blank"
            "type": parameter_type,
            "unit": plan['unit'],
            "value_type": "integer",
            "config": {
                "start_price": plan['init_price'],
                "step_price": plan['switch_price'],
                "max": plan['max_amount'],
                "currency": "Euro"
            }
        })
    return full_data


def offering_request_post_patch(waldur_offering_data, plan, parameter_type, internal=True):
    headers = {
        'accept': 'application/json',
        'Content-Type': 'application/json',
        'X-User-Token': OFFERING_TOKEN,
    }
    data = {
        'name': plan['name'],
        'description': re.sub('<[^<]+?>', '', plan['description']),  # plan['description'],  # "can't be blank"
        'order_type': 'order_required',
        'primary_oms_id': 2,
        'oms_params': {},
        'order_url': 'https://example.com/',  # plan['url'],  # "is not a valid URL"
        'internal': internal,
        'parameters': offer_parameters(parameter_type=parameter_type,
                                       waldur_offering_data=waldur_offering_data,
                                       plan=plan),
    }
    return headers, data


def offering_request_delete():
    headers = {
        'accept': '*/*',
        'X-User-Token': OFFERING_TOKEN,
    }
    return headers


def get_resource_list():
    headers = resource_and_offering_request()
    response = requests.get(urllib.parse.urljoin(EOSC_URL, RESOURCE_LIST_URL),
                            headers=headers)
    resource_list_data = json.loads(response.text)
    return resource_list_data


def get_resource(resource_id):
    headers = resource_and_offering_request()
    response = requests.get(urllib.parse.urljoin(EOSC_URL, RESOURCE_URL % (str(resource_id))),
                            headers=headers)
    resource_data = json.loads(response.text)
    return resource_data


def get_offer_list_of_resource(resource_id):
    headers = resource_and_offering_request()
    response = requests.get(urllib.parse.urljoin(EOSC_URL, OFFER_LIST_URL % (str(resource_id))),
                            headers=headers)
    offer_list_data = json.loads(response.text)
    return offer_list_data


def create_offer_for_resource(resource_id, waldur_offering_data, parameter_type, plan):
    headers, data = offering_request_post_patch(waldur_offering_data=waldur_offering_data,
                                                parameter_type=parameter_type,
                                                plan=plan)

    response = requests.post(urllib.parse.urljoin(EOSC_URL, OFFER_LIST_URL % (str(resource_id))),
                             headers=headers,
                             data=json.dumps(data))
    offer_post_data = json.loads(response.request.body)
    return offer_post_data


def get_offer_from_resource(resource_id, offer_id):
    headers = resource_and_offering_request()
    response = requests.post(urllib.parse.urljoin(EOSC_URL, OFFER_URL % (str(resource_id), str(offer_id))),
                             headers=headers)
    offer_data = json.loads(response.text)
    print(offer_data)
    return offer_data


def patch_offer_from_resource(resource_id, offer_id, waldur_offering_data, parameter_type, plan):
    headers, data = offering_request_post_patch(waldur_offering_data=waldur_offering_data,
                                                parameter_type=parameter_type,
                                                plan=plan)
    response = requests.patch(urllib.parse.urljoin(EOSC_URL, OFFER_URL % (str(resource_id), str(offer_id))),
                              headers=headers,
                              data=data)
    patch_offer_data = json.loads(response.text)
    return patch_offer_data


def delete_offer_from_resource(resource_id, offer_id):
    headers = offering_request_delete()
    response = requests.delete(urllib.parse.urljoin(EOSC_URL, OFFER_URL % (str(resource_id), str(offer_id))),
                               headers=headers)
    delete_offer_data = json.loads(response.text)
    return delete_offer_data


def get_or_create_offer(resource_id, offering_data, parameter_type):
    off_list = get_offer_list_of_resource(resource_id)
    waldur_offer_list = []
    for offer in offering_data['plans']:
        waldur_offer_list.append(offer['uuid'])
    if len(off_list['offers']) == 0:
        for offering_plan in offering_data['plans']:
            create_offer_for_resource(resource_id=resource_id,
                                      waldur_offering_data=offering_data,
                                      parameter_type=parameter_type,
                                      plan=offering_plan)
    else:
        for eosc_offer in off_list['offers']:
            if eosc_offer['parameters'][0]['id'] in waldur_offer_list:
                pass


def process_offerings():
    resource_list_data = get_resource_list()['resources']
    resource_id_1 = resource_list_data[1]['id']  # hardcoded resource: Nordic Test Resource 1
    resource_id_2 = resource_list_data[0]['id']  # hardcoded resource: Nordic Test Resource 2
    offering_data_test1 = get_waldur_offering_data("3a878cee7bb749d0bb258d7b8442cb64")
    offering_data_test2 = get_waldur_offering_data("5162bd1a4dc146bfa8576d62cca49e43")
    get_or_create_offer(resource_id=resource_id_1, offering_data=offering_data_test1,
                        parameter_type=re.sub('<[^<]+?>', '', offering_data_test1['plans'][0]['description']))
    get_or_create_offer(resource_id=resource_id_2,
                        offering_data=offering_data_test2,
                        parameter_type=re.sub('<[^<]+?>', '', offering_data_test2['plans'][0]['description']))
