import unittest

from programy.security.authenticate.authenticator import Authenticator
from programy.config.brain.security import BrainSecurityConfiguration
from programy.bot import Bot
from programy.brain import Brain
from programy.config.bot.bot import BotConfiguration
from programy.config.brain.brain import BrainConfiguration
from programy.context import ClientContext

from programytest.aiml_tests.client import TestClient

class AuthenticatorTests(unittest.TestCase):

    def test_authenticator_with_empty_config(self):
        client_context = ClientContext(TestClient(), "console")
        client_context.bot = Bot(BotConfiguration())
        client_context.bot.configuration.conversations._max_histories = 3
        client_context.brain = client_context.bot.brain

        service = Authenticator(BrainSecurityConfiguration("authentication"))
        self.assertIsNotNone(service)
        self.assertIsNotNone(service.configuration)
        self.assertIsNone(service.get_default_denied_srai())
        self.assertFalse(service.authenticate(client_context))
