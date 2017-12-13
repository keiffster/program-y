import unittest
import os

from programy.utils.license.keys import LicenseKeys
from programy.services.duckduckgo import DuckDuckGoService
from programytest.settings import external_services
from programy.services.service import BrainServiceConfiguration

class TestBot:

    def __init__(self):
        self.license_keys = None

class MockDuckDuckGoAPI(object):

    def __init__(self, response=None, throw_exception=False):
        self._response = response
        self._throw_exception = throw_exception

    def ask_question(self, url, question):
        if self._throw_exception is True:
            raise Exception()
        else:
            return self._response

class DuckDuckGoServiceTests(unittest.TestCase):

    def setUp(self):
        self.bot = TestBot()
        self.bot.license_keys = LicenseKeys()
        self.bot.license_keys.load_license_key_file(os.path.dirname(__file__)+ os.sep + "test.keys")

    def test_ask_question(self):

        config = BrainServiceConfiguration("pannous")
        config._url = "http://test.pandora.url"

        service = DuckDuckGoService(config=config, api=MockDuckDuckGoAPI(response="Test DuckDuckGo response"))
        self.assertIsNotNone(service)

        response = service.ask_question(self.bot, "testid", "what is a cat")
        self.assertEquals("Test DuckDuckGo response", response)

    def test_ask_question_general_exception(self):
        config = BrainServiceConfiguration("pannous")
        config._url = "http://test.pandora.url"

        service = DuckDuckGoService(config=config, api=MockDuckDuckGoAPI(response=None, throw_exception=True))
        self.assertIsNotNone(service)

        response = service.ask_question(self.bot, "testid", "what is a cat")
        self.assertEquals("", response)

    @unittest.skipIf(not external_services, "External service testing disabled")
    def test_ask_question_summary(self):
        config = BrainServiceConfiguration("pannous")
        config._url = "http://api.duckduckgo.com"

        service = DuckDuckGoService(config=config)
        self.assertIsNotNone(service)

        response = service.ask_question(self.bot, "testid", "cat")
        self.assertIsNotNone(response)
        self.assertEqual("Cat A small, typically furry, carnivorous mammal", response)
