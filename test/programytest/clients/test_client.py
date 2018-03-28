import unittest
import unittest.mock
import os

from programy.clients.client import BotClient
from programy.clients.client import DefaultBotSelector
from programy.clients.client import BotFactory
from programy.config.bot.bot import BotConfiguration
from programy.bot import Bot

from programytest.clients.arguments import MockArgumentParser
from programy.config.client.config import ClientConfigurationData


class MockClientConfiguration(ClientConfigurationData):

    def __init__(self):
        ClientConfigurationData.__init__(self, "console")

    def load_configuration(self, configuration_file, bot_root):
        console = configuration_file.get_section(self.section_name)
        super(MockClientConfiguration, self).load_configuration(configuration_file, console, bot_root)


class MockBotClient(BotClient):

    def __init__(self, argument_parser=None):
        BotClient.__init__(self, "Mock", argument_parser)

    def get_description(self):
        return "ProgramY Test Client"

    def set_environment(self):
        self.bot.brain.properties.add_property("env", "Mock")

    def get_client_configuration(self):
        return MockClientConfiguration()

    def set_environment(self):
        """For testing purposes we do nothing"""
        return

    def run(self):
        """For testing purposes we do nothing"""
        return


class DefaultBotSelectorTests(unittest.TestCase):

    def test_init(self):
        configuration = unittest.mock.Mock()

        selector = DefaultBotSelector(configuration)
        self.assertIsNotNone(selector)

        bot1 = unittest.mock.Mock()
        bot2 = unittest.mock.Mock()

        bots = {"one": bot1, "two": bot2}
        self.assertEquals(bot1, selector.select_bot(bots))


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


class BotClientTests(unittest.TestCase):

    def test_client_init(self):
        arguments = MockArgumentParser()
        with self.assertRaises(Exception):
            client = BotClient("test", arguments)

    def test_sub_classed_client(self):

        if os.name == 'posix':
            logging_file = os.path.dirname(__file__) + os.sep + "logging.yaml"
            config_file = os.path.dirname(__file__) + os.sep + "config.yaml"
        elif os.name == 'nt':
            logging_file = os.path.dirname(__file__) + os.sep + "logging.windows.yaml"
            config_file = os.path.dirname(__file__) + os.sep + "config.windows.yaml"
        else:
            raise Exception("Unknown os [%s]" % os.name)

        arguments = MockArgumentParser(bot_root=".",
                                       logging=logging_file,
                                       config=config_file,
                                       cformat="yaml",
                                       noloop=False)
        client = MockBotClient(arguments)
        self.assertIsNotNone(client)
        self.assertIsNotNone(client.arguments)

        self.assertIsNotNone(client.arguments)
        self.assertEquals("ProgramY Test Client", client.get_description())

        client.run()
        client.log_response(None, None)
        client.log_unknown_response(None)

    def test_sub_classed_client_no_bot_root(self):
        if os.name == 'posix':
            logging_file = os.path.dirname(__file__) + os.sep + "logging.yaml"
            config_file = os.path.dirname(__file__) + os.sep + "config.yaml"
        elif os.name == 'nt':
            logging_file = os.path.dirname(__file__) + os.sep + "logging.windows.yaml"
            config_file = os.path.dirname(__file__) + os.sep + "config.windows.yaml"
        else:
            raise Exception("Unknown os [%s]" % os.name)

        arguments = MockArgumentParser(bot_root=None,
                                       logging=logging_file,
                                       config=config_file,
                                       cformat="yaml",
                                       noloop=False)
        client = MockBotClient(arguments)
        self.assertIsNotNone(client)
        self.assertIsNotNone(client.arguments)

    def test_sub_classed_client_no_bot_root_no_config(self):
        if os.name == 'posix':
            logging_file = os.path.dirname(__file__) + os.sep + "logging.yaml"
        elif os.name == 'nt':
            logging_file = os.path.dirname(__file__) + os.sep + "logging.windows.yaml"
        else:
            raise Exception("Unknown os [%s]" % os.name)

        arguments = MockArgumentParser(bot_root=None,
                                       logging=logging_file,
                                       config=None,
                                       cformat="yaml",
                                       noloop=False)
        client = MockBotClient(arguments)
        self.assertIsNotNone(client)
        self.assertIsNotNone(client.arguments)
