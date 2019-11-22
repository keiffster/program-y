import unittest

from programy.bot import Bot
from programy.config.bot.bot import BotConfiguration
from programy.spelling.extension import SpellingExtension
from programy.spelling.textblob_spelling import TextBlobSpellingChecker
from programytest.client import TestClient


class TextBlobSpellchecherExtensionTests(unittest.TestCase):

    def setUp(self):
        self._client = TestClient()

        config = BotConfiguration()

        self.client_context = self._client.create_client_context("testuser")

        self.client_context._bot = Bot(config=config, client=self._client)
        self.client_context._bot._spell_checker = TextBlobSpellingChecker()

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

        result = extension.execute(self.client_context, "SPELLING OTHER")
        self.assertIsNotNone(result)
        self.assertEqual("SPELLING CORRECT INVALID COMMAND", result)

    def test_spelling_enabled(self):
        extension = SpellingExtension()
        self.assertIsNotNone(extension)

        result = extension.execute(self.client_context, "SPELLING ENABLED")
        self.assertIsNotNone(result)
        self.assertEqual("SPELLING ENABLED", result)

        self.client_context.bot._spell_checker = None

        result = extension.execute(self.client_context, "SPELLING ENABLED")
        self.assertIsNotNone(result)
        self.assertEqual("SPELLING DISABLED", result)

    def test_spelling(self):

        extension = SpellingExtension()
        self.assertIsNotNone(extension)

        result = extension.execute(self.client_context, "SPELLING CORRECT HALLO")
        self.assertIsNotNone(result)
        self.assertEqual("SPELLING CORRECTED HALLO", result)

    def test_spelling_disabled(self):

        extension = SpellingExtension()
        self.assertIsNotNone(extension)

        self.client_context.bot._spell_checker = None

        result = extension.execute(self.client_context, "SPELLING CORRECT HAVVE")
        self.assertIsNotNone(result)
        self.assertEqual("SPELLING UNCORRECTED HAVVE", result)
