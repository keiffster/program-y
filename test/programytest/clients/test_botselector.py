import unittest

from programy.config.bot.bot import BotConfiguration
from programy.bot import Bot
from programy.clients.botfactory import DefaultBotSelector

from programy.clients.config import ClientConfigurationData

from programytest.clients.mocks import MockBotClient, MockConfigFiles


class DefaultBotSelectorTests(unittest.TestCase):

    def test_selection_no_bot(self):

        config = ClientConfigurationData(name="test")
        selector = DefaultBotSelector(config, {})

        selected = selector.select_bot()

        self.assertIsNone(selected)

    def test_selection_single_bot(self):
        config_file, logging_file = MockConfigFiles.get_config_files(self)
        arguments = MockConfigFiles.get_commandline_args(None, logging_file)
        client = MockBotClient(arguments)

        bot1 = Bot(BotConfiguration(), client)
        bots = {"bot1": bot1}

        config = ClientConfigurationData(name="test")
        selector = DefaultBotSelector(config, bots)

        selected = selector.select_bot()

        self.assertIsNotNone(selected)
        self.assertEquals(selected, bot1)

        selected = selector.select_bot()

        self.assertIsNotNone(selected)
        self.assertEquals(selected, bot1)

    def test_selection_multi_bot(self):
        config_file, logging_file = MockConfigFiles.get_config_files(self)
        arguments = MockConfigFiles.get_commandline_args(None, logging_file)
        client = MockBotClient(arguments)

        bot1 = Bot(BotConfiguration(), client)
        bot2 = Bot(BotConfiguration(), client)
        bot3 = Bot(BotConfiguration(), client)
        bots = {"bot1": bot1, "bot2": bot2, "bot3": bot3}

        config = ClientConfigurationData(name="test")
        selector = DefaultBotSelector(config, bots)

        selected = selector.select_bot()
        self.assertIsNotNone(selected)
        self.assertEquals(selected, bot1)

        selected = selector.select_bot()
        self.assertIsNotNone(selected)
        self.assertEquals(selected, bot2)

        selected = selector.select_bot()
        self.assertIsNotNone(selected)
        self.assertEquals(selected, bot3)

        selected = selector.select_bot()
        self.assertIsNotNone(selected)
        self.assertEquals(selected, bot1)
