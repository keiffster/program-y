import unittest

from programy.bot import Bot
from programytest.custom import CustomAssertions
from programy.config.bot.bot import BotConfiguration
from programy.context import ClientContext
from programytest.client import TestClient


class TestBot(Bot):

    def __init__(self, bot_config, client):
        Bot.__init__(self, bot_config, client)
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
        client = TestClient()
        client.add_default_stores()
        self._client_context = ClientContext(client, "testid")
        self._client_context.bot = TestBot(BotConfiguration(), client)
        self._client_context.brain = self._client_context.bot.brain

