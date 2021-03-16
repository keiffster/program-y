import unittest
from unittest.mock import patch
from unittest.mock import Mock
from programy.services.rest.geonames.service import GeoNamesService
from programy.services.config import ServiceConfiguration
from programytest.services.testclient import ServiceTestClient
from programytest.services.testcase import ServiceTestCase
from programytest.externals import integration_tests_active, integration_tests_disabled
from programytest.services.rest.geonames.responses import postcode_success_response
from programytest.services.rest.geonames.responses import placename_success_response


class GeoNamesServiceTestClient(ServiceTestClient):

    def __init__(self):
        ServiceTestClient.__init__(self, debug=True)

    def load_storage(self):
        super(GeoNamesServiceTestClient, self).load_storage()


class GeoNamesServiceTests(ServiceTestCase):

    def test_init(self):
        service = GeoNamesService(ServiceConfiguration.from_data("rest", "geonames", "geocode"))
        self.assertIsNotNone(service)

    def patch_requests_postcode_success_reponse(self, url, headers, timeout):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = postcode_success_response
        return mock_response

    def patch_requests_placename_success_reponse(self, url, headers, timeout):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = placename_success_response
        return mock_response

    def _do_postcode(self):
        service = GeoNamesService(ServiceConfiguration.from_data("rest", "geonames", "geocode"))

        self.assertIsNotNone(service)

        client = GeoNamesServiceTestClient()
        service.initialise(client)

        response = service.latlng_for_postcode("KY3 9UR")
        self.assertResponse(response, 'latlng_for_postcode', "geonames", "geocode")

    @unittest.skipIf(integration_tests_active() is False, integration_tests_disabled)
    def test_postcode_integration(self):
        self._do_postcode()

    @patch("programy.services.rest.base.RESTService._requests_get", patch_requests_postcode_success_reponse)
    def test_postcode_unit(self):
        self._do_postcode()

    def _do_placename(self):
        service = GeoNamesService(ServiceConfiguration.from_data("rest", "geonames", "geocode"))

        self.assertIsNotNone(service)

        client = GeoNamesServiceTestClient()
        service.initialise(client)

        response = service.latlng_for_placename("KY3 9UR")
        self.assertResponse(response, 'latlng_for_placename', "geonames", "geocode")

    @unittest.skipIf(integration_tests_active() is False, integration_tests_disabled)
    def test_placename_integration(self):
        self._do_placename()

    @patch("programy.services.rest.base.RESTService._requests_get", patch_requests_placename_success_reponse)
    def test_placename_unit(self):
        self._do_placename()

    @patch("programy.services.rest.base.RESTService._requests_get", patch_requests_postcode_success_reponse)
    def test_postcode_aiml(self):
        client = GeoNamesServiceTestClient()
        conf_file = GeoNamesService.get_default_conf_file()

        response = self._do_handler_load(client, conf_file, "geonames", "GEONAMES LATLNG POSTCODE KY39UR")
        self.assertIsNotNone(response)
        self.assertEqual("LAT SIGN POS DEC 56 FRAC 07206630948395 LNG SIGN NEG DEC 3 FRAC 175233081708717.", response)

    @patch("programy.services.rest.base.RESTService._requests_get", patch_requests_placename_success_reponse)
    def test_placename_aiml(self):
        client = GeoNamesServiceTestClient()
        conf_file = GeoNamesService.get_default_conf_file()

        response = self._do_handler_load(client, conf_file, "geonames", "GEONAMES LATLNG PLACENAME KINGHORN")
        self.assertIsNotNone(response)
        self.assertEqual("LAT SIGN POS DEC 56 FRAC 07206630948395 LNG SIGN NEG DEC 3 FRAC 175233081708717.", response)

    @patch("programy.services.rest.base.RESTService._requests_get", patch_requests_placename_success_reponse)
    def test_placename_aiml_with_country(self):
        client = GeoNamesServiceTestClient()
        conf_file = GeoNamesService.get_default_conf_file()

        response = self._do_handler_load(client, conf_file, "geonames", "GEONAMES LATLNG PLACENAME KINGHORN COUNTRY UK")
        self.assertIsNotNone(response)
        self.assertEqual("LAT SIGN POS DEC 56 FRAC 07206630948395 LNG SIGN NEG DEC 3 FRAC 175233081708717.", response)

    @unittest.skipIf(integration_tests_active() is False, integration_tests_disabled)
    def test_placename_aiml_different_country(self):
        client = GeoNamesServiceTestClient()
        conf_file = GeoNamesService.get_default_conf_file()

        response = self._do_handler_load(client, conf_file, "geonames", "GEONAMES LATLNG PLACENAME WASHINGTON COUNTRY US")
        self.assertIsNotNone(response)
        self.assertEqual("LAT SIGN POS DEC 38 FRAC 545851 LNG SIGN NEG DEC 91 FRAC 019346.", response)

        response = self._do_handler_load(client, conf_file, "geonames", "GEONAMES LATLNG PLACENAME WASHINGTON COUNTRY UK")
        self.assertIsNotNone(response)
        self.assertEqual("LAT SIGN POS DEC 54 FRAC 885019095463335 LNG SIGN NEG DEC 1 FRAC 5427184694082379.", response)