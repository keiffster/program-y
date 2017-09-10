import unittest

from programy.services.requestsapi import RequestsAPI

class RequestsAPITests(unittest.TestCase):

    def test_requestsapi(self):
        api = RequestsAPI()
        with self.assertRaises(Exception):
            api.get("http://invalid.url.com", None)