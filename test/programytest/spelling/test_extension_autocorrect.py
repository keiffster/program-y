import unittest

from programy.bot import Bot
from programy.config.bot.bot import BotConfiguration
from programy.spelling.extension import SpellingExtension

from programytest.client import TestClient
from programy.spelling.autocorrection import AutoCorrectSpellingChecker


class AutocorrectSpellingExtensionTests(unittest.TestCase):

    def setUp(self):
        self._client = TestClient()

        config = BotConfiguration()

        self.client_context = self._client.create_client_context("testuser")

        self.client_context._bot = Bot(config=config, client=self._client)
        self.client_context._bot._spell_checker = AutoCorrectSpellingChecker()

    def test_invalid_command(self):

        extension = SpellingExtension()
        self.assertIsNotNone(extension)

        result = extension.execute(self.client_context, "XXX")
        self.assertIsNotNone(result)
        self.assertEqual("SPELLING CORRECT INVALID COMMAND", result)

        result = extension.execute(self.client_context, "SPELLING")
        self.assertIsNotNone(result)
        self.assertEqual("SPELLING CORRECT INVALID COMMAND", result)

        result = extension.execute(self.client_context, "SPELLING CORRECT")
        self.assertIsNotNone(result)
        self.assertEqual("SPELLING CORRECT INVALID COMMAND", result)

    def test_valid_scores_command(self):

        extension = SpellingExtension()
        self.assertIsNotNone(extension)

        result = extension.execute(self.client_context, "SPELLING ENABLED")
        self.assertIsNotNone(result)
        self.assertEqual("SPELLING ENABLED", result)

        result = extension.execute(self.client_context, "SPELLING CORRECT HAVVE")
        self.assertIsNotNone(result)
        self.assertEqual("SPELLING CORRECTED HAVE", result)
