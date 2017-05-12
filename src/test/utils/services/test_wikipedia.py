import unittest
import os

from programy.utils.license.keys import LicenseKeys
from programy.utils.services.wikipediaservice import WikipediaService

class TestBot:

    def __init__(self):
        self.license_keys = None

class MockWikipediaAPI(object):

    def summary(self, title, sentences=0, chars=0, auto_suggest=True, redirect=True):
        return "Test Wikipedia response"

class WikipediaServiceTests(unittest.TestCase):

    def setUp(self):
        self.bot = TestBot()
        self.bot.license_keys = LicenseKeys()
        self.bot.license_keys.load_license_key_file(os.path.dirname(__file__)+"/test.keys")

    def test_ask_question(self):
        service = WikipediaService(api=MockWikipediaAPI())
        self.assertIsNotNone(service)

        response = service.ask_question(self.bot, "testid", "what is a cat")
        self.assertEquals("Test Wikipedia response", response)