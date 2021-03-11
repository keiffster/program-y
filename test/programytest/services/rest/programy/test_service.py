import unittest
from unittest.mock import patch
from unittest.mock import Mock
import os
from programy.services.rest.programy.service import ProgramyService
from programy.services.config import ServiceConfiguration
from programy.services.config import ServiceRESTConfiguration
from programytest.services.testclient import ServiceTestClient
from programytest.services.testcase import ServiceTestCase
from programytest.externals import integration_tests_active, integration_tests_disabled
from programytest.services.rest.programy.responses import ask_success_response


class ProgramyServiceTestClient(ServiceTestClient):

    def __init__(self):
        ServiceTestClient.__init__(self, debug=True)

    def load_storage(self):
        super(ProgramyServiceTestClient, self).load_storage()
        self.add_license_keys_store(filepath=os.path.dirname(__file__) + os.sep + "../../testdata" + os.sep + "license.keys")


class ProgramyServiceTests(ServiceTestCase):

    def test_init(self):
        service = ProgramyService(ServiceConfiguration.from_data("rest", "programy", "chatbot"))
        self.assertIsNotNone(service)

    def patch_requests_programy_success(self, url, headers, timeout):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = ask_success_response
        return mock_response

    def _do_ask(self):
        service = ProgramyService(ServiceConfiguration.from_data("rest", "programy", "chatbot",
                                                                 api="https://www.chatilly.chat:9989/api/rest/v1.0/ask?question={0}&userid={1}",
                                                                 ))

        self.assertIsNotNone(service)

        client = ProgramyServiceTestClient()
        service.initialise(client)

        response = service.ask("Hello", "1234567890")
        self.assertResponse(response, 'ask', "programy", "chatbot")

    @unittest.skipIf(integration_tests_active() is False, integration_tests_disabled)
    def test_ask_integration(self):
        self._do_ask()

    @patch("programy.services.rest.base.RESTService._requests_get", patch_requests_programy_success)
    def test_ask_unit(self):
        self._do_ask()

    @unittest.skipIf(integration_tests_active() is False, integration_tests_disabled)
    @patch("programy.services.rest.base.RESTService._requests_get", patch_requests_programy_success)
    def test_handler_load(self):
        client = ProgramyServiceTestClient()
        conf_file = ProgramyService.get_default_conf_file()

        response = self._do_handler_load(client, conf_file, "programyv1", "PROGRAMY ASK HELLO USERID 123456789")
        self.assertIsNotNone(response)
        self.assertEqual("Hello!", response)