import unittest
import os

from programy.config.sections.brain.security import BrainSecurityConfiguration
from programy.security.authenticate.authenticator import Authenticator

from programytest.aiml_tests.client import TestClient

class MockAuthenticationService(Authenticator):

    AUTHENTICATION_SUCCESS = False

    def __init__(self, configuration: BrainSecurityConfiguration):
        Authenticator.__init__(self, configuration)

    def authenticate(self, bot, clientid: str):
        return MockAuthenticationService.AUTHENTICATION_SUCCESS


class AuthenticateTestClient(TestClient):

    def __init__(self):
        TestClient.__init__(self)

    def load_configuration(self, arguments):
        super(AuthenticateTestClient, self).load_configuration(arguments)
        self.configuration.brain_configuration.files.aiml_files._files = [os.path.dirname(__file__)]
        self.configuration.brain_configuration.security._authentication = BrainSecurityConfiguration("authentication")
        self.configuration.brain_configuration.security.authentication._classname = "programytest.aiml_tests.authenticate_tests.test_authenticate_aiml.MockAuthenticationService"
        self.configuration.brain_configuration.security.authentication._denied_srai = "AUTHENTICATED_FAILED"


class AuthenticateAIMLTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        AuthenticateAIMLTests.test_client = AuthenticateTestClient()

    def test_authentication_passed(self):
        MockAuthenticationService.AUTHENTICATION_SUCCESS = True

        response = AuthenticateAIMLTests.test_client.bot.ask_question("console", "AUTHENTICATE PASSED")
        self.assertIsNotNone(response)
        self.assertEqual(response, 'User allowed')

    def test_authentication_failed_with_srai(self):
        MockAuthenticationService.AUTHENTICATION_SUCCESS = False
        AuthenticateAIMLTests.test_client.bot.brain.authentication.configuration._denied_srai = "AUTHENTICATED_FAILED"
        AuthenticateAIMLTests.test_client.bot.brain.authentication.configuration._denied_text = "AUTHENTICATED FAILED TEXT"

        response = AuthenticateAIMLTests.test_client.bot.ask_question("console", "AUTHENTICATE FAIL SRAI")
        self.assertIsNotNone(response)
        self.assertEqual(response, 'Authentication failed')

    def test_authentication_failed_with_unknown_srai(self):
        MockAuthenticationService.AUTHENTICATION_SUCCESS = False
        AuthenticateAIMLTests.test_client.bot.brain.authentication.configuration._denied_srai = "AUTHENTICATED_FAILEDX"
        AuthenticateAIMLTests.test_client.bot.brain.authentication.configuration._denied_text = "AUTHENTICATED FAILED TEXT"

        response = AuthenticateAIMLTests.test_client.bot.ask_question("console", "AUTHENTICATE FAIL SRAI")
        self.assertIsNotNone(response)
        self.assertEqual(response, 'AUTHENTICATED FAILED TEXT')

    def test_authentication_failed_with_text(self):
        MockAuthenticationService.AUTHENTICATION_SUCCESS = False
        AuthenticateAIMLTests.test_client.bot.brain.authentication.configuration._denied_srai = None
        AuthenticateAIMLTests.test_client.bot.brain.authentication.configuration._denied_text = "AUTHENTICATED FAILED TEXT"

        response = AuthenticateAIMLTests.test_client.bot.ask_question("console", "AUTHENTICATE FAIL TEXT")
        self.assertIsNotNone(response)
        self.assertEqual(response, 'AUTHENTICATED FAILED TEXT')
