import unittest
import os
from programy.clients.clients import BotClient

class MockArguments(object):

    def __init__(self, bot_root = ".", logging=None, config=None, cformat="yaml", noloop = False ):
        self.bot_root = bot_root
        self.logging = logging
        self.config = config
        self.cformat = cformat
        self.noloop = noloop

class MockArgumentParser(object):

    def __init__(self, bot_root = ".", logging=None, config=None, cformat="yaml", noloop=False):
        self.bot_root = bot_root
        self.logging = logging
        self.config = config
        self.cformat = cformat
        self.noloop = noloop

    def add_argument(self, argument, dest=None, action=None, help=None):
        pass

    def parse_args(self):
        return MockArguments(bot_root=self.bot_root, logging=self.logging, config=self.config, cformat=self.cformat, noloop=self.noloop )

class BotClientTests(unittest.TestCase):

    def test_bot_client_default_values(self):
        bot_client = BotClient(argument_parser=MockArgumentParser())
        self.assertIsNotNone(bot_client)
        self.assertIsNotNone(bot_client.arguments)
        self.assertEqual("ProgramY AIML2.0 Console Client", bot_client.get_description())
        self.assertIsNotNone(bot_client.get_client_configuration())

    def test_bot_client_config_files(self):
        bot_client = BotClient(argument_parser=MockArgumentParser(
            logging=os.path.dirname(__file__) + "/logging.yaml",
            config=os.path.dirname(__file__) + "/config.yaml"
        ))
        self.assertIsNotNone(bot_client)
        self.assertIsNotNone(bot_client.arguments)
        self.assertEqual("ProgramY AIML2.0 Console Client", bot_client.get_description())
        self.assertIsNotNone(bot_client.get_client_configuration())

    def test_bot_client_no_bot_root(self):
        bot_client = BotClient(argument_parser=MockArgumentParser(
            bot_root=None,
            config=os.path.dirname(__file__) + "/config.yaml"
        ))
        self.assertIsNotNone(bot_client)
        self.assertIsNotNone(bot_client.arguments)
        self.assertEqual(os.path.dirname(__file__) , bot_client.arguments.bot_root)

    def test_bot_client_no_bot_root_no_config_file(self):
        bot_client = BotClient(argument_parser=MockArgumentParser(
            bot_root=None
        ))
        self.assertIsNotNone(bot_client)
        self.assertIsNotNone(bot_client.arguments)
        self.assertEqual(".", bot_client.arguments.bot_root)

    def test_empty_methods(self):
        bot_client = BotClient(argument_parser=MockArgumentParser())
        bot_client.add_client_arguments()
        bot_client.run()
        bot_client.log_unknown_response("Hello?")
        bot_client.log_response("Hello?", "Hiya!")
