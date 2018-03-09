import unittest

from programy.services.requestsapi import RequestsAPI

from programytest.settings import external_services

class RequestsAPITests(unittest.TestCase):

    @unittest.skipIf(not external_services, "External service testing disabled")
    def test_requestsapi(self):
        api = RequestsAPI()
        with self.assertRaises(Exception):
            api.get("http://invalid.url.com", None)