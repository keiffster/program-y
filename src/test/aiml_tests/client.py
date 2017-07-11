import logging

from programy.clients.client import BotClient
from programy.config.programy import ProgramyConfiguration
from programy.config.sections.client.console import ConsoleConfiguration

class TestClient(BotClient):

    def __init__(self, debug=False, level=logging.DEBUG):
        if debug is True:
            logging.getLogger().setLevel(level)
        BotClient.__init__(self)

    def parse_arguments(self, argument_parser):
        client_args = {}
        return client_args

    def initiate_logging(self, arguments):
        pass

    def load_configuration(self, arguments):
        self.configuration = ProgramyConfiguration(ConsoleConfiguration())

    def dump_bot_brain_tree(self):
        self.bot.brain.dump_tree()