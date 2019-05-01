import unittest.mock

from programy.clients.client import BotClient

from programytest.clients.arguments import MockArgumentParser
from programytest.clients.mocks import MockBotClient, MockConfigFiles


class BotClientTests(unittest.TestCase):

    def test_client_init(self):
        arguments = MockArgumentParser()
        with self.assertRaises(Exception):
            client = BotClient("test", arguments)

    def test_sub_classed_client(self):

        config_file, logging_file = MockConfigFiles.get_config_files(self)

        arguments = MockConfigFiles.get_commandline_args(None, logging_file)

        client = MockBotClient(arguments)
        self.assertIsNotNone(client)
        self.assertIsNotNone(client.arguments)

        self.assertIsNotNone(client.arguments)
        self.assertEqual("ProgramY Test Client", client.get_description())

        client.run()
        client.log_response(None, None)
        client.log_unknown_response(None)

    def test_sub_classed_client_no_bot_root(self):

        config_file, logging_file = MockConfigFiles.get_config_files(self)

        arguments = MockConfigFiles.get_commandline_args(config_file, logging_file)

        client = MockBotClient(arguments)
        self.assertIsNotNone(client)
        self.assertIsNotNone(client.arguments)

    def test_sub_classed_client_no_bot_root_no_config(self):

        config_file, logging_file = MockConfigFiles.get_config_files(self)

        arguments = MockConfigFiles.get_commandline_args(None, logging_file)

        client = MockBotClient(arguments)
        self.assertIsNotNone(client)
        self.assertIsNotNone(client.arguments)

    def test_scheduler(self):

        config_file, logging_file = MockConfigFiles.get_config_files(self)

        arguments = MockConfigFiles.get_commandline_args(config_file, logging_file)

        client = MockBotClient(arguments)

        self.assertIsNotNone(client.scheduler)

    def test_trigger_manager(self):

        config_file, logging_file = MockConfigFiles.get_config_files(self)

        arguments = MockConfigFiles.get_commandline_args(config_file, logging_file)

        client = MockBotClient(arguments)

        self.assertIsNotNone(client.trigger_manager)

        client.startup()
        client.shutdown()
