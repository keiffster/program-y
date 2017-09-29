import unittest
import os

from programy.clients.client import BotClient

from programytest.clients.arguments import MockArgumentParser
from programy.config.base import BaseConfigurationData

class MockBaseConfigurationData(BaseConfigurationData):

    def __init__(self, name):
        BaseConfigurationData.__init__(self, name)

    def load_configuration(self, config_file, bot_root):
        return

class MockBotClient(BotClient):

    def __init__(self, argument_parser=None):
        BotClient.__init__(self, "Mock", argument_parser=argument_parser)

    def get_client_configuration(self):
        return MockBaseConfigurationData("mock")

    def load_configuration(self, arguments):
        super(MockBotClient, self).load_configuration(arguments)
        if os.name == 'posix':
            self.configuration.brain_configuration.braintree._file = "/tmp/tmp_braintree.txt"
        elif os.name == 'nt':
            self.configuration.brain_configuration.braintree._file = "C:\Windows\Temp\tmp_braintree.txt"
        else:
            raise Exception("Unknown os [%s]" % os.name)

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

        arguments = MockArgumentParser(bot_root = ".",
                                       logging=logging_file,
                                       config=config_file,
                                       cformat="yaml",
                                       noloop=False)
        client = MockBotClient(arguments)
        self.assertIsNotNone(client)
        self.assertIsNotNone(client.arguments)

        self.assertIsNotNone(client.arguments)
        self.assertEquals("ProgramY AIML2.0 Console Client", client.get_description())

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
