import datetime
import unittest
from unittest.mock import Mock
import waldur_client
from oms_jira.services.mp import MPClient

from src import utils_orders
from src.utils_orders import get_or_create_project, create_order, process_orders, get_events, get_new_events
from . import MOCK_LIST_PROJECTS_1, EOSC_PROJECT_DATA_1, WALDUR_ORGANIZATION_DATA_1, MOCK_CREATE_PROJECT_1, \
    MOCK_CREATE_MARKETPLACE_ORDER_3, MOCK_OFFERING_DATA_3, WALDUR_PROJECT_DATA_3, EOSC_PROJECT_ITEM_DATA_3, EVENTS_4, \
    MOCK_WALDUR_ORGANIZATION_4, MOCK_LIST_PROJECTS_4, MOCK_WALDUR_OFFERING_4, MOCK_CREATE_PROJECT_4,\
    MOCK_GET_EVENTS_6, MOCK_GET_EVENTS_7, EXPECTED_EVENTS_7


class TestOrders(unittest.TestCase):
    # without create_project()
    def test_get_or_create_project_first(self):
        mock_list_projects = Mock()
        waldur_client.WaldurClient.list_projects = mock_list_projects
        mock_list_projects.return_value = MOCK_LIST_PROJECTS_1

        eosc_project_data = EOSC_PROJECT_DATA_1

        waldur_organization_data = WALDUR_ORGANIZATION_DATA_1

        mock_create_project = Mock()
        waldur_client.WaldurClient.create_project = mock_create_project
        mock_create_project.return_value = MOCK_CREATE_PROJECT_1

        result = get_or_create_project(eosc_project_data=eosc_project_data,
                                       waldur_organization_data=waldur_organization_data)

        self.assertEqual(mock_create_project.return_value,
                         result)

        mock_list_projects.assert_called_once()

    # with create_project()
    def test_get_or_create_project_second(self):
        mock_list_projects = Mock()
        waldur_client.WaldurClient.list_projects = mock_list_projects
        mock_list_projects.return_value = []

        eosc_project_data = EOSC_PROJECT_DATA_1

        waldur_organization_data = WALDUR_ORGANIZATION_DATA_1

        mock_create_project = Mock()
        waldur_client.WaldurClient.create_project = mock_create_project
        mock_create_project.return_value = MOCK_CREATE_PROJECT_1

        mock_invite_client = Mock()
        waldur_client.WaldurClient.create_project_invitation = mock_invite_client
        mock_invite_client.return_value = {}

        result = get_or_create_project(eosc_project_data=eosc_project_data,
                                       waldur_organization_data=waldur_organization_data)

        self.assertEqual(mock_create_project.return_value, result)

        mock_create_project.assert_called_once()

    def test_create_order(self):
        mock_create_marketplace_order = Mock()
        waldur_client.WaldurClient.create_marketplace_order = mock_create_marketplace_order
        mock_create_marketplace_order.return_value = MOCK_CREATE_MARKETPLACE_ORDER_3

        mock_post_message = Mock()
        MPClient.post = mock_post_message
        mock_post_message.return_value = {}

        waldur_offering_data = MOCK_OFFERING_DATA_3

        waldur_project_data = WALDUR_PROJECT_DATA_3
        eosc_project_item_data = EOSC_PROJECT_ITEM_DATA_3

        result = create_order(waldur_offering_data=waldur_offering_data[0],
                              waldur_project_data_for_order=waldur_project_data,
                              eosc_project_item_data=eosc_project_item_data)

        self.assertEqual(mock_create_marketplace_order.return_value, result)

        mock_create_marketplace_order.assert_called_once()

    # without create_project()
    def test_process_orders_first(self):
        events = EVENTS_4

        mock_get_events = Mock()
        utils_orders.get_events = mock_get_events
        mock_get_events.return_value = events

        mock_waldur_organization = Mock()
        utils_orders.get_target_waldur_organization = mock_waldur_organization
        mock_waldur_organization.return_value = MOCK_WALDUR_ORGANIZATION_4

        mock_waldur_offering_data = Mock()
        waldur_client.WaldurClient.list_marketplace_offerings = mock_waldur_offering_data
        mock_waldur_offering_data.return_value = MOCK_WALDUR_OFFERING_4

        mock_list_projects = Mock()
        waldur_client.WaldurClient.list_projects = mock_list_projects
        mock_list_projects.return_value = MOCK_LIST_PROJECTS_4

        mock_invite_client = Mock()
        waldur_client.WaldurClient.create_project_invitation = mock_invite_client
        mock_invite_client.return_value = {}

        mock_create_marketplace_order = Mock()
        waldur_client.WaldurClient.create_marketplace_order = mock_create_marketplace_order
        mock_create_marketplace_order.return_value = {}

        mock_post_message = Mock()
        MPClient.post = mock_post_message
        mock_post_message.return_value = {}

        process_orders()
        mock_create_marketplace_order.assert_called_once()

    # with create_project()
    def test_process_orders_second(self):
        events = EVENTS_4

        mock_get_events = Mock()
        utils_orders.get_events = mock_get_events
        mock_get_events.return_value = events

        mock_waldur_organization = Mock()
        utils_orders.get_target_waldur_organization = mock_waldur_organization
        mock_waldur_organization.return_value = MOCK_WALDUR_ORGANIZATION_4

        mock_waldur_offering_data = Mock()
        waldur_client.WaldurClient.list_marketplace_offerings = mock_waldur_offering_data
        mock_waldur_offering_data.return_value = MOCK_WALDUR_OFFERING_4

        mock_list_projects = Mock()
        waldur_client.WaldurClient.list_projects = mock_list_projects
        mock_list_projects.return_value = []

        mock_create_project = Mock()
        waldur_client.WaldurClient.create_project = mock_create_project
        mock_create_project.return_value = MOCK_CREATE_PROJECT_4

        mock_invite_client = Mock()
        waldur_client.WaldurClient.create_project_invitation = mock_invite_client
        mock_invite_client.return_value = {}

        mock_create_marketplace_order = Mock()
        waldur_client.WaldurClient.create_marketplace_order = mock_create_marketplace_order
        mock_create_marketplace_order.return_value = {}

        mock_post_message = Mock()
        MPClient.post = mock_post_message
        mock_post_message.return_value = {}

        process_orders()
        mock_create_project.assert_called_once()
        mock_create_marketplace_order.assert_called_once()

    def test_get_events(self):
        mock_get_events = Mock()
        utils_orders.get_events = mock_get_events
        mock_get_events.return_value = MOCK_GET_EVENTS_6

        events = get_events("2021-09-28 10:57:00.000000")

        self.assertEqual(mock_get_events.return_value,
                         events)

    def test_new_events(self):
        mock_get_events = Mock()
        utils_orders.get_events = mock_get_events
        mock_get_events.return_value = MOCK_GET_EVENTS_7

        expected_events = EXPECTED_EVENTS_7

        new_events = get_new_events(events=mock_get_events.return_value,
                                    time_now=datetime.datetime(2021, 9, 28, 10, 57, 28))

        self.assertEqual(new_events, expected_events)


if __name__ == '__main__':
    unittest.main()
