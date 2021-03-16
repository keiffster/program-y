import unittest
from unittest.mock import patch
from unittest.mock import Mock
import os
from programy.services.rest.omdb.service import OMDBService
from programy.services.config import ServiceConfiguration
from programytest.services.testclient import ServiceTestClient
from programytest.services.testcase import ServiceTestCase
from programytest.externals import integration_tests_active, integration_tests_disabled
from programytest.services.rest.omdb.responses import title_search_success_response


class OMDBServiceTestClient(ServiceTestClient):

    def __init__(self):
        ServiceTestClient.__init__(self, debug=True)

    def load_storage(self):
        super(OMDBServiceTestClient, self).load_storage()
        self.add_license_keys_store(self.get_license_key_file())


class OMDBServiceTests(ServiceTestCase):

    def test_init(self):
        service = OMDBService(ServiceConfiguration.from_data("rest", "omdb", "film"))
        self.assertIsNotNone(service)

    def patch_requests_title_search_success(self, url, headers, timeout):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = title_search_success_response
        return mock_response

    def _do_title_search(self):
        service = OMDBService(ServiceConfiguration.from_data("rest", "omdb", "film"))
        self.assertIsNotNone(service)

        client = OMDBServiceTestClient()
        service.initialise(client)

        response = service.title_search("Aliens")
        self.assertResponse(response, 'title_search', "omdb", "film")

    @unittest.skipIf(integration_tests_active() is False, integration_tests_disabled)
    def test_title_search_integration(self):
        self._do_title_search()

    @patch("programy.services.rest.base.RESTService._requests_get", patch_requests_title_search_success)
    def test_title_search_unit(self):
        self._do_title_search()

    @patch("programy.services.rest.base.RESTService._requests_get", patch_requests_title_search_success)
    def test_handler_title_search(self):
        client = OMDBServiceTestClient()
        conf_file = OMDBService.get_default_conf_file()

        response = self._do_handler_load(client, conf_file, "omdb", "OMDB TITLE SEARCH ALIENS")
        self.assertIsNotNone(response)
        self.assertTrue(response.startswith("Aliens was released in 18 Jul 1986 and directed by James Cameron and starring Sigourney Weaver"))