import unittest

from programy.security.authenticate.passthrough import BasicPassThroughAuthenticationService
from programy.config.sections.brain.service import BrainServiceConfiguration
from programy.bot import Bot
from programy.brain import Brain
from programy.config.sections.bot.bot import BotConfiguration
from programy.config.sections.brain.brain import BrainConfiguration


class BasicPassThroughAuthenticationServiceTests(unittest.TestCase):

    def test_service(self):
        testbot = Bot(Brain(BrainConfiguration()), BotConfiguration())

        service = BasicPassThroughAuthenticationService(BrainServiceConfiguration("authentication"))
        self.assertIsNotNone(service)
        self.assertIsNotNone(service.configuration)
        self.assertTrue(service.authenticate(testbot, "console"))
        self.assertTrue(service.authenticate(testbot, "anyone"))
