import unittest
import unittest.mock

from programy.clients.client import BotFactory
from programy.config.bot.bot import BotConfiguration
from programy.bot import Bot

from programytest.clients.arguments import MockArgumentParser
from programytest.clients.mocks import MockBotClient


class BotFactoryTests(unittest.TestCase):

    def test_empty_config_init(self):
        arguments = MockArgumentParser()
        client = MockBotClient(arguments)

        configuration = unittest.mock.Mock()

        configuration.configurations = []

        configuration.bot_selector = "programy.clients.client.DefaultBotSelector"

        factory = BotFactory(client, configuration)
        self.assertIsNotNone(factory)

        bot = factory.select_bot()
        self.assertIsNone(bot)

    def test_config_init(self):
        arguments = MockArgumentParser()
        client = MockBotClient(arguments)

        configuration = unittest.mock.Mock()

        configuration.configurations = [BotConfiguration()]

        configuration.bot_selector = "programy.clients.client.DefaultBotSelector"

        factory = BotFactory(client, configuration)
        self.assertIsNotNone(factory)

        bot = factory.select_bot()
        self.assertIsNotNone(bot)
        self.assertIsInstance(bot, Bot)
