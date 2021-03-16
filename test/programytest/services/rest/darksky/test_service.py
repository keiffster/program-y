import unittest
from unittest.mock import patch
from unittest.mock import Mock
import os
from programy.services.rest.darksky.service import DarkSkyService
from programy.services.rest.geonames.service import GeoNamesService
from programy.services.config import ServiceConfiguration
from programytest.services.testclient import ServiceTestClient
from programytest.services.testcase import ServiceTestCase
from programytest.externals import integration_tests_active, integration_tests_disabled
from programytest.services.rest.darksky.responses import forecast_success_response
from programytest.services.rest.darksky.responses import timemachine_success_response
from programytest.services.rest.geonames.responses import postcode_success_response
import logging


class DarkSkyServiceTestClient(ServiceTestClient):

    def __init__(self):
        ServiceTestClient.__init__(self, debug=True, level=logging.DEBUG)

    def load_storage(self):
        super(DarkSkyServiceTestClient, self).load_storage()
        self.add_license_keys_store(self.get_license_key_file())


class DarkSkyServiceTests(ServiceTestCase):

    def test_init(self):
        service = DarkSkyService(ServiceConfiguration.from_data("rest", "darksky", "weather"))
        self.assertIsNotNone(service)

    def patch_requests_forecast_success_response(self, url, headers, timeout):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = forecast_success_response
        return mock_response

    def patch_requests_timemachine_success_response(self, url, headers, timeout):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = timemachine_success_response
        return mock_response

    def _do_forecast(self):
        service = DarkSkyService(ServiceConfiguration.from_data("rest", "darksky", "weather"))
        self.assertIsNotNone(service)

        client = DarkSkyServiceTestClient()
        service.initialise(client)

        response = service.forecast(56.0712, -3.1743)
        self.assertResponse(response, 'forecast', 'darksky', 'weather')

    @unittest.skipIf(integration_tests_active() is False, integration_tests_disabled)
    def test_forecast_integration(self):
        self._do_forecast()

    @patch("programy.services.rest.base.RESTService._requests_get", patch_requests_forecast_success_response)
    def test_forecast_unit(self):
        self._do_forecast()

    def _do_timemachine(self):
        service = DarkSkyService(ServiceConfiguration.from_data("rest", "darksky", "weather"))
        self.assertIsNotNone(service)

        client = DarkSkyServiceTestClient()
        service.initialise(client)

        response = service.timemachine(56.0712, -3.1743, "255657600")
        self.assertResponse(response, 'timemachine', 'darksky', 'weather')

    @unittest.skipIf(integration_tests_active() is False, integration_tests_disabled)
    def test_timemachine_integration(self):
        self._do_timemachine()

    @patch("programy.services.rest.base.RESTService._requests_get", patch_requests_timemachine_success_response)
    def test_timemachine_unit(self):
        self._do_timemachine()

    @patch("programy.services.rest.base.RESTService._requests_get", patch_requests_forecast_success_response)
    def test_forecast_aiml(self):
        client = DarkSkyServiceTestClient()
        conf_file = DarkSkyService.get_default_conf_file()

        response = self._do_handler_load(client, conf_file, "darksky", "DARKSKY FORECAST LAT SIGN POS DEC 56 FRAC 0712 LNG SIGN NEG DEC 3 FRAC 1743")
        self.assertIsNotNone(response)
        self.assertEqual("It is currently clear.", response)

    def patch_requests_postcode_success_response(self, url, headers, timeout):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = postcode_success_response
        return mock_response

    @unittest.skipIf(integration_tests_active() is False, integration_tests_disabled)
    def test_forecast_postcode_aiml(self):
        client = DarkSkyServiceTestClient()
        client_context = client.create_client_context("testuser")

        self._load_conf_file(client_context, DarkSkyService.get_default_conf_file())
        self.assertTrue("darksky" in client_context.brain.service_handler.services)
        self._load_conf_file(client_context, GeoNamesService.get_default_conf_file())
        self.assertTrue("geonames" in client_context.brain.service_handler.services)

        response = client_context.bot.ask_question(client_context, "DARKSKY FORECAST POSTCODE KY39UR")
        self.assertIsNotNone(response)
        self.assertTrue(response.startswith("It is currently"))

    @unittest.skipIf(integration_tests_active() is False, integration_tests_disabled)
    def test_timemachine_postcode_aiml(self):
        client = DarkSkyServiceTestClient()
        client_context = client.create_client_context("testuser")

        self._load_conf_file(client_context, DarkSkyService.get_default_conf_file())
        self.assertTrue("darksky" in client_context.brain.service_handler.services)
        self._load_conf_file(client_context, GeoNamesService.get_default_conf_file())
        self.assertTrue("geonames" in client_context.brain.service_handler.services)

        response = client_context.bot.ask_question(client_context, "DARKSKY TIMEMACHINE POSTCODE KY39UR TIME 255657600")
        self.assertIsNotNone(response)
        self.assertTrue(response.startswith("It was"))
