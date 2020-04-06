import unittest

from programy.bot import Bot
from programy.config.bot.bot import BotConfiguration
from programy.config.brain.security import BrainSecurityAuthenticationConfiguration
from programy.context import ClientContext
from programy.security.authenticate.passthrough import BasicPassThroughAuthenticationService
from programytest.client import TestClient


class BasicPassThroughAuthenticationServiceTests(unittest.TestCase):

    def test_service(self):
        client = TestClient()
        client_context = ClientContext(client, "unknown")
        client_context.bot = Bot(BotConfiguration(), client)
        client_context.bot.configuration.conversations._max_histories = 3
        client_context.brain = client_context.bot.brain

        service = BasicPassThroughAuthenticationService(BrainSecurityAuthenticationConfiguration("authentication"))
        self.assertIsNotNone(service)
        self.assertIsNotNone(service.configuration)
        client_context._userid = "console"
        self.assertTrue(service.authenticate(client_context))
        client_context._userid = "anyone"
        self.assertTrue(service.authenticate(client_context))
