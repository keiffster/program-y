import unittest
from unittest.mock import patch
from unittest.mock import Mock
import os
from programy.services.rest.goodreads.service import GoodReadsService
from programy.services.config import ServiceConfiguration
from programy.services.config import ServiceRESTConfiguration
from programytest.services.testclient import ServiceTestClient
from programytest.services.testcase import ServiceTestCase
from programytest.externals import integration_tests_active, integration_tests_disabled
from programytest.services.rest.goodreads.responses import search_author_success_response
from programytest.services.rest.goodreads.responses import book_list_success_response


class GoodReadsServiceTestClient(ServiceTestClient):

    def __init__(self):
        ServiceTestClient.__init__(self, debug=True)

    def load_storage(self):
        super(GoodReadsServiceTestClient, self).load_storage()
        self.add_license_keys_store(self.get_license_key_file())


class GoodReadsServiceTests(ServiceTestCase):

    @unittest.skip("Goodreads currently disabled at source - https://help.goodreads.com/s/article/Why-did-my-API-key-stop-working")
    def test_init(self):
        service = GoodReadsService(ServiceConfiguration.from_data("rest", "goodreads", "books"))
        self.assertIsNotNone(service)

    def patch_requests_search_author_success_response(self, url, headers, timeout):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.content = search_author_success_response
        return mock_response

    def patch_requests_book_list_success_response(self, url, headers, timeout):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.content = book_list_success_response
        return mock_response

    def _do_search_author(self):
        service = GoodReadsService(ServiceConfiguration.from_data("rest", "goodreads", "books",))
        self.assertIsNotNone(service)

        client = GoodReadsServiceTestClient()
        service.initialise(client)

        response = service.search_for_author("William Gibson")
        self.assertResponse(response, 'search_for_author', "goodreads", "books",)

    @unittest.skip("Goodreads currently disabled at source - https://help.goodreads.com/s/article/Why-did-my-API-key-stop-working")
    #@unittest.skipIf(integration_tests_active() is False, integration_tests_disabled)
    def test_search_author_integration(self):
        self._do_search_author()

    @patch("programy.services.rest.base.RESTService._requests_get", patch_requests_search_author_success_response)
    def test_search_author_unit(self):
        self._do_search_author()

    def _do_book_list(self):
        service = GoodReadsService(ServiceConfiguration.from_data("rest", "goodreads", "books"))
        self.assertIsNotNone(service)

        client = GoodReadsServiceTestClient()
        service.initialise(client)

        response = service.list_books("9226")
        self.assertResponse(response, 'list_books', "goodreads", "books",)

    @unittest.skip("Goodreads currently disabled at source - https://help.goodreads.com/s/article/Why-did-my-API-key-stop-working")
    #@unittest.skipIf(integration_tests_active() is False, integration_tests_disabled)
    def test_book_list_integration(self):
        self._do_book_list()

    @patch("programy.services.rest.base.RESTService._requests_get", patch_requests_book_list_success_response)
    def test_book_list_unit(self):
        self._do_book_list()

    @patch("programy.services.rest.base.RESTService._requests_get", patch_requests_search_author_success_response)
    def test_handler_load_author_search(self):
        client = GoodReadsServiceTestClient()
        conf_file = GoodReadsService.get_default_conf_file()

        response = self._do_handler_load(client, conf_file, "goodreads", "GOODREADS SEARCH AUTHOR IAIN BANKS")
        self.assertIsNotNone(response)
        self.assertEquals("9226.", response)

    @unittest.skip("Goodreads currently disabled at source - https://help.goodreads.com/s/article/Why-did-my-API-key-stop-working")
    #@patch("programy.services.rest.base.RESTService._requests_get", patch_requests_book_list_success_response)
    def test_handler_load_author_search(self):
        client = GoodReadsServiceTestClient()
        conf_file = GoodReadsService.get_default_conf_file()

        response = self._do_handler_load(client, conf_file, "goodreads", "GOODREADS BOOK LIST 9226")
        self.assertIsNotNone(response)
        self.assertTrue(response.startswith("<ul><li>Neuromancer</li>"))