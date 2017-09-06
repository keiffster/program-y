import unittest

from programy.utils.newsapi.newsapi import NewsApiApi

class RequestsAPITests(unittest.TestCase):

    def test_requestsapi(self):
        api = NewsApiApi()
        with self.assertRaises(Exception):
            api.get("http://invalid.url.com", None)

