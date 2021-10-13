import datetime
import unittest
from unittest.mock import Mock
import waldur_client
from oms_jira.services.mp import ProjectOwner, ProjectAttributes, MPProject, MPClient, ProjectItemAttributes, \
    MPProjectItem, Event

from src import utils_orders
from src.utils_orders import get_or_create_project, create_order, process_orders, get_events


class MyTestCase(unittest.TestCase):
    def test_get_or_create_project_first(self):
        mock_list_projects = Mock()
        waldur_client.WaldurClient.list_projects = mock_list_projects
        mock_list_projects.return_value = [{'url': 'project_url',
                                            'uuid': 'project_uuid',
                                            'name': 'TEST4',
                                            'customer': 'customer_url',
                                            'customer_uuid': 'customer_uuid',
                                            'customer_name': 'Test4all',
                                            'customer_native_name': '',
                                            'customer_abbreviation': '',
                                            'description': '',
                                            'created': '2021-08-16T11:44:22.851786Z',
                                            'type': None,
                                            'backend_id': '1452',
                                            'end_date': None,
                                            'oecd_fos_2007_code': None,
                                            'billing_price_estimate': {'total': 0.0,
                                                                       'current': 0,
                                                                       'tax': 0,
                                                                       'tax_current': 0}}]

        eosc_project_data = MPProject(id=1452, owner=ProjectOwner(
            uid='owner@aai.eosc-portal.eu',
            email='owner@ut.ee', name='OWNER'), project_items=[1, 2, 3],
                                      attributes=ProjectAttributes(name='TEST4',
                                                                   customer_typology='single_user',
                                                                   organization='ETAIS',
                                                                   department='backend',
                                                                   department_webpage='https://etais.ee/',
                                                                   scientific_domains=[
                                                                       'Economics & Business'],
                                                                   country='Estonia',
                                                                   collaboration_countries=[],
                                                                   user_group_name=''))

        waldur_organization_data = [{
            'url': 'customer_url',
            'uuid': 'customer_uuid',
            'created': '2017-03-21T07:24:34.090847Z',
            'division': 'customer_division',
            'division_name': 'Tests',
            'division_uuid': 'customer_division_uuid',
            'division_type_name': 'Department',
            'division_type_uuid': 'customer_division_type_uuid',
            'display_name': 'Test4all',
            'projects': [
                {'url': 'project_url',
                 'uuid': 'project_uuid',
                 'name': 'TEST4'}],
            'owners': [
                {'url': 'owner_url',
                 'uuid': 'owner_uuid',
                 'username': 'owner@ut.ee',
                 'full_name': 'OWNER',
                 'native_name': ''}
            ],
            'support_users': [],
            'service_managers': [],
            'backend_id': '',
            'image': None,
            'default_tax_percent': '0.00',
            'accounting_start_date': '2018-02-11T22:52:29.951974Z',
            'name': 'Test4all',
            'native_name': '',
            'abbreviation': '',
            'contact_details': '',
            'agreement_number': None,
            'email': '',
            'phone_number': '',
            'access_subnets': '',
            'registration_code': '',
            'homepage': '',
            'domain': '',
            'vat_code': '',
            'postal': '',
            'address': '',
            'bank_name': '',
            'bank_account': '',
            'latitude': None,
            'longitude': None,
            'country': '',
            'payment_profiles': [],
            'is_service_provider': False,
            'billing_price_estimate': {'total': 0.0, 'current': 0, 'tax': 0, 'tax_current': 0}
        }]

        mock_create_project = Mock()
        waldur_client.WaldurClient.create_project = mock_create_project
        mock_create_project.return_value = {
            'url': 'project_url',
            'uuid': 'project_uuid',
            'name': 'TEST4',
            'customer': 'customer_url',
            'customer_uuid': 'customer_uuid',
            'customer_name': 'Test4all',
            'customer_native_name': '',
            'customer_abbreviation': '',
            'description': '',
            'created': '2021-08-16T11:44:22.851786Z',
            'type': None,
            'backend_id': '1452',
            'end_date': None,
            'oecd_fos_2007_code': None,
            'billing_price_estimate': {'total': 0.0,
                                       'current': 0,
                                       'tax': 0,
                                       'tax_current': 0}}

        get_or_create_project(eosc_project_data=eosc_project_data,
                              waldur_organization_data=waldur_organization_data)

        mock_list_projects.assert_called_once()

    def test_get_or_create_project_second(self):
        mock_list_projects = Mock()
        waldur_client.WaldurClient.list_projects = mock_list_projects
        mock_list_projects.return_value = []

        eosc_project_data = MPProject(id=1452, owner=ProjectOwner(
            uid='owner@aai.eosc-portal.eu',
            email='owner@ut.ee', name='OWNER'), project_items=[1, 2, 3],
                                      attributes=ProjectAttributes(name='TEST4',
                                                                   customer_typology='single_user',
                                                                   organization='ETAIS',
                                                                   department='backend',
                                                                   department_webpage='https://etais.ee/',
                                                                   scientific_domains=[
                                                                       'Economics & Business'],
                                                                   country='Estonia',
                                                                   collaboration_countries=[],
                                                                   user_group_name=''))

        waldur_organization_data = [{
            'url': 'customer_url',
            'uuid': 'customer_uuid',
            'created': '2017-03-21T07:24:34.090847Z',
            'division': 'customer_division',
            'division_name': 'Tests',
            'division_uuid': 'customer_division_uuid',
            'division_type_name': 'Department',
            'division_type_uuid': 'customer_division_type_uuid',
            'display_name': 'Test4all',
            'projects': [
                {'url': 'project_url',
                 'uuid': 'project_uuid',
                 'name': 'TEST4'}],
            'owners': [
                {'url': 'owner_url',
                 'uuid': 'owner_uuid',
                 'username': 'owner@ut.ee',
                 'full_name': 'OWNER',
                 'native_name': ''}
            ],
            'support_users': [],
            'service_managers': [],
            'backend_id': '',
            'image': None,
            'default_tax_percent': '0.00',
            'accounting_start_date': '2018-02-11T22:52:29.951974Z',
            'name': 'Test4all',
            'native_name': '',
            'abbreviation': '',
            'contact_details': '',
            'agreement_number': None,
            'email': '',
            'phone_number': '',
            'access_subnets': '',
            'registration_code': '',
            'homepage': '',
            'domain': '',
            'vat_code': '',
            'postal': '',
            'address': '',
            'bank_name': '',
            'bank_account': '',
            'latitude': None,
            'longitude': None,
            'country': '',
            'payment_profiles': [],
            'is_service_provider': False,
            'billing_price_estimate': {'total': 0.0, 'current': 0, 'tax': 0, 'tax_current': 0}
        }]

        mock_create_project = Mock()
        waldur_client.WaldurClient.create_project = mock_create_project
        mock_create_project.return_value = {
            'url': 'project_url',
            'uuid': 'project_uuid',
            'name': 'TEST4',
            'customer': 'customer_url',
            'customer_uuid': 'customer_uuid',
            'customer_name': 'Test4all',
            'customer_native_name': '',
            'customer_abbreviation': '',
            'description': '',
            'created': '2021-08-16T11:44:22.851786Z',
            'type': None,
            'backend_id': '1452',
            'end_date': None,
            'oecd_fos_2007_code': None,
            'billing_price_estimate': {'total': 0.0,
                                       'current': 0,
                                       'tax': 0,
                                       'tax_current': 0}}

        mock_invite_client = Mock()
        waldur_client.WaldurClient.create_project_invitation = mock_invite_client
        mock_invite_client.return_value = {}

        get_or_create_project(eosc_project_data=eosc_project_data,
                              waldur_organization_data=waldur_organization_data)

        mock_create_project.assert_called_once()

    def test_create_order(self):
        mock_create_marketplace_order = Mock()
        waldur_client.WaldurClient.create_marketplace_order = mock_create_marketplace_order
        mock_create_marketplace_order.return_value = {}

        mock_post_message = Mock()
        MPClient.post = mock_post_message
        mock_post_message.return_value = {}

        waldur_offering_data = [
            {'url': 'offering_url',
             'uuid': 'offering_uuid',
             'created': '2019-05-03T12:03:13.531473Z',
             'name': 'service',
             'description': 'sample',
             'full_description': '',
             'terms_of_service': '',
             'terms_of_service_link': '',
             'privacy_policy_link': '',
             'customer': 'customer_url',
             'customer_uuid': 'customer_uuid',
             'customer_name': 'ETAIS',
             'category': 'category_url',
             'category_uuid': 'category_uuid',
             'category_title': 'Private clouds',
             'rating': None,
             'attributes': {'vpc_Support_email': 'support@hpc.ut.ee',
                            'vpc_Security_certification': ['vpc_Security_certification_iskem']
                            },
             'options': {'order': [],
                         'options': {}
                         },
             'components': [
                 {'billing_type': 'limit',
                  'type': 'cores',
                  'name': 'Cores',
                  'description': '',
                  'measured_unit': 'cores',
                  'limit_period': None,
                  'limit_amount': None,
                  'article_code': '',
                  'max_value': 10,
                  'min_value': 1,
                  'is_boolean': False,
                  'default_limit': None,
                  'factor': 1,
                  'is_builtin': True},
             ],
             'plugin_options': {'storage_mode': 'fixed'},
             'state': 'Active',
             'native_name': '',
             'native_description': '',
             'vendor_details': '',
             'thumbnail': 'thumbnail_url',
             'order_item_count': 804.0,
             'plans': [
                 {'url': 'plan_url',
                  'uuid': 'plan_uuid',
                  'name': 'plan_name',
                  'description': '',
                  'article_code': '',
                  'prices': {'cores': 0.1,
                             'ram': 0.1,
                             'storage': 0.1},
                  'quotas': {'cores': 0,
                             'ram': 0,
                             'storage': 0},
                  'max_amount': None,
                  'archived': False,
                  'is_active': True,
                  'unit_price': '0.0000000',
                  'unit': 'day',
                  'init_price': 0,
                  'switch_price': 0,
                  'backend_id': '',
                  'plan_type': 'limit',
                  'minimal_price': 0.0}
             ],
             'screenshots': [],
             'type': 'Packages.Template',
             'shared': True,
             'billable': True,
             'scope': 'scoper_url',
             'scope_uuid': 'scope_uuid',
             'files': [],
             'quotas': [
                 {'url': 'quota_url',
                  'uuid': 'quota_uuid',
                  'name': 'quota_name',
                  'limit': -1.0,
                  'usage': 0.0}
             ],
             'paused_reason': '',
             'datacite_doi': '',
             'citation_count': -1,
             'latitude': 1.1,
             'longitude': 1.1,
             'backend_id': '',
             'divisions': [],
             'image': None,
             'google_calendar_is_public': None,
             'google_calendar_link': None}
        ]

        waldur_project_data = {'url': 'project_url',
                               'uuid': 'project_uuid',
                               'name': 'project_name',
                               'customer': 'customer_name',
                               'customer_uuid': 'customer_uuid',
                               'customer_name': 'customer_name',
                               'customer_native_name': '',
                               'customer_abbreviation': '',
                               'description': '',
                               'created': '2021-08-16T11:38:29.677204Z',
                               'type': None,
                               'backend_id': '1449',
                               'end_date': None,
                               'oecd_fos_2007_code': None,
                               'billing_price_estimate': {'total': 0.0,
                                                          'current': 0,
                                                          'tax': 0,
                                                          'tax_current': 0}
                               }
        eosc_project_item_data = MPProjectItem(id=3,
                                               project_id=1449,
                                               status=MPProjectItem.Status(value='registered',
                                                                           type='registered'),
                                               attributes=ProjectItemAttributes(category='Applications',
                                                                                service='service',
                                                                                offer='plan_name',
                                                                                offer_properties=[
                                                                                    {'id': 'name',
                                                                                     'type': 'input',
                                                                                     'unit': '',
                                                                                     'label': 'Name',
                                                                                     'value': 'my offer',
                                                                                     'value_type': 'string',
                                                                                     'description': 'sample'}
                                                                                ],
                                                                                platforms=[],
                                                                                request_voucher=False,
                                                                                order_type='order_required'),
                                               user_secrets={})

        create_order(waldur_offering_data=waldur_offering_data[0],
                     waldur_project_data_for_order=waldur_project_data,
                     eosc_project_item_data=eosc_project_item_data)

        mock_create_marketplace_order.assert_called_once()

    def test_get_events(self):
        get_events("2021-08-19 12:00:00.000000")


if __name__ == '__main__':
    unittest.main()
