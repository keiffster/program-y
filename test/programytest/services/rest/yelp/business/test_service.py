import unittest
from unittest.mock import patch
from unittest.mock import Mock
import os
from programy.services.rest.yelp.business.service import YelpBusinessSearchService
from programy.services.config import ServiceConfiguration
from programytest.services.testclient import ServiceTestClient
from programytest.services.testcase import ServiceTestCase
from programytest.externals import integration_tests_active, integration_tests_disabled
from programytest.services.rest.yelp.business.responses import search_success_reponse


class YelpBusinessSearchServiceTestClient(ServiceTestClient):

    def __init__(self):
        ServiceTestClient.__init__(self, debug=True)

    def load_storage(self):
        super(YelpBusinessSearchServiceTestClient, self).load_storage()
        self.add_license_keys_store(self.get_license_key_file())


class YelpBusinessSearchServiceTests(ServiceTestCase):

    def test_init(self):
        service = YelpBusinessSearchService(ServiceConfiguration.from_data("rest", "yelp.business.search", "search"))
        self.assertIsNotNone(service)

    def patch_requests_search_success_reponse(self, url, headers, timeout):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = search_success_reponse
        return mock_response

    def _do_search(self):
        service = YelpBusinessSearchService(ServiceConfiguration.from_data("rest", "yelp.business.search", "search"))
        self.assertIsNotNone(service)

        client = YelpBusinessSearchServiceTestClient()
        service.initialise(client)

        response = service.search("post office", "kinghorn")
        self.assertResponse(response, 'search', "yelp.business.search", "search")

    @unittest.skipIf(integration_tests_active() is False, integration_tests_disabled)
    def test_search_integration(self):
        self._do_search()

    @patch("programy.services.rest.base.RESTService._requests_get", patch_requests_search_success_reponse)
    def test_search_unit(self):
        self._do_search()

    @patch("programy.services.rest.base.RESTService._requests_get", patch_requests_search_success_reponse)
    def test_search_aiml(self):
        client = YelpBusinessSearchServiceTestClient()
        conf_file = YelpBusinessSearchService.get_default_conf_file()

        response = self._do_handler_load(client, conf_file, "yelp.business.search", "YELP BUSINESS SEARCH POST OFFICE LOCATION KINGHORN")
        self.assertIsNotNone(response)
        self.assertTrue(response.startswith("<ul>\n<li>Aberdour Post Office - 43 High Street, Aberdour, Burntisland KY3 0SJ - +441383860317</li>"))
