import unittest
from unittest.mock import patch
from unittest.mock import Mock
import os
from programy.services.rest.cocktaildb.service import CocktailDBService
from programy.services.config import ServiceConfiguration
from programy.services.config import ServiceRESTConfiguration
from programytest.services.testclient import ServiceTestClient
from programytest.services.testcase import ServiceTestCase
from programytest.externals import integration_tests_active, integration_tests_disabled
from programytest.services.rest.cocktaildb.responses import search_by_name_success_response
from programytest.services.rest.cocktaildb.responses import search_by_ingredient_success_response


class CocktailDBServiceTestClient(ServiceTestClient):

    def __init__(self):
        ServiceTestClient.__init__(self, debug=True)

    def load_storage(self):
        super(CocktailDBServiceTestClient, self).load_storage()
        self.add_license_keys_store(self.get_license_key_file())


class CocktailDBServiceTests(ServiceTestCase):

    def test_init(self):
        service = CocktailDBService(ServiceConfiguration.from_data("rest", "cocktaildb", "drinks"))
        self.assertIsNotNone(service)

    def patch_requests_search_by_name_success(self, url, headers, timeout):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = search_by_name_success_response
        return mock_response

    def patch_requests_search_by_ingredient_success(self, url, headers, timeout):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = search_by_ingredient_success_response
        return mock_response

    def _do_search_by_name(self):
        service = CocktailDBService(ServiceConfiguration.from_data("rest", "cocktaildb", "drinks"))

        self.assertIsNotNone(service)

        client = CocktailDBServiceTestClient()
        service.initialise(client)

        response = service.search_by_name("Old fashioned")
        self.assertResponse(response, 'search_by_name', 'cocktaildb', 'drinks')

    @unittest.skipIf(integration_tests_active() is False, integration_tests_disabled)
    def test_search_by_name_integration(self):
        self._do_search_by_name()

    @patch("programy.services.rest.base.RESTService._requests_get", patch_requests_search_by_name_success)
    def test_search_by_name_unit(self):
        self._do_search_by_name()

    def _do_search_by_ingredient(self):
        service = CocktailDBService(ServiceConfiguration.from_data("rest", "cocktaildb", "drinks"))
        self.assertIsNotNone(service)

        client = CocktailDBServiceTestClient()
        service.initialise(client)

        response = service.search_by_ingredient("bourbon")
        self.assertResponse(response, 'search_by_ingredient', 'cocktaildb', 'drinks')

    @unittest.skipIf(integration_tests_active() is False, integration_tests_disabled)
    def test_search_by_ingredient_integration(self):
        self._do_search_by_ingredient()

    @patch("programy.services.rest.base.RESTService._requests_get", patch_requests_search_by_ingredient_success)
    def test_search_by_ingredient_unit(self):
        self._do_search_by_ingredient()

    @patch("programy.services.rest.base.RESTService._requests_get", patch_requests_search_by_name_success)
    def test_handler_load_name(self):
        client = CocktailDBServiceTestClient()
        conf_file = CocktailDBService.get_default_conf_file()

        response = self._do_handler_load(client, conf_file, "cocktaildb", "COCKTAILDB SEARCH NAME OLD FASHIONED")
        self.assertIsNotNone(response)
        self.assertTrue(response.startswith("To make a Old Fashioned"))

    @patch("programy.services.rest.base.RESTService._requests_get", patch_requests_search_by_ingredient_success)
    def test_handler_load_ingredient(self):
        client = CocktailDBServiceTestClient()
        conf_file = CocktailDBService.get_default_conf_file()

        response = self._do_handler_load(client, conf_file, "cocktaildb", "COCKTAILDB SEARCH INGREDIENT BOURBON")
        self.assertIsNotNone(response)
        self.assertTrue(response.startswith("Bourbon whiskey /bɜːrbən/ is a type of American whiskey:"))
