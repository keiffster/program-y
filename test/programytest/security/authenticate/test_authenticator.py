import unittest

from programy.security.authenticate.authenticator import Authenticator
from programy.config.sections.brain.security import BrainSecurityConfiguration
from programy.bot import Bot
from programy.brain import Brain
from programy.config.sections.bot.bot import BotConfiguration
from programy.config.sections.brain.brain import BrainConfiguration

class AuthenticatorTests(unittest.TestCase):

    def test_authenticator_with_empty_config(self):
        testbot = Bot(Brain(BrainConfiguration()), BotConfiguration())
        service = Authenticator(BrainSecurityConfiguration("authentication"))
        self.assertIsNotNone(service)
        self.assertIsNotNone(service.configuration)
        self.assertIsNone(service.get_default_denied_srai())
        self.assertFalse(service.authenticate(testbot, "console"))
