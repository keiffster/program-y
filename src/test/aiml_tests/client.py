import logging

from programy.clients import BotClient
from programy.bot import Bot
from programy.brain import Brain
from programy.config import ClientConfiguration

class TestClient(BotClient):

    def __init__(self):
        BotClient.__init__(self)

    def parse_arguements(self):
        client_args = {}
        return client_args

    def initiate_logging(self, arguments):
        pass

    def load_configuration(self, arguments):
        self.configuration = ClientConfiguration()

        self.configuration.brain_configuration._supress_warnings = False

        self.configuration.brain_configuration._aiml_files = None
        self.configuration.brain_configuration._set_files = None
        self.configuration.brain_configuration._map_files = None

        self.configuration.brain_configuration._denormal = None
        self.configuration.brain_configuration._normal = None
        self.configuration.brain_configuration._gender = None
        self.configuration.brain_configuration._person = None
        self.configuration.brain_configuration._person2 = None
        self.configuration.brain_configuration._predicates = None
        self.configuration.brain_configuration._pronouns = None
        self.configuration.brain_configuration._properties = None
        self.configuration.brain_configuration._triples = None
        self.configuration.brain_configuration._preprocessors = None

        self.configuration.bot_configuration.default_response = ""

    def initiate_bot(self, configuration):
        brain = Brain(configuration.brain_configuration)
        self.bot = Bot(brain, config=configuration.bot_configuration)
