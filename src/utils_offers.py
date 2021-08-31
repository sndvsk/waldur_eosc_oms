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
OFFERING_URL = os.environ.get('OFFERING_URL')
WALDUR_TOKEN = os.environ.get('WALDUR_TOKEN')
OFFERING_TOKEN = os.environ.get('OFFERING_TOKEN')
PROVIDER_TOKEN = os.environ.get('PROVIDER_TOKEN')
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
        logging.error(f'Response status code: {response.status_code}')
        raise requests.exceptions.RequestException


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
    waldur_offering = waldur_offering[0]  # because of list
    eosc_offers = get_offer_list_of_resource(eosc_resource_id)['offers']
    eosc_offers_names = {offer['name'] for offer in eosc_offers}
    for plan in waldur_offering['plans']:
        if plan['name'] in eosc_offers_names:
            logging.info(f"Skipping creation of plan {plan['name']}. Offer with the same name already exists.")
            continue

        parameters = [{
            "id": "name",
            "label": "Name",
            "description": "Name will be visible in accounting",
            "type": "input",
            "value_type": "string",
            "unit": "",
        }]
        # TODO: 2. Add description field - always present, optional
        # TODO 3. input parameters from offering
        for component in waldur_offering['components']:
            if component['billing_type'] == 'limit':
                parameters.append(
                    {
                        "id": "limit " + component['type'],
                        "label": component['name'],
                        "description": component['description'] or f"Amount of {component['name']} in "
                                                                   f"{plan['name']}.",
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


def create_resource():
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'Authorization': PROVIDER_TOKEN,
    }
    id_asd = 5
    data = {
        "id": "tnp." + "nordic_test_resource_" + str(id_asd),
        "name": "test2",
        "resourceOrganisation": "tnp",
        "resourceProviders": [
            "tnp"
        ],
        "webpage": "https://example.com",
        "description": "string",
        "tagline": "string",
        "logo": "https://example.com",
        "multimedia": [
        ],
        "useCases": [
        ],
        "scientificDomains": [
            {
                "scientificDomain": "scientific_domain-agricultural_sciences",
                "scientificSubdomain": "scientific_subdomain-agricultural_sciences-agricultural_biotechnology"
            }
        ],
        "categories": [
            {
                "category": "category-aggregators_and_integrators-aggregators_and_integrators",
                "subcategory": "subcategory-aggregators_and_integrators-aggregators_and_integrators-applications"
            }
        ],
        "targetUsers": [
            "target_user-businesses"
        ],
        "accessTypes": [
        ],
        "accessModes": [
        ],
        "tags": [
        ],
        "geographicalAvailabilities": [
            "EO"
        ],
        "languageAvailabilities": [
            "en"
        ],
        "resourceGeographicLocations": [
        ],
        "mainContact": {
            "firstName": "Aleksander",
            "lastName": "Veske",
            "email": "aleksander.daniel.veske@ut.ee",
            "phone": "372",
            "position": "intern",
            "organisation": None
        },
        "publicContacts": [
            {
                "firstName": "test",
                "lastName": "test",
                "email": "test@example.com",
                "phone": "0",
                "position": None,
                "organisation": None
            }
        ],
        "helpdeskEmail": "helpdesk@example.com",
        "securityContactEmail": "security@example.com",
        "trl": "trl-1",
        "lifeCycleStatus": None,
        "certifications": [
        ],
        "standards": [
        ],
        "openSourceTechnologies": [
        ],
        "version": None,
        "lastUpdate": None,
        "changeLog": [
        ],
        "requiredResources": [
        ],
        "relatedResources": [
        ],
        "relatedPlatforms": [
        ],
        "fundingBody": [
        ],
        "fundingPrograms": [
        ],
        "grantProjectNames": [
        ],
        "helpdeskPage": None,
        "userManual": None,
        "termsOfUse": None,
        "privacyPolicy": None,
        "accessPolicy": None,
        "serviceLevel": None,
        "trainingInformation": None,
        "statusMonitoring": None,
        "maintenance": None,
        "orderType": "order_type-order_required",
        "order": None,
        "paymentModel": None,
        "pricing": None
    }
    data = json.dumps(data)
    response = requests.post(OFFERING_URL, headers=headers, data=data)
    return response


# create_resource()


# # TODO: implement sub-methods
# def is_resource_up_to_date(eosc_resource, waldur_offering):
#     return None
#
#
# def are_offers_up_to_date(osc_resource_offers, waldur_offering):
#     return None
#
#
# def update_eosc_resource(eosc_resource, waldur_offering):
#     return None
#
#
# def update_eosc_offers(eosc_resource, waldur_offering):
#     return None
#
#
# def get_or_create_eosc_resource(waldur_offering, eosc_provider_portal):
#     return None
#
#
# def get_or_create_eosc_resource_offer(waldur_offering, eosc_marketplace):
#     return None
#
#
# def get_or_create_eosc_provider(customer, eosc_provider_portal):
#     return None
#
#
# def get_waldur_offerings(deployment, token):
#
#     return None
#
#
# # TODO: implement this skeleton method
# def test(eosc_provider_portal=None, eosc_marketplace=None, deployment=None):
#     # waldur_offerings = get_waldur_offerings(deployment, token)
#     waldur_offerings = get_waldur_offerings(deployment, WALDUR_TOKEN)
#
#     for waldur_offering in waldur_offerings:
#         provider, created = get_or_create_eosc_provider(waldur_offering.customer, eosc_provider_portal)
#         if created:
#             logging.info(f'Provider has been created, pending approval')
#         if provider.is_approved:
#             eosc_resource, resource_created = get_or_create_eosc_resource(waldur_offering, eosc_provider_portal)
#             eosc_resource_offers, offer_created = get_or_create_eosc_resource_offer(waldur_offering, eosc_marketplace)
#
#         if resource_created:
#             logging.info('New resource has been created in EOSC', eosc_resource)
#         if offer_created:
#             logging.info('New offering has been created in EOSC', eosc_resource)
#
#         if not resource_created and not is_resource_up_to_date(eosc_resource, waldur_offering):
#             update_eosc_resource(eosc_resource, waldur_offering)
#         if not offer_created and not are_offers_up_to_date(eosc_resource_offers, waldur_offering):
#             update_eosc_offers(eosc_resource, waldur_offering)


def process_offerings():
    resource_list_data = get_resource_list()['resources']

    # creates offering in eosc
    # we need to add offer to project in eosc in order to successfully execute utils_orders.py

    resource_id_1 = resource_list_data[1]['id']  # hardcoded resource: Rocket (UT HPC)
    offering_data_1 = get_waldur_client().list_marketplace_offerings(
        {'name_exact': 'Rocket (UT HPC)'}
    )
    sync_offer(eosc_resource_id=resource_id_1,
               waldur_offering=offering_data_1)

    resource_id_2 = resource_list_data[0]['id']  # hardcoded resource: OpenStack VPC
    offering_data_2 = get_waldur_client().list_marketplace_offerings(
        {'name_exact': 'UT HPC (Campus)'}
    )
    sync_offer(eosc_resource_id=resource_id_2,
               waldur_offering=offering_data_2)


# process_offerings()

