import unittest

from programy.bot import Bot
from programy.brain import Brain
from programy.config.sections.brain.brain import BrainConfiguration
from programy.config.sections.bot.bot import BotConfiguration

from test.custom import CustomAssertions

class TestBot(Bot):

    def __init__(self):
        Bot.__init__(self, Brain(BrainConfiguration()), BotConfiguration())
        self._response = "Unknown"

    @property
    def response(self):
        return self._response

    @response.setter
    def response(self, text):
        self._response = text

    def ask_question(self, clientid, text, srai=False):
        return self._response


class TemplateTestsBaseClass(unittest.TestCase, CustomAssertions):

    def setUp(self):
        self.bot = TestBot()
        self.clientid = "testid"
