import unittest
from unittest.mock import patch
from unittest.mock import Mock
import os
from programy.services.rest.pandora.service import PandoraService
from programy.services.config import ServiceConfiguration
from programy.services.config import ServiceRESTConfiguration
from programytest.services.testclient import ServiceTestClient
from programytest.services.testcase import ServiceTestCase
from programytest.externals import integration_tests_active, integration_tests_disabled
from programytest.services.rest.pandora.responses import ask_success_response
from programytest.services.rest.pandora.responses import ask_service_failure


class PandoraServiceTestClient(ServiceTestClient):

    def __init__(self):
        ServiceTestClient.__init__(self, debug=True)

    def load_storage(self):
        super(PandoraServiceTestClient, self).load_storage()
        self.add_license_keys_store(self.get_license_key_file())


class PandoraServiceTests(ServiceTestCase):

    def test_init(self):
        service = PandoraService(ServiceConfiguration.from_data("rest", "pandora", "chatbot"))
        self.assertIsNotNone(service)

    def patch_requests_ask_success(self, url, headers, timeout):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = ask_success_response
        return mock_response

    def patch_requests_ask_failure_server_error(self, url, headers, timeout):
        mock_response = Mock()
        mock_response.status_code = 503
        mock_response.json.return_value = None
        return mock_response

    def patch_ask_failure_service_error(self, question):
        return ask_service_failure

    def _do_ask(self):
        service = PandoraService(ServiceConfiguration.from_data("rest", "pandora", "chatbot"))
        self.assertIsNotNone(service)

        client = PandoraServiceTestClient()
        service.initialise(client)

        response = service.ask("Hello")
        self.assertResponse(response, 'ask', "pandora", "chatbot")

    @unittest.skipIf(integration_tests_active() is False, integration_tests_disabled)
    def test_ask_integration(self):
        self._do_ask()

    @patch("programy.services.rest.base.RESTService._requests_get", patch_requests_ask_success)
    def test_ask_unit(self):
        self._do_ask()

    @patch("programy.services.rest.base.RESTService._requests_get", patch_requests_ask_success)
    def test_handler_load_ask_success(self):
        client = PandoraServiceTestClient()
        conf_file = PandoraService.get_default_conf_file()

        response = self._do_handler_load(client, conf_file, "pandora", "PANDORA ASK HELLO")
        self.assertIsNotNone(response)
        self.assertEqual("Hi there!", response)

    @patch("programy.services.rest.base.RESTService._requests_get", patch_requests_ask_failure_server_error)
    def test_handler_load_ask_server_failure(self):
        client = PandoraServiceTestClient()
        conf_file = PandoraService.get_default_conf_file()

        response = self._do_handler_load(client, conf_file, "pandora", "PANDORA ASK HELLO")
        self.assertIsNotNone(response)
        self.assertEqual("Pandorabots failed to return a valid response.", response)

    @patch("programy.services.rest.pandora.service.PandoraService.ask", patch_ask_failure_service_error)
    def test_handler_load_ask_service_failure(self):
        client = PandoraServiceTestClient()
        conf_file = PandoraService.get_default_conf_file()

        response = self._do_handler_load(client, conf_file, "pandora", "PANDORA ASK HELLO")
        self.assertIsNotNone(response)
        self.assertEqual("Pandorabots failed to return a valid response.", response)
