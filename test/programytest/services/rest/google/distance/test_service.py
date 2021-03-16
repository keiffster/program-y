import unittest
from unittest.mock import patch
from unittest.mock import Mock
import os
from programy.services.rest.google.distance.service import GoogleDistanceService
from programy.services.config import ServiceConfiguration
from programy.services.config import ServiceRESTConfiguration
from programytest.services.testclient import ServiceTestClient
from programytest.services.testcase import ServiceTestCase
from programytest.externals import integration_tests_active, integration_tests_disabled
from programytest.services.rest.google.distance.responses import distance_success_response


class GoogleDistanceServiceTestClient(ServiceTestClient):

    def __init__(self):
        ServiceTestClient.__init__(self, debug=True)

    def load_storage(self):
        super(GoogleDistanceServiceTestClient, self).load_storage()
        self.add_license_keys_store(self.get_license_key_file())


class GoogleDistanceServiceTests(ServiceTestCase):

    def test_init(self):
        service = GoogleDistanceService(ServiceConfiguration.from_data("rest", "google", "distance"))
        self.assertIsNotNone(service)

    def patch_requests_distance_success_response(self, url, headers, timeout):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = distance_success_response
        return mock_response

    def _do_distance(self):
        service = GoogleDistanceService(ServiceConfiguration.from_data("rest", "google", "distance"))
        self.assertIsNotNone(service)

        client = GoogleDistanceServiceTestClient()
        service.initialise(client)

        response = service.get_distance("London", "Brighton")
        self.assertResponse(response, 'get_distance', "google", "distance")

    @unittest.skipIf(integration_tests_active() is False, integration_tests_disabled)
    def test_distance_integration(self):
        self._do_distance()

    @patch("programy.services.rest.base.RESTService._requests_get", patch_requests_distance_success_response)
    def test_distance_unit(self):
        self._do_distance()

    @patch("programy.services.rest.base.RESTService._requests_get", patch_requests_distance_success_response)
    def test_handler_load(self):
        client = GoogleDistanceServiceTestClient()
        conf_file = GoogleDistanceService.get_default_conf_file()

        response = self._do_handler_load(client, conf_file, "google.distance", "GOOGLE DISTANCE ORIGIN KINGHORN DESTINATION EDINBURGH")
        self.assertIsNotNone(response)
        self.assertEquals("About 64.6 mi.", response)