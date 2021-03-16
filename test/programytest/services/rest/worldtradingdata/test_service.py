import unittest
from unittest.mock import patch
from unittest.mock import Mock
import os
from programy.services.rest.worldtradingdata.service import WorldTradingDataStocksService
from programy.services.config import ServiceConfiguration
from programy.services.config import ServiceRESTConfiguration
from programytest.services.testclient import ServiceTestClient
from programytest.services.testcase import ServiceTestCase
from programytest.externals import integration_tests_active, integration_tests_disabled
from programytest.services.rest.worldtradingdata.responses import stocks_success_response


class WorldTradingDataServiceTestClient(ServiceTestClient):

    def __init__(self):
        ServiceTestClient.__init__(self, debug=True)

    def load_storage(self):
        super(WorldTradingDataServiceTestClient, self).load_storage()
        self.add_license_keys_store(self.get_license_key_file())


class WorldTradingDataStocksServiceTests(ServiceTestCase):

    def test_init(self):
        service = WorldTradingDataStocksService(ServiceConfiguration.from_data("rest", "worldtradingdata", "stockmarket"))
        self.assertIsNotNone(service)

    def patch_requests_stocks_success(self, url, headers, timeout):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.text = stocks_success_response
        return mock_response

    def _do_stocks(self):
        service = WorldTradingDataStocksService(ServiceConfiguration.from_data("rest", "worldtradingdata", "stockmarket"))

        self.assertIsNotNone(service)

        client = WorldTradingDataServiceTestClient()
        service.initialise(client)

        response = service.stocks("AAPL")
        self.assertResponse(response, 'stocks', "worldtradingdata", "stockmarket")

    @unittest.skipIf(integration_tests_active() is False, integration_tests_disabled)
    def test_stocks_integration(self):
        self._do_stocks()

    @patch("programy.services.rest.base.RESTService._requests_get", patch_requests_stocks_success)
    def test_stocks_unit(self):
        self._do_stocks()

    @patch("programy.services.rest.base.RESTService._requests_get", patch_requests_stocks_success)
    def test_handler_load(self):
        client = WorldTradingDataServiceTestClient()
        conf_file = WorldTradingDataStocksService.get_default_conf_file()

        response = self._do_handler_load(client, conf_file, "worldtradingdata", "WORLDTRADINGDATA SYMBOLS AMZN")
        self.assertIsNotNone(response)
        self.assertEqual("Apple Inc. [ AAPL ] is currently priced at 318.85 USD.", response)