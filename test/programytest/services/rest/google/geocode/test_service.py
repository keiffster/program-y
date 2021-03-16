import unittest
from unittest.mock import patch
from unittest.mock import Mock
import os
from programy.services.rest.google.geocode.service import GoogleGeoCodeService
from programy.services.config import ServiceConfiguration
from programy.services.config import ServiceRESTConfiguration
from programytest.services.testclient import ServiceTestClient
from programytest.services.testcase import ServiceTestCase
from programytest.externals import integration_tests_active, integration_tests_disabled
from programytest.services.rest.google.geocode.responses import postcode_valid_response


class GoogleGeoCodeServiceTestClient(ServiceTestClient):

    def __init__(self):
        ServiceTestClient.__init__(self, debug=True)

    def load_storage(self):
        super(GoogleGeoCodeServiceTestClient, self).load_storage()
        self.add_license_keys_store(self.get_license_key_file())


class GoogleGeoCodeServiceTests(ServiceTestCase):

    def test_init(self):
        service = GoogleGeoCodeService(ServiceConfiguration.from_data("rest", "google", "geocode"))
        self.assertIsNotNone(service)

    def patch_requests_postcode_valid_response(self, url, headers, timeout):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = postcode_valid_response
        return mock_response

    def _do_postcode(self):
        service = GoogleGeoCodeService(ServiceConfiguration.from_data("rest", "google", "geocode"))

        self.assertIsNotNone(service)

        client = GoogleGeoCodeServiceTestClient()
        service.initialise(client)

        response = service.latlng_for_postcode("KY3 9UR")
        self.assertResponse(response, 'latlng_for_postcode', "google", "geocode")

    @unittest.skipIf(integration_tests_active() is False, integration_tests_disabled)
    def test_postcode_integration(self):
        self._do_postcode()

    @patch("programy.services.rest.base.RESTService._requests_get", patch_requests_postcode_valid_response)
    def test_postcode_unit(self):
        self._do_postcode()

    @patch("programy.services.rest.base.RESTService._requests_get", patch_requests_postcode_valid_response)
    def test_handler_load(self):
        client = GoogleGeoCodeServiceTestClient()
        conf_file = GoogleGeoCodeService.get_default_conf_file()

        response = self._do_handler_load(client, conf_file, "google.geocode", "GOOGLE LATLNG POSTCODE KY39UR")
        self.assertIsNotNone(response)
        self.assertEquals("LAT SIGN POS DEC 56 FRAC 0719912 LNG SIGN NEG DEC 3 FRAC 1750909.", response)