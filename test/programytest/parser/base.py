import unittest

from programy.bot import Bot
from programy.brain import Brain
from programytest.custom import CustomAssertions
from programy.config.sections.brain.brain import BrainConfiguration
from programy.config.sections.bot.bot import BotConfiguration
from programy.parser.aiml_parser import AIMLParser

class TestBot(Bot):

    def __init__(self, brain, bot_config):
        Bot.__init__(self, brain, bot_config)
        self._response = "Unknown"

    @property
    def response(self):
        return self._response

    @response.setter
    def response(self, text):
        self._response = text

    def ask_question(self, clientid, text, srai=False):
        return self._response


class ParserTestsBaseClass(unittest.TestCase, CustomAssertions):

    def setUp(self):
        self._clientid = "testid"
        self._brain = Brain(BrainConfiguration())
        self._bot = TestBot(self._brain, BotConfiguration())
        self._aiml_parser = AIMLParser(self._brain)
