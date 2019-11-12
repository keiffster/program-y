import unittest

from programy.activate import Activatable
from programy.bot import Bot
from programy.config.bot.bot import BotConfiguration
from programy.config.bot.spelling import BotSpellingConfiguration
from programy.context import ClientContext
from programy.dynamic.variables.system.spelling import Spelling
from programy.spelling.base import SpellingChecker
from programytest.client import TestClient


class MockSpellingChecker(SpellingChecker):

    def __init__(self, spelling_config=None):
        SpellingChecker.__init__(self, spelling_config)

    def correct(self, phrase):
        return "Hello World"


class SpellingDynamicVarTests(unittest.TestCase):

    def setUp(self):
        client = TestClient()
        self._client_context = ClientContext(client, "testid")
        self._client_context.bot = Bot(BotConfiguration(), client)

        spelling_config = BotSpellingConfiguration()
        spelling_config._classname = "programytest.spelling.test_base.MockSpellingChecker"
        self._client_context.bot._spell_checker = SpellingChecker.initiate_spellchecker(spelling_config, None)

    def test_spelling_active(self):
        dyn_var = Spelling(None)
        self.assertIsNotNone(dyn_var)
        active = dyn_var.get_value(self._client_context)
        self.assertIsNotNone(active)
        self.assertEqual(Activatable.ON, active)

        dyn_var.set_value(self._client_context, Activatable.OFF)
        active = dyn_var.get_value(self._client_context)
        self.assertIsNotNone(active)
        self.assertEqual(Activatable.OFF, active)

    def test_no_spell_checker(self):
        self._client_context.bot._spell_checker = None

        dyn_var = Spelling(None)
        self.assertIsNotNone(dyn_var)
        active = dyn_var.get_value(self._client_context)
        self.assertIsNone(active)

    def test_no_spell_checker_no_active(self):
        self._client_context.bot._spell_checker = None

        dyn_var = Spelling(None)
        self.assertIsNotNone(dyn_var)
        dyn_var.set_value(self._client_context, True)

        active = dyn_var.get_value(self._client_context)
        self.assertIsNone(active)
