import unittest
import os

from programy.context import ClientContext
from programy.config.brain.security import BrainSecurityAuthenticationConfiguration
from programy.security.authenticate.authenticator import Authenticator

from programytest.aiml_tests.client import TestClient

class MockAuthenticationService(Authenticator):

    AUTHENTICATION_SUCCESS = False

    def __init__(self, configuration: BrainSecurityAuthenticationConfiguration):
        Authenticator.__init__(self, configuration)

    def authenticate(self, context: str):
        return MockAuthenticationService.AUTHENTICATION_SUCCESS


class AuthenticateTestClient(TestClient):

    def __init__(self):
        TestClient.__init__(self)

    def load_configuration(self, arguments):
        super(AuthenticateTestClient, self).load_configuration(arguments)
        self.configuration.client_configuration.configurations[0].configurations[0].files.aiml_files._files = [os.path.dirname(__file__)]
        self.configuration.client_configuration.configurations[0].configurations[0].security._authentication = BrainSecurityAuthenticationConfiguration("authentication")
        self.configuration.client_configuration.configurations[0].configurations[0].security.authentication._classname = "programytest.aiml_tests.authenticate_tests.test_authenticate_aiml.MockAuthenticationService"
        self.configuration.client_configuration.configurations[0].configurations[0].security.authentication._denied_srai = "AUTHENTICATED_FAILED"


class AuthenticateAIMLTests(unittest.TestCase):

    def setUp(self):
        client = AuthenticateTestClient()
        self._client_context = client.create_client_context("testid")

    def test_authentication_passed(self):
        MockAuthenticationService.AUTHENTICATION_SUCCESS = True

        response = self._client_context.bot.ask_question(self._client_context, "AUTHENTICATE PASSED")
        self.assertIsNotNone(response)
        self.assertEqual(response, 'User allowed')

    def test_authentication_failed_with_srai(self):
        MockAuthenticationService.AUTHENTICATION_SUCCESS = False
        self._client_context.bot.brain.authentication.configuration._denied_srai = "AUTHENTICATED_FAILED"
        self._client_context.bot.brain.authentication.configuration._denied_text = "AUTHENTICATED FAILED TEXT"

        response = self._client_context.bot.ask_question(self._client_context, "AUTHENTICATE FAIL SRAI")
        self.assertIsNotNone(response)
        self.assertEqual(response, 'Authentication failed')

    def test_authentication_failed_with_unknown_srai(self):
        MockAuthenticationService.AUTHENTICATION_SUCCESS = False
        self._client_context.bot.brain.authentication.configuration._denied_srai = "AUTHENTICATED_FAILEDX"
        self._client_context.bot.brain.authentication.configuration._denied_text = "AUTHENTICATED FAILED TEXT"

        response = self._client_context.bot.ask_question(self._client_context, "AUTHENTICATE FAIL SRAI")
        self.assertIsNotNone(response)
        self.assertEqual(response, 'AUTHENTICATED FAILED TEXT')

    def test_authentication_failed_with_text(self):
        MockAuthenticationService.AUTHENTICATION_SUCCESS = False
        self._client_context.bot.brain.authentication.configuration._denied_srai = None
        self._client_context.bot.brain.authentication.configuration._denied_text = "AUTHENTICATED FAILED TEXT"

        response = self._client_context.bot.ask_question(self._client_context, "AUTHENTICATE FAIL TEXT")
        self.assertIsNotNone(response)
        self.assertEqual(response, 'AUTHENTICATED FAILED TEXT')
