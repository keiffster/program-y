import unittest
import os

from programy.utils.license.keys import LicenseKeys
from programy.services.duckduckgo import DuckDuckGoService
from programy.services.service import BrainServiceConfiguration


class TestBot:

    def __init__(self):
        self.license_keys = None


class DuckDuckGoServiceTests(unittest.TestCase):

    def setUp(self):
        self.bot = TestBot()
        self.bot.license_keys = LicenseKeys()
        self.bot.license_keys.load_license_key_file(os.path.dirname(__file__)+ os.sep + "test.keys")

    def test_ask_question_summary(self):
        config = BrainServiceConfiguration("pannous")
        config._url = "http://api.duckduckgo.com"

        service = DuckDuckGoService(config=config)
        self.assertIsNotNone(service)

        response = service.ask_question(self.bot, "testid", "cat")
        self.assertIsNotNone(response)
        self.assertEqual("Cat A small, typically furry, carnivorous mammal", response)
