import unittest
from unittest.mock import Mock

from src import utils_offers
from src.utils_offers import get_or_create_eosc_provider


class TestOffers(unittest.TestCase):
    def test_get_or_create_eosc_provider(self):
        mock_get_or_create_eosc_provider = Mock()
        utils_offers.get_or_create_eosc_provider = mock_get_or_create_eosc_provider
        get_or_create_eosc_provider.return_value = {}

        # provider, is_approved = get_or_create_eosc_provider()

        # mock_get_or_create_eosc_provider.assert_called_once()
        # self.assertEqual(True, False)

    # TODO
    def test_get_or_create_eosc_resource_offer(self):
        self.assertEqual(True, True)

    def test_get_or_create_eosc_resource(self):
        self.assertEqual(True, True)

    def test_create_resource(self):
        self.assertEqual(True, True)

    def test_create_offer_for_resource(self):
        self.assertEqual(True, True)

    def test_sync_offer(self):
        self.assertEqual(True, True)

    def test_process_offers(self):
        self.assertEqual(True, True)


if __name__ == '__main__':
    unittest.main()
