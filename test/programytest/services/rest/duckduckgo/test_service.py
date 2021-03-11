import unittest
from unittest.mock import patch
from unittest.mock import Mock
from programy.services.rest.duckduckgo.service import DuckDuckGoService
from programy.services.config import ServiceConfiguration
from programytest.services.testclient import ServiceTestClient
from programytest.services.testcase import ServiceTestCase
from programytest.externals import integration_tests_active, integration_tests_disabled
from programytest.services.rest.duckduckgo.responses import instant_success_response
from programytest.services.rest.duckduckgo.responses import scrape_success_response

class DuckDuckGoServiceTestClient(ServiceTestClient):

    def __init__(self):
        ServiceTestClient.__init__(self, debug=True)

    def load_storage(self):
        super(DuckDuckGoServiceTestClient, self).load_storage()


class DuckDuckGoServiceTests(ServiceTestCase):

    def test_init(self):
        service = DuckDuckGoService(ServiceConfiguration.from_data("rest", "duckduckgo", "search"))
        self.assertIsNotNone(service)

    def patch_requests_instant_success_response(self, url, headers, timeout):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = instant_success_response
        return mock_response

    def patch_requests_scrape_success_response(self, url, headers, timeout):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = scrape_success_response
        return mock_response

    def _do_instant(self):
        service = DuckDuckGoService(ServiceConfiguration.from_data("rest", "duckduckgo", "search"))
        self.assertIsNotNone(service)

        client = DuckDuckGoServiceTestClient()
        service.initialise(client)

        response = service.instant("CHATBOTS")
        self.assertResponse(response, 'instant', 'duckduckgo', 'search')

    @unittest.skipIf(integration_tests_active() is False, integration_tests_disabled)
    def test_do_instant_integration(self):
        self._do_instant()

    @patch("programy.services.rest.base.RESTService._requests_get", patch_requests_instant_success_response)
    def test_do_instant_unit(self):
        self._do_instant()

    def _do_scrape(self):
        service = DuckDuckGoService(ServiceConfiguration.from_data("rest", "duckduckgo", "search"))
        self.assertIsNotNone(service)

        client = DuckDuckGoServiceTestClient()
        service.initialise(client)

        response = service.scrape("CHATBOTS")
        self.assertResponse(response, 'scrape', 'duckduckgo', 'search')

    @unittest.skipIf(integration_tests_active() is False, integration_tests_disabled)
    def test_do_scraoe_integration(self):
        self._do_scrape()

    @patch("programy.services.rest.base.RESTService._requests_get", patch_requests_scrape_success_response)
    def test_do_scrape_unit(self):
        self._do_scrape()

    @patch("programy.services.rest.base.RESTService._requests_get", patch_requests_instant_success_response)
    def test_instant_aiml(self):
        client = DuckDuckGoServiceTestClient()
        conf_file = DuckDuckGoService.get_default_conf_file()

        response = self._do_handler_load(client, conf_file, "duckduckgo", "DUCKDUCKGO INSTANT CHATBOTS")
        self.assertIsNotNone(response)
        self.assertTrue(response.startswith("A chatbot is a piece of software that conducts a conversation via auditory or textual methods"))

    @patch("programy.services.rest.base.RESTService._requests_get", patch_requests_scrape_success_response)
    def test_scrape_aiml(self):
        client = DuckDuckGoServiceTestClient()
        conf_file = DuckDuckGoService.get_default_conf_file()

        response = self._do_handler_load(client, conf_file, "duckduckgo", "DUCKDUCKGO SCRAPE WHAT ARE CHATBOTS")
        self.assertTrue(response.startswith("A chatbot is a piece of software that conducts a conversation via auditory or textual methods"))
