import unittest
import os

from programy.utils.license.keys import LicenseKeys
from programy.utils.services.pandora import PandoraService
from programy.utils.services.service import BrainServiceConfiguration

class TestBot:

    def __init__(self):
        self.license_keys = None

class MockPandoraAPI(object):

    def ask_question(self, url, question, botid):
        return "Test pandora response"

class PandoraServiceTests(unittest.TestCase):

    def setUp(self):
        self.bot = TestBot()
        self.bot.license_keys = LicenseKeys()
        self.bot.license_keys.load_license_key_file(os.path.dirname(__file__)+"/test.keys")

    def test_ask_question(self):

        config = BrainServiceConfiguration("pandora")
        config.set_parameter("url", "http://test.pandora.url")

        service = PandoraService(config=config, api=MockPandoraAPI())
        self.assertIsNotNone(service)

        response = service.ask_question(self.bot, "testid", "what is a cat")
        self.assertEquals("Test pandora response", response)