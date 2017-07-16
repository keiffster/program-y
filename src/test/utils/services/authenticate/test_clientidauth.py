import unittest

from programy.utils.services.authenticate.clientidauth import ClientIdAuthenticationService
from programy.config.sections.brain.service import BrainServiceConfiguration
from programy.brain import Brain
from programy.bot import Bot
from programy.config.sections.brain.brain import BrainConfiguration
from programy.config.sections.bot.bot import BotConfiguration

class ClientIdAuthenticationServiceTests(unittest.TestCase):

    def test_ask_question(self):
        brain = Brain(BrainConfiguration())
        bot = Bot(brain, BotConfiguration())

        config = BrainServiceConfiguration("AUTHENTICATION")
        config._additionals['denied_srai'] = "ACCESS_DENIED"

        service = ClientIdAuthenticationService(config)

        self.assertEqual("Hello", service.ask_question(bot, "console", "Hello"))

        self.assertEqual("ACCESS_DENIED", service.ask_question(bot, "unknown", "Hello"))