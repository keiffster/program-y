import unittest
from unittest.mock import patch
from unittest.mock import Mock
import os
from programy.services.rest.accuweather.service import AccuWeatherService
from programy.services.config import ServiceConfiguration
from programy.services.config import ServiceRESTConfiguration
from programytest.externals import integration_tests_active, integration_tests_disabled
from programytest.services.testclient import ServiceTestClient
from programytest.services.testcase import ServiceTestCase
from programytest.services.rest.accuweather.responses import postcodesearch_success_response
from programytest.services.rest.accuweather.responses import textsearch_success_response
from programytest.services.rest.accuweather.responses import conditions_success_response


class AccuWeatherServiceTestClient(ServiceTestClient):

    def __init__(self):
        ServiceTestClient.__init__(self, debug=True)

    def load_storage(self):
        super(AccuWeatherServiceTestClient, self).load_storage()
        self.add_license_keys_store(self.get_license_key_file())


class AccuWeatherServiceTests(ServiceTestCase):

    def test_init(self):
        service = AccuWeatherService(ServiceConfiguration.from_data("rest", "omdb", "film"))
        self.assertIsNotNone(service)

    def patch_requests_postcodesearch_success(self, url, headers, timeout):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = postcodesearch_success_response
        return mock_response

    def patch_requests_textsearch_success(self, url, headers, timeout):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = textsearch_success_response
        return mock_response

    def patch_requests_conditions_success(self, url, headers, timeout):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = conditions_success_response
        return mock_response

    def _do_postcodesearch(self):
        service = AccuWeatherService(ServiceConfiguration.from_data("rest", "accuweather", "weather"))
        self.assertIsNotNone(service)

        client = AccuWeatherServiceTestClient()
        service.initialise(client)

        response = service.postcodesearch("KY3 9UR")
        self.assertResponse(response, 'postcodesearch', 'accuweather', 'weather')

        key = AccuWeatherService.get_location_key(response)
        self.assertIsNotNone(key)
        self.assertEquals("47724_PC", key)

    @unittest.skipIf(integration_tests_active() is False, integration_tests_disabled)
    def test_postcodesearch_integration(self):
        self._do_postcodesearch()

    @patch("programy.services.rest.base.RESTService._requests_get", patch_requests_postcodesearch_success)
    def test_postcodesearch_unit(self):
        self._do_postcodesearch()

    def _do_textsearch(self):
        service = AccuWeatherService(ServiceConfiguration.from_data("rest", "accuweather", "weather"))
        self.assertIsNotNone(service)

        client = AccuWeatherServiceTestClient()
        service.initialise(client)

        response = service.textsearch("Kinghorn")
        self.assertResponse(response, 'textsearch', 'accuweather', 'weather')

        key = AccuWeatherService.get_location_key(response)
        self.assertIsNotNone(key)
        self.assertEquals("3385695", key)

    @unittest.skipIf(integration_tests_active() is False, integration_tests_disabled)
    def test_textsearch_integration(self):
        self._do_textsearch()

    @patch("programy.services.rest.base.RESTService._requests_get", patch_requests_textsearch_success)
    def test_textsearch_unit(self):
        self._do_textsearch()

    def _do_conditions(self):
        service = AccuWeatherService(ServiceConfiguration.from_data("rest", "accuweather", "weather"))
        self.assertIsNotNone(service)

        client = AccuWeatherServiceTestClient()
        service.initialise(client)

        response = service.conditions("3385695")
        self.assertResponse(response, 'conditions', 'accuweather', 'weather')

    @unittest.skipIf(integration_tests_active() is False, integration_tests_disabled)
    def test_conditions_integration(self):
        self._do_conditions()

    @patch("programy.services.rest.base.RESTService._requests_get", patch_requests_conditions_success)
    def test_conditions_unit(self):
        self._do_conditions()

    @patch("programy.services.rest.base.RESTService._requests_get", patch_requests_textsearch_success)
    def test_handler_load_textsearch(self):
        client = AccuWeatherServiceTestClient()
        conf_file = AccuWeatherService.get_default_conf_file()

        response = self._do_handler_load(client, conf_file, "accuweather", "ACCUWEATHER TEXTSEARCH LOCATION KINGHORN")
        self.assertIsNotNone(response)
        self.assertEqual("ACCUWEATHER RESULT KEY 3385695.", response)

    @patch("programy.services.rest.base.RESTService._requests_get", patch_requests_conditions_success)
    def test_conditions_location_aiml(self):
        client = AccuWeatherServiceTestClient()
        conf_file = AccuWeatherService.get_default_conf_file()

        response = self._do_handler_load(client, conf_file, "accuweather", "ACCUWEATHER CONDITIONS LOCATION KINGHORN")
        self.assertIsNotNone(response)
        self.assertEqual("It is currently -0.7 C and Cloudy.", response)

    @unittest.skipIf(integration_tests_active() is False, integration_tests_disabled)
    def test_weather_location_aiml(self):
        client = AccuWeatherServiceTestClient()
        conf_file = AccuWeatherService.get_default_conf_file()

        response = self._do_handler_load(client, conf_file, "accuweather", "ACCUWEATHER WEATHER LOCATION KINGHORN")
        self.assertIsNotNone(response)
        self.assertTrue(response.startswith("It is currently"))