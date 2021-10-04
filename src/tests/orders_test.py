import unittest
from unittest.mock import Mock
import waldur_client
from oms_jira.services.mp import ProjectOwner, ProjectAttributes, MPProject
from src.utils_orders import get_or_create_project


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
        create_project_data = mock_create_project.return_value

        mock_invite_client = Mock()
        waldur_client.WaldurClient.create_project_invitation = mock_invite_client
        mock_invite_client.return_value = {}

        get_or_create_project(eosc_project_data=eosc_project_data,
                              waldur_organization_data=waldur_organization_data)

        mock_create_project.assert_called_once()


if __name__ == '__main__':
    unittest.main()
