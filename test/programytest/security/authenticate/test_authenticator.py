import unittest

from programy.security.authenticate.authenticator import Authenticator
from programy.config.brain.security import BrainSecurityConfiguration
from programy.bot import Bot
from programy.config.bot.bot import BotConfiguration
from programy.context import ClientContext

from programytest.client import TestClient

class AuthenticatorTests(unittest.TestCase):

    def test_authenticator_with_empty_config(self):
        client = TestClient()
        client_context = ClientContext(client, "console")
        client_context.bot = Bot(BotConfiguration(), client)
        client_context.bot.configuration.conversations._max_histories = 3
        client_context.brain = client_context.bot.brain

        service = Authenticator(BrainSecurityConfiguration("authentication"))
        self.assertIsNotNone(service)
        self.assertIsNotNone(service.configuration)
        self.assertIsNone(service.get_default_denied_srai())
        self.assertFalse(service.authenticate(client_context))
