import unittest
from unittest.mock import Mock
from unittest.mock import patch
import os
from programy.services.library.metoffice.service import MetOfficeService
from programy.services.rest.geonames.service import GeoNamesService
from programy.services.config import ServiceConfiguration
from programytest.externals import integration_tests_active, integration_tests_disabled
from programytest.services.testclient import ServiceTestClient
from programytest.services.testcase import ServiceTestCase
from programytest.services.library.metoffice.payloads.observation import observation_payload
from programytest.services.rest.geonames.responses import postcode_success_response
import logging


class MetOfficeTestClient(ServiceTestClient):

    def __init__(self):
        ServiceTestClient.__init__(self, debug=True, level=logging.DEBUG)

    def load_storage(self):
        super(MetOfficeTestClient, self).load_storage()
        self.add_license_keys_store(self.get_license_key_file())


class MetOfficeObservationServiceTests(ServiceTestCase):

    def test_init(self):
        service = MetOfficeService(ServiceConfiguration.from_data("library", "metoffice", "weather"))
        self.assertIsNotNone(service)
        client = MetOfficeTestClient()
        service.initialise(client)

    def patch_metoffer_current_observation_success(self, lat, lng):
        return observation_payload

    def _do_observation(self):
        service = MetOfficeService(ServiceConfiguration.from_data("library", "metoffice", "weather"))
        self.assertIsNotNone(service)
        client = MetOfficeTestClient()
        service.initialise(client)

        response = service.observation(56.0712, -3.1743)
        payload = self.assertResponse(response, 'observation', 'metoffice', 'weather')
        self.assertTrue('observation' in payload)
        self.assertTrue('SiteRep' in payload['observation'])
        self.assertTrue('DV' in payload['observation']['SiteRep'])
        self.assertTrue('Location' in payload['observation']['SiteRep']['DV'])
        self.assertTrue('Period' in payload['observation']['SiteRep']['DV']['Location'])

    @unittest.skipIf(integration_tests_active() is False, integration_tests_disabled)
    def test_observation_integration(self):
        self._do_observation()

    @patch("programy.services.library.metoffice.metoffice.MetOffice.current_observation", patch_metoffer_current_observation_success)
    def test_observation_unit(self):
        self._do_observation()

    @patch("programy.services.library.metoffice.metoffice.MetOffice.current_observation", patch_metoffer_current_observation_success)
    def test_obversation_by_aiml(self):
        client = MetOfficeTestClient()
        conf_file = MetOfficeService.get_default_conf_file()

        response = self._do_handler_load(client, conf_file, "metoffice", "METOFFICE OBSERVATION LAT SIGN POS DEC 56 FRAC 0719912 LNG SIGN NEG DEC 3 FRAC 1750909")
        self.assertIsNotNone(response)
        self.assertEqual("It is currently Partly cloudy (day) , with a temperature of 12 . 3 'C.", response)

    def patch_requests_postcode_success_reponse(self, url, headers, timeout):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = postcode_success_response
        return mock_response

    @patch("programy.services.library.metoffice.metoffice.MetOffice.current_observation", patch_metoffer_current_observation_success)
    @patch("programy.services.rest.base.RESTService._requests_get", patch_requests_postcode_success_reponse)
    def test_weather_postcode(self):
        client = MetOfficeTestClient()
        client_context = client.create_client_context("testuser")

        self._load_conf_file(client_context, MetOfficeService.get_default_conf_file())
        self.assertTrue("metoffice" in client_context.brain.service_handler.services)
        self._load_conf_file(client_context, GeoNamesService.get_default_conf_file())
        self.assertTrue("geonames" in client_context.brain.service_handler.services)

        response = client_context.bot.ask_question(client_context, "METOFFICE WEATHER POSTCODE KY39UR")

        self.assertIsNotNone(response)
        self.assertEqual("It is currently Partly cloudy (day) , with a temperature of 12 . 3 'C.", response)
