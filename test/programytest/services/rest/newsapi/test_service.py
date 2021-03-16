import unittest
from unittest.mock import patch
from unittest.mock import Mock
import os
from programy.services.rest.newsapi.service import NewsAPIService
from programy.services.config import ServiceConfiguration
from programy.services.config import ServiceRESTConfiguration
from programytest.services.testclient import ServiceTestClient
from programytest.services.testcase import ServiceTestCase
from programytest.externals import integration_tests_active, integration_tests_disabled
from programytest.services.rest.newsapi.responses import everything_success_response
from programytest.services.rest.newsapi.responses import headlines_success_response
from programytest.services.rest.newsapi.responses import sources_success_response


class NewsAPIServiceTestClient(ServiceTestClient):

    def __init__(self):
        ServiceTestClient.__init__(self, debug=True)

    def load_storage(self):
        super(NewsAPIServiceTestClient, self).load_storage()
        self.add_license_keys_store(self.get_license_key_file())


class NewsAPIServiceTests(ServiceTestCase):

    def test_init(self):
        service = NewsAPIService(ServiceConfiguration.from_data("rest", "newsapi", "news"))
        self.assertIsNotNone(service)

    def patch_requests_everything_success_response(self, url, headers, timeout):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = everything_success_response
        return mock_response

    def patch_requests_headlines_success_response(self, url, headers, timeout):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = headlines_success_response
        return mock_response

    def patch_requests_sources_success_response(self, url, headers, timeout):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = sources_success_response
        return mock_response

    def _do_everything(self):
        service = NewsAPIService(ServiceConfiguration.from_data("rest", "newsapi", "news"))
        self.assertIsNotNone(service)

        client = NewsAPIServiceTestClient()
        service.initialise(client)

        response = service.get_everything("chatbot")
        self.assertResponse(response, 'get_everything', "newsapi", "news")

    @unittest.skipIf(integration_tests_active() is False, integration_tests_disabled)
    def test_everything_integration(self):
        self._do_everything()

    @patch("programy.services.rest.base.RESTService._requests_get", patch_requests_everything_success_response)
    def test_everything_unit(self):
        self._do_everything()

    def _do_headlines(self):
        service = NewsAPIService(ServiceConfiguration.from_data("rest", "newsapi", "news"))
        self.assertIsNotNone(service)

        client = NewsAPIServiceTestClient()
        service.initialise(client)

        response = service.get_headlines("uk")
        self.assertResponse(response, 'get_headlines', "newsapi", "news")

    @unittest.skipIf(integration_tests_active() is False, integration_tests_disabled)
    def test_headlines_integration(self):
        self._do_headlines()

    @patch("programy.services.rest.base.RESTService._requests_get", patch_requests_headlines_success_response)
    def test_headlines_unit(self):
        self._do_headlines()

    def _do_sources(self):
        service = NewsAPIService(ServiceConfiguration.from_data("rest", "newsapi", "news"))
        self.assertIsNotNone(service)

        client = NewsAPIServiceTestClient()
        service.initialise(client)

        response = service.get_sources()
        self.assertResponse(response, 'get_sources', "newsapi", "news")

    @unittest.skipIf(integration_tests_active() is False, integration_tests_disabled)
    def test_sources_integration(self):
        self._do_sources()

    @patch("programy.services.rest.base.RESTService._requests_get", patch_requests_sources_success_response)
    def test_sources_unit(self):
        self._do_sources()

    @patch("programy.services.rest.base.RESTService._requests_get", patch_requests_everything_success_response)
    def test_handler_load_everything(self):
        client = NewsAPIServiceTestClient()
        conf_file = NewsAPIService.get_default_conf_file()

        response = self._do_handler_load(client, conf_file, "newsapi", "NEWSAPI EVERYTHING CHATBOTS")
        self.assertIsNotNone(response)
        self.assertTrue(response.startswith("<ul><li>How artificial intelligence and machine learning produced robots we can talk to</li>"))