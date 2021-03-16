import unittest
from unittest.mock import patch
from unittest.mock import Mock
import os
from programy.services.rest.google.directions.service import GoogleDirectionsService
from programy.services.config import ServiceConfiguration
from programy.services.config import ServiceRESTConfiguration
from programytest.services.testclient import ServiceTestClient
from programytest.services.testcase import ServiceTestCase
from programytest.externals import integration_tests_active, integration_tests_disabled
from programytest.services.rest.google.directions.responses import directions_success_reponse


class GoogleDirectionsServiceTestClient(ServiceTestClient):

    def __init__(self):
        ServiceTestClient.__init__(self, debug=True)

    def load_storage(self):
        super(GoogleDirectionsServiceTestClient, self).load_storage()
        self.add_license_keys_store(self.get_license_key_file())


class GoogleDirectionsServiceTests(ServiceTestCase):

    def test_init(self):
        service = GoogleDirectionsService(ServiceConfiguration.from_data("rest", "google", "directions"))
        self.assertIsNotNone(service)

    def patch_requests_directions_success_reponse(self, url, headers, timeout):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = directions_success_reponse
        return mock_response

    def _do_directions(self):
        service = GoogleDirectionsService(ServiceConfiguration.from_data("rest", "google", "directions"))
        self.assertIsNotNone(service)

        client = GoogleDirectionsServiceTestClient()
        service.initialise(client)

        response = service.get_directions("London", "Brighton")
        self.assertResponse(response, 'get_directions', "google", "directions")

    @unittest.skipIf(integration_tests_active() is False, integration_tests_disabled)
    def test_directions_integrastion(self):
        self._do_directions()

    @patch("programy.services.rest.base.RESTService._requests_get", patch_requests_directions_success_reponse)
    def test_directions_unit(self):
        self._do_directions()

    @patch("programy.services.rest.base.RESTService._requests_get", patch_requests_directions_success_reponse)
    def test_handler_load(self):
        client = GoogleDirectionsServiceTestClient()
        conf_file = GoogleDirectionsService.get_default_conf_file()

        response = self._do_handler_load(client, conf_file, "google.directions", "GOOGLE DIRECTIONS ORIGIN KINGHORN DESTINATION EDINBURGH")
        self.assertIsNotNone(response)
        self.assertTrue(response.startswith("<ol><li>Head <b>north</b> toward <b>A4</b></li>"))