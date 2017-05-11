import unittest
import os

from programy.utils.license.keys import LicenseKeys
from programy.utils.newsapi.newsapi import NewsAPI

class NewsAPIExtensionTests(unittest.TestCase):

    def setUp(self):
        self.license_keys = LicenseKeys()
        self.license_keys.load_license_key_file(os.path.dirname(__file__)+"/test.keys")

    def test_init(self):
        newsapi = NewsAPI(self.license_keys)
        self.assertIsNotNone(newsapi)