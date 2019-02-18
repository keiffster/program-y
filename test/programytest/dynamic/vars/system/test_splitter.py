import unittest

from programy.dynamic.variables.system.splitter import SentenceSplitter as SentenceSplitterVar
from programy.dialog.splitter.splitter import SentenceSplitter
from programy.context import ClientContext
from programy.bot import Bot
from programy.config.bot.bot import BotConfiguration
from programy.config.bot.splitter import BotSentenceSplitterConfiguration
from programy.activate import Activatable

from programytest.client import TestClient


class SentenceSplitterDynamicVarTests(unittest.TestCase):

    def setUp(self):
        client = TestClient()
        self._client_context = ClientContext(client, "testid")
        self._client_context.bot = Bot(BotConfiguration(), client)

        config = BotSentenceSplitterConfiguration()
        self._client_context.bot._sentence_splitter = SentenceSplitter.initiate_sentence_splitter(config)

    def test_splitter_active(self):
        dyn_var = SentenceSplitterVar(None)
        self.assertIsNotNone(dyn_var)
        active = dyn_var.get_value(self._client_context)
        self.assertIsNotNone(active)
        self.assertEquals(Activatable.ON, active)

        dyn_var.set_value(self._client_context, Activatable.OFF)
        active = dyn_var.get_value(self._client_context)
        self.assertIsNotNone(active)
        self.assertEquals(Activatable.OFF, active)
