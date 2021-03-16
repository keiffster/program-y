import unittest
from unittest.mock import patch
from unittest.mock import Mock
import os
from programy.services.rest.generic.service import GenericService
from programy.services.config import ServiceConfiguration
from programy.services.config import ServiceRESTConfiguration
from programytest.services.testclient import ServiceTestClient
from programytest.services.testcase import ServiceTestCase
from programytest.services.rest.generic.responses import generic_success_response


class GenericServiceTestClient(ServiceTestClient):

    def __init__(self):
        ServiceTestClient.__init__(self, debug=True)

    def load_storage(self):
        super(GenericServiceTestClient, self).load_storage()


class GenericServiceTests(ServiceTestCase):

    def test_init(self):
        service = GenericService(ServiceConfiguration.from_data("generic", "generic", "generic"))
        self.assertIsNotNone(service)

    def patch_requests_generic_success(self, url, headers, timeout):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = generic_success_response
        return mock_response

    @patch("programy.services.rest.base.RESTService._requests_get", patch_requests_generic_success)
    def test_search(self):
        service = GenericService(ServiceConfiguration.from_data("rest", "generic", "generic",
                                                                url="https://localhost/api?query={0}"))
        self.assertIsNotNone(service)

        client = GenericServiceTestClient()
        service.initialise(client)

        response = service.generic("Ping")
        self.assertResponse(response, 'generic', 'generic', 'generic')

