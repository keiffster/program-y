import unittest
from unittest.mock import patch
from unittest.mock import Mock

from programy.services.rest.getguidelines.service import GetGuidelinesService
from programy.services.config import ServiceConfiguration
from programytest.services.testclient import ServiceTestClient
from programytest.services.testcase import ServiceTestCase
from programytest.externals import integration_tests_active, integration_tests_disabled
from programytest.services.rest.getguidelines.responses import all_success_response, vac_success_response
import logging


class GetGuidelinesServiceTestClient(ServiceTestClient):

    def __init__(self):
        ServiceTestClient.__init__(self, debug=True, level=logging.DEBUG)

    def load_storage(self):
        super(GetGuidelinesServiceTestClient, self).load_storage()
        self.add_license_keys_store(self.get_license_key_file())


class GetGuidelinesServiceTests(ServiceTestCase):

    @unittest.skip("GetGuidelines down at this time - getguidelines.com")
    def test_init(self):
        service = GetGuidelinesService(ServiceConfiguration.from_data("rest", "getguidelines", "health"))
        self.assertIsNotNone(service)

    def patch_requests_all_success_response(self, url, headers, timeout):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.text = all_success_response
        return mock_response

    def patch_requests_vac_success_response(self, url, headers, timeout):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.text = vac_success_response
        return mock_response

    def _do_all(self):
        service = GetGuidelinesService(ServiceConfiguration.from_data("rest", "getguidelines", "health"))
        self.assertIsNotNone(service)

        client = GetGuidelinesServiceTestClient()
        service.initialise(client)

        response = service.all("dm,chf")
        self.assertResponse(response, 'all', "getguidelines", "health")

    @unittest.skip("GetGuidelines down at this time - getguidelines.com")
    #@unittest.skipIf(integration_tests_active() is False, integration_tests_disabled)
    def test_all_integration(self):
        self._do_all()

    @patch("programy.services.rest.base.RESTService._requests_get", patch_requests_all_success_response)
    def test_all_unit(self):
        self._do_all()

    def _do_vac(self):
        service = GetGuidelinesService(ServiceConfiguration.from_data("rest", "getguidelines", "health"))
        self.assertIsNotNone(service)

        client = GetGuidelinesServiceTestClient()
        service.initialise(client)

        response = service.vac("dm,chf")
        self.assertResponse(response, 'vac', "getguidelines", "health")

    @unittest.skip("GetGuidelines down at this time - getguidelines.com")
    #@unittest.skipIf(integration_tests_active() is False, integration_tests_disabled)
    def test_vac_integration(self):
        self._do_vac()

    @patch("programy.services.rest.base.RESTService._requests_get", patch_requests_all_success_response)
    def test_vac_unit(self):
        self._do_vac()

    @patch("programy.services.rest.base.RESTService._requests_get", patch_requests_all_success_response)
    def test_all_aiml(self):
        client = GetGuidelinesServiceTestClient()
        conf_file = GetGuidelinesService.get_default_conf_file()

        response = self._do_handler_load(client, conf_file, "getguidelines", "GETGUIDELINES ALL DM CHF")
        self.assertIsNotNone(response)
        self.assertTrue(response.startswith("<ol><li>#1: Monitor glucose, HbA1c, blood pressure, body weight,"))

    @patch("programy.services.rest.base.RESTService._requests_get", patch_requests_vac_success_response)
    def test_vac_aiml(self):
        client = GetGuidelinesServiceTestClient()
        conf_file = GetGuidelinesService.get_default_conf_file()

        response = self._do_handler_load(client, conf_file, "getguidelines", "GETGUIDELINES VACINATION DM CHF")
        self.assertIsNotNone(response)

    @unittest.skip("GetGuidelines down at this time - getguidelines.com")
    def test_conditions_aiml(self):
        client = GetGuidelinesServiceTestClient()
        conf_file = GetGuidelinesService.get_default_conf_file()

        response = self._do_handler_load(client, conf_file, "getguidelines", "GETGUIDELINES CONDITIONS")
        self.assertIsNotNone(response)
        self.assertTrue(response.startswith("<ul><li>Key - Description</li>"))

