import os

from programy.clients.client import BotClient
from programy.clients.config import ClientConfigurationData
from programytest.clients.arguments import MockArgumentParser


class MockClientConfiguration(ClientConfigurationData):

    def __init__(self):
        ClientConfigurationData.__init__(self, "mock")


class MockBotClient(BotClient):

    def __init__(self, argument_parser=None):
        BotClient.__init__(self, "mock", argument_parser)

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


class MockConfigFiles(object):

    @staticmethod
    def get_config_files(testclient):
        if os.name == 'posix':
            logging_file = os.path.dirname(__file__) + os.sep + "logging.yaml"
            testclient.assertTrue(os.path.exists(logging_file))
            config_file = os.path.dirname(__file__) + os.sep + "config.yaml"
            testclient.assertTrue(os.path.exists(config_file))
        elif os.name == 'nt':
            logging_file = os.path.dirname(__file__) + os.sep + "logging.windows.yaml"
            testclient.assertTrue(os.path.exists(logging_file))
            config_file = os.path.dirname(__file__) + os.sep + "config.windows.yaml"
            testclient.assertTrue(os.path.exists(config_file))
        else:
            raise Exception("Unknown os [%s]" % os.name)

        return config_file, logging_file

    @staticmethod
    def get_commandline_args(config_file = None, logging_file = None):
        return MockArgumentParser(bot_root=None,
                                  logging=logging_file,
                                  config=config_file,
                                  cformat="yaml",
                                  noloop=False)

