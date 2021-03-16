import unittest
from unittest.mock import patch
from unittest.mock import Mock
import os
from programy.services.rest.microsoft.search.service import MicrosoftSearchService
from programy.services.config import ServiceConfiguration
from programytest.services.testclient import ServiceTestClient
from programytest.services.testcase import ServiceTestCase
from programytest.externals import integration_tests_active, integration_tests_disabled
from programytest.services.rest.microsoft.search.responses import search_success_reponse


class MicrosoftSearchServiceTestClient(ServiceTestClient):

    def __init__(self):
        ServiceTestClient.__init__(self, debug=True)

    def load_storage(self):
        super(MicrosoftSearchServiceTestClient, self).load_storage()
        self.add_license_keys_store(self.get_license_key_file())


class MicrosoftSearchServiceTests(ServiceTestCase):

    def test_init(self):
        service = MicrosoftSearchService(ServiceConfiguration.from_data("rest", "microsoft.search", "search",
                                                                        url="https://chatilly.cognitiveservices.azure.com/bing/v7.0/search"))
        self.assertIsNotNone(service)

    def patch_requests_search_success_reponse(self, url, headers, timeout):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = search_success_reponse
        return mock_response

    def _do_search(self):
        service = MicrosoftSearchService(ServiceConfiguration.from_data("rest", "microsoft.search", "search",
                                                                        url="https://chatilly.cognitiveservices.azure.com/bing/v7.0/search"))
        self.assertIsNotNone(service)

        client = MicrosoftSearchServiceTestClient()
        service.initialise(client)

        response = service.search("chatbots")
        self.assertResponse(response, 'search', "microsoft.search", "search")

    @unittest.skip("Needs active cognitiveservices.azure.com account, chatilly closed down")
    #@unittest.skipIf(integration_tests_active() is False, integration_tests_disabled)
    def test_search_integration(self):
        self._do_search()

    @patch("programy.services.rest.base.RESTService._requests_get", patch_requests_search_success_reponse)
    def test_search_unit(self):
        self._do_search()

    @patch("programy.services.rest.base.RESTService._requests_get", patch_requests_search_success_reponse)
    def test_search_aiml(self):
        client = MicrosoftSearchServiceTestClient()
        conf_file = MicrosoftSearchService.get_default_conf_file()

        response = self._do_handler_load(client, conf_file, "microsoft.search", "MICROSOFT SEARCH CHATBOTS")
        self.assertIsNotNone(response)
        self.assertTrue(response.startswith("<ul>\n<li>Chatbots are also appearing in the healthcare industry"))
