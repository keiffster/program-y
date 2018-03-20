import unittest
import os

from programy.utils.license.keys import LicenseKeys
from programy.services.wikipediaservice import WikipediaService

class TestBot:

    def __init__(self):
        self.license_keys = None


class WikipediaServiceTests(unittest.TestCase):

    def setUp(self):
        self.bot = TestBot()
        self.bot.license_keys = LicenseKeys()
        self.bot.license_keys.load_license_key_file(os.path.dirname(__file__)+ os.sep + "test.keys")

    def test_ask_question_summary(self):
        service = WikipediaService()
        self.assertIsNotNone(service)

        response = service.ask_question(self.bot, "testid", "SUMMARY cat")
        self.assertIsNotNone(response)
        self.assertEqual("The domestic cat (Felis silvestris catus or Felis catus) is a small, typically furry, carnivorous mammal.", response)

    def test_ask_question_search(self):
        service = WikipediaService()
        self.assertIsNotNone(service)

        response = service.ask_question(self.bot, "testid", "SEARCH cat")
        self.assertIsNotNone(response)
        self.assertTrue(response.startswith("Cat"))