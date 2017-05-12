import unittest
import os

from programy.utils.license.keys import LicenseKeys
from programy.utils.services.pannous import PannousService
from programy.utils.services.service import BrainServiceConfiguration

class TestBot:

    def __init__(self):
        self.license_keys = None

class MockPannousAPI(object):

    def ask_question(self, url, question, login):
        return "Test pannous response"

class PannousServiceTests(unittest.TestCase):

    def setUp(self):
        self.bot = TestBot()
        self.bot.license_keys = LicenseKeys()
        self.bot.license_keys.load_license_key_file(os.path.dirname(__file__)+"/test.keys")

    def test_ask_question(self):

        config = BrainServiceConfiguration("pannous")
        config.set_parameter("url", "http://test.pandora.url")

        service = PannousService(config=config, api=MockPannousAPI())
        self.assertIsNotNone(service)

        response = service.ask_question(self.bot, "testid", "what is a cat")
        self.assertEquals("Test pannous response", response)