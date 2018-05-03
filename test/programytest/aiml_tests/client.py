import logging

from programy.clients.client import BotClient
from programy.config.programy import ProgramyConfiguration
from programy.clients.events.console.config import ConsoleConfiguration

class TestClient(BotClient):

    def __init__(self, debug=False, level=logging.ERROR):
        if debug is True:
            logging.getLogger().setLevel(level)
        BotClient.__init__(self, "testclient")

    def parse_arguments(self, argument_parser):
        client_args = {}
        return client_args

    def initiate_logging(self, arguments):
        pass

    def get_client_configuration(self):
        return ConsoleConfiguration()

    def load_configuration(self, arguments):
        config = ConsoleConfiguration()
        self._configuration = ProgramyConfiguration(config)

    def set_environment(self):
        """For testing purposes we do nothing"""
        return

    def run(self):
        """For testing purposes we do nothing"""
        return

    def dump_graph(self, client_context):
        client_context.brain.aiml_parser.pattern_parser.root.dump("", output_func=print)
