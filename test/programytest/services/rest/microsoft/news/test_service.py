import unittest
from unittest.mock import patch
from unittest.mock import Mock
import os
from programy.services.rest.microsoft.news.service import MicrosoftNewsService
from programy.services.config import ServiceConfiguration
from programytest.services.testclient import ServiceTestClient
from programytest.services.testcase import ServiceTestCase
from programytest.externals import integration_tests_active, integration_tests_disabled
from programytest.services.rest.microsoft.news.responses import news_success_reponse


class MicrosoftNewsServiceTestClient(ServiceTestClient):

    def __init__(self):
        ServiceTestClient.__init__(self, debug=True)

    def load_storage(self):
        super(MicrosoftNewsServiceTestClient, self).load_storage()
        self.add_license_keys_store(self.get_license_key_file())


class MicrosoftNewsServiceTests(ServiceTestCase):

    def test_init(self):
        service = MicrosoftNewsService(ServiceConfiguration.from_data("rest", "microsoft.news", "news",
                                                                        url="https://chatilly.cognitiveservices.azure.com/bing/v7.0"))
        self.assertIsNotNone(service)

    def patch_requests_news_success_reponse(self, url, headers, timeout):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = news_success_reponse
        return mock_response

    def _do_news(self):
        service = MicrosoftNewsService(ServiceConfiguration.from_data("rest", "microsoft.news", "news",
                                                                        url="https://chatilly.cognitiveservices.azure.com/bing/v7.0"))
        self.assertIsNotNone(service)

        client = MicrosoftNewsServiceTestClient()
        service.initialise(client)

        response = service.news("chatbots")
        self.assertResponse(response, 'news', "microsoft.news", "news")

    @unittest.skipIf(integration_tests_active() is False, integration_tests_disabled)
    def test_news_integration(self):
        self._do_news()

    @patch("programy.services.rest.base.RESTService._requests_get", patch_requests_news_success_reponse)
    def test_news_unit(self):
        self._do_news()

    @patch("programy.services.rest.base.RESTService._requests_get", patch_requests_news_success_reponse)
    def test_news_aiml(self):
        client = MicrosoftNewsServiceTestClient()
        conf_file = MicrosoftNewsService.get_default_conf_file()

        response = self._do_handler_load(client, conf_file, "microsoft.news", "MICROSOFT NEWS CHATBOTS")
        self.assertIsNotNone(response)
        self.assertTrue(response.startswith("<ul>\n<li>How Europe deals with terror offenders when they are freed from jail"))
