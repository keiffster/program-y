import unittest
from unittest.mock import patch
from programy.services.library.wikipedia.service import WikipediaService
from programy.services.config import ServiceConfiguration
from programytest.services.testclient import ServiceTestClient
from programytest.services.testcase import ServiceTestCase
from programytest.externals import integration_tests_active, integration_tests_disabled
from programytest.services.library.wikipedia.responses import search_success_response
from programytest.services.library.wikipedia.responses import summary_success_response


class WikipediaTestClient(ServiceTestClient):

    def __init__(self):
        ServiceTestClient.__init__(self, debug=True)

    def load_storage(self):
        super(WikipediaTestClient, self).load_storage()


class WikipediaServiceTests(ServiceTestCase):

    def test_init(self):
        service = WikipediaService(ServiceConfiguration.from_data("library", "wikipedia", "search"))
        self.assertIsNotNone(service)

    def patch_wikipedia_search_success(self, query, results=10, suggestion=False):
        return search_success_response

    def patch_wikipedia_summary_success(self, title, sentences=0, chars=0, auto_suggest=True, redirect=True):
        return summary_success_response

    def _do_search(self):
        service = WikipediaService(ServiceConfiguration.from_data("library", "wikipedia", "search"))
        self.assertIsNotNone(service)

        response = service.search("CHATBOTS")
        payload = self.assertResponse(response, 'search', 'wikipedia', 'search')

    @unittest.skipIf(integration_tests_active() is False, integration_tests_disabled)
    def test_search_integration(self):
        self._do_search()

    @patch("wikipedia.search", patch_wikipedia_search_success)
    def test_search_unit(self):
        self._do_search()

    def _do_summary(self):
        service = WikipediaService(ServiceConfiguration.from_data("library", "wikipedia", "search"))
        self.assertIsNotNone(service)

        response = service.summary("8 Out of 10 Cats Does Countdown")
        payload = self.assertResponse(response, 'summary', 'wikipedia', 'search')

    @unittest.skipIf(integration_tests_active() is False, integration_tests_disabled)
    def test_summary_integration(self):
        self._do_summary()

    @patch("wikipedia.summary", patch_wikipedia_summary_success)
    def test_summary_unit(self):
        self._do_summary()

    @patch("wikipedia.search", patch_wikipedia_search_success)
    def test_search_by_aiml(self):
        client = WikipediaTestClient()
        conf_file = WikipediaService.get_default_conf_file()

        response = self._do_handler_load(client, conf_file, "wikipedia", "WIKIPEDIA SEARCH CHATBOTS")
        self.assertIsNotNone(response)
        self.assertTrue(response.startswith("<ul><li>Chatbot</li><li>"))

    @patch("wikipedia.summary", patch_wikipedia_summary_success)
    def test_summary_by_aiml(self):
        client = WikipediaTestClient()
        conf_file = WikipediaService.get_default_conf_file()

        response = self._do_handler_load(client, conf_file, "wikipedia", "WIKIPEDIA SUMMARY 8 Out of 10 Cats")
        self.assertIsNotNone(response)
        self.assertTrue(response.startswith("8 Out of 10 Cats Does Countdown is a British comedy panel show."))
