import unittest
import os

from programy.utils.license.keys import LicenseKeys
from programy.utils.services.rest import GenericRESTService
from programy.utils.services.service import BrainServiceConfiguration

class TestBot:

    def __init__(self):
        self.license_keys = None


class MockRestResponse(object):
    def __init__(self, status_code, text):
        self.status_code = status_code
        self.text = text


class MockRestAPI(object):
    def get(self, host, data):
        return MockRestResponse(200, "Test REST response")

    def post(host, data):
        return MockRestResponse(200, "Test REST response")


class RestServiceTests(unittest.TestCase):

    def setUp(self):
        self.bot = TestBot()
        self.bot.license_keys = LicenseKeys()
        self.bot.license_keys.load_license_key_file(os.path.dirname(__file__)+"/test.keys")

    def test_ask_question(self):
        config = BrainServiceConfiguration("rest")
        config.set_parameter("host", "127.0.0.1")
        config.set_parameter("method", "GET")

        service = GenericRESTService(config=config, api=MockRestAPI())
        self.assertIsNotNone(service)

        response = service.ask_question(self.bot, "testid", "what is a cat")
        self.assertEquals("Test REST response", response)