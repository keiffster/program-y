import unittest
from unittest.mock import patch
from unittest.mock import Mock
import os
from programy.services.rest.wolframalpha.service import WolframAlphaService
from programy.services.config import ServiceConfiguration
from programy.services.config import ServiceRESTConfiguration
from programytest.services.testclient import ServiceTestClient
from programytest.services.testcase import ServiceTestCase
from programytest.externals import integration_tests_active, integration_tests_disabled
from programytest.services.rest.wolframalpha.responses import simple_success_response
from programytest.services.rest.wolframalpha.responses import short_success_response


class WolframAlphaServiceTestClient(ServiceTestClient):

    def __init__(self):
        ServiceTestClient.__init__(self, debug=True)

    def load_storage(self):
        super(WolframAlphaServiceTestClient, self).load_storage()
        self.add_license_keys_store(self.get_license_key_file())


class WolframAlphaServiceTests(ServiceTestCase):

    def test_init(self):
        service = WolframAlphaService(ServiceConfiguration.from_data("rest", "wolframalpha", "search"))
        self.assertIsNotNone(service)

    def patch_requests_simple_success(self, url, headers, timeout):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.text = simple_success_response
        return mock_response

    def patch_requests_short_success(self, url, headers, timeout):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.text = short_success_response
        return mock_response

    def _do_simple(self):
        service = WolframAlphaService(ServiceConfiguration.from_data("rest", "wolframalpha", "search"))
        self.assertIsNotNone(service)

        client = WolframAlphaServiceTestClient()
        service.initialise(client)

        response = service.simple("CHATBOTS")
        self.assertResponse(response, 'simple', "wolframalpha", "search")

    @unittest.skipIf(integration_tests_active() is False, integration_tests_disabled)
    def test_simple_integration(self):
        self._do_simple()

    @patch("programy.services.rest.base.RESTService._requests_get", patch_requests_simple_success)
    def test_simple_unit(self):
        self._do_simple()

    def _do_short(self):
        service = WolframAlphaService(ServiceConfiguration.from_data("rest", "wolframalpha", "search"))
        self.assertIsNotNone(service)

        client = WolframAlphaServiceTestClient()
        service.initialise(client)

        response = service.short("How far is Los Angeles from New York")
        self.assertResponse(response, 'short', "wolframalpha", "search")

    @unittest.skipIf(integration_tests_active() is False, integration_tests_disabled)
    def test_short_integration(self):
        self._do_short()

    @patch("programy.services.rest.base.RESTService._requests_get", patch_requests_short_success)
    def test_short_unit(self):
        self._do_short()

    @patch("programy.services.rest.base.RESTService._requests_get", patch_requests_simple_success)
    def test_handler_load_simple(self):
        client = WolframAlphaServiceTestClient()
        conf_file = WolframAlphaService.get_default_conf_file()

        response = self._do_handler_load(client, conf_file, "wolframalpha", "WOLFRAMALPHA SIMPLE EDINBURGH UK")
        self.assertIsNotNone(response)
        self.assertEqual("Edinburgh, Edinburgh.", response)

    @patch("programy.services.rest.base.RESTService._requests_get", patch_requests_short_success)
    def test_handler_load_short(self):
        client = WolframAlphaServiceTestClient()
        conf_file = WolframAlphaService.get_default_conf_file()

        response = self._do_handler_load(client, conf_file, "wolframalpha", "WOLFRAMALPHA SHORT How far is Los Angeles from New York")
        self.assertIsNotNone(response)
        self.assertEqual("About 2464 miles.", response)