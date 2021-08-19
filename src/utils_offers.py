import json
import logging
import os
import urllib.parse
import requests
from waldur_client import WaldurClient

logging.getLogger("requests").setLevel(logging.WARNING)
logging.basicConfig(level=logging.INFO, format=f'[%(asctime)s] %(filename)s:%(lineno)d %(levelname)s - '
                                               f'%(message)s')

EOSC_URL = os.environ.get('EOSC_URL')  # polling url
WALDUR_TOKEN = os.environ.get('WALDUR_TOKEN')
OFFERING_TOKEN = os.environ.get('OFFERING_TOKEN')
RESOURCE_LIST_URL = "/api/v1/resources/"
RESOURCE_URL = "/api/v1/resources/%s/"
OFFER_LIST_URL = "/api/v1/resources/%s/offers"
OFFER_URL = "/api/v1/resources/%s/offers/%s"

WALDUR_URL = os.environ.get('WALDUR_URL')
WALDUR_API = urllib.parse.urljoin(WALDUR_URL, 'api/')


def get_waldur_client():
    waldur_client = WaldurClient(WALDUR_API, WALDUR_TOKEN)
    return waldur_client


def resource_and_offering_request():
    headers = {
        'accept': 'application/json',
        'X-User-Token': OFFERING_TOKEN,
    }
    return headers


def offering_request_post_patch(offer_name: str, offer_description: str, offer_parameters, internal=True):
    headers = {
        'accept': 'application/json',
        'Content-Type': 'application/json',
        'X-User-Token': OFFERING_TOKEN,
    }
    data = {
        'name': offer_name,
        'description': offer_description,
        'order_type': 'order_required',
        'primary_oms_id': 2,
        'oms_params': {},
        'order_url': 'https://example.com/',  # plan['url'],  # "is not a valid URL"
        'internal': internal,
        'parameters': offer_parameters,
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
    if response.status_code == 200:
        return response.json()
    else:
        raise


def create_offer_for_resource(eosc_resource_id: str, offer_name: str, offer_description: str, offer_parameters,
                              internal=True):
    headers = {
        'accept': 'application/json',
        'Content-Type': 'application/json',
        'X-User-Token': OFFERING_TOKEN,
    }
    data = {
        'name': offer_name,
        'description': offer_description or "N/A",
        'order_type': 'order_required',
        'primary_oms_id': 2,
        'oms_params': {},
        'order_url': 'https://example.com/',  # plan['url'],  # "is not a valid URL"
        'internal': internal,
        'parameters': offer_parameters,
    }

    response = requests.post(urllib.parse.urljoin(EOSC_URL, OFFER_LIST_URL % eosc_resource_id),
                             headers=headers,
                             data=json.dumps(data))
    if response.status_code != 201:
        logging.error('Failed to create an offer.', response.status_code, response.text)
    else:
        logging.info(f'Successfully created offer {offer_name} for {eosc_resource_id}.')


def patch_offer_from_resource(resource_id, offer_id, waldur_offering_data, offer_description, offer_parameters):
    headers, data = offering_request_post_patch(offer_name=waldur_offering_data,
                                                offer_description=offer_description,
                                                offer_parameters=offer_parameters)
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


def _normalize_limits(limit, limit_type):
    if limit is None:
        limit = 0
        return limit
    if limit_type in ['storage', 'ram']:
        return int(limit / 1024)
    return limit


def sync_offer(eosc_resource_id, waldur_offering):
    plans = waldur_offering['plans']
    eosc_offers = get_offer_list_of_resource(eosc_resource_id)['offers']
    eosc_offers_names = {offer['name'] for offer in eosc_offers}
    for plan in plans:
        if plan['name'] in eosc_offers_names:
            logging.info(f"Skipping creation of plan {plan['name']}. Offer with the same name already exists.")
            continue
        parameters = []
        # add name

        parameters.append(
            {
                "id": "name",
                "label": "Name",
                "description": "Name will be visible in accounting",
                "type": "input",
                "value_type": "string",
                "unit": "",
            },
        )
        # TODO: 2. Add description field - always present, optional
        # TODO 3. input parameters from offering
        for component in waldur_offering['components']:
            if component['billing_type'] == 'limit':
                parameters.append(
                    {
                        "id": "limit " + component['type'],
                        "label": component['name'],
                        "description": component['description'] or f"Amount of {component['name']} in "
                                                                   f"{waldur_offering['name']}.",
                        "type": "range",
                        "value_type": "integer",  # waldur only expects numeric values for limit-type components
                        "unit": component['measured_unit'],
                        "config": {
                            "minimum": _normalize_limits(component['min_value'], component['type']),
                            "maximum": _normalize_limits(component['max_value'], component['type']),
                            "exclusiveMinimum": False,
                            "exclusiveMaximum": False
                        }
                    },
                )
            if component['billing_type'] == 'usage':
                parameters.append(
                    {
                        "id": "attributes " + component['type'],
                        "label": component['name'],
                        "description": component['description'] or f"Amount of {component['name']} in "
                                                                   f"{waldur_offering['name']}.",
                        "type": "range",
                        "value_type": "integer",  # waldur only expects numeric values for limit-type components
                        "unit": component['measured_unit'],
                        "config": {
                            "minimum": _normalize_limits(component['min_value'], component['type']),
                            "maximum": _normalize_limits(component['max_value'], component['type']),
                            "exclusiveMinimum": False,
                            "exclusiveMaximum": False
                        }
                    },
                )

        create_offer_for_resource(
            eosc_resource_id=eosc_resource_id,
            offer_name=plan['name'],
            offer_description=plan['description'],
            offer_parameters=parameters,
        )


def process_offerings():
    resource_list_data = get_resource_list()['resources']

    # creates offering in eosc
    # we need to add offer to project in eosc in order to successfully execute utils_orders.py

    resource_id_1 = resource_list_data[1]['id']  # hardcoded resource: SLURM
    offering_data_test1 = get_waldur_client()._get_offering(offering="08f5dce57d784ee88499109ca9653f02")
    sync_offer(eosc_resource_id=resource_id_1,
               waldur_offering=offering_data_test1)

    # resource_id_2 = resource_list_data[0]['id']  # hardcoded resource: OpenStack VPC
    # offering_data_test2 = get_waldur_client()._get_offering(offering="4ce883470b7242beb7368becf614d1ec")
    # sync_offer(eosc_resource_id=resource_id_2,
    #            waldur_offering=offering_data_test2)


# process_offerings()
