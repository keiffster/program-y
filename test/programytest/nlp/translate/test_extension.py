import unittest

from programy.bot import Bot
from programy.config.bot.bot import BotConfiguration
from programy.nlp.translate.extension import TranslateExtension

from programytest.client import TestClient

import programytest.externals as Externals


class TranslateExtensionTests(unittest.TestCase):

    def setUp(self):
        self._client = TestClient()

        config = BotConfiguration()
        config._from_translator._classname = "programy.nlp.translate.textblob_translator.TextBlobTranslator"

        self.client_context = self._client.create_client_context("testuser")

        self.client_context._bot = Bot(config=config, client=self._client)
        self.client_context._bot.initiate_translator()

    def test_invalid_command(self):

        extension = TranslateExtension()
        self.assertIsNotNone(extension)

        result = extension.execute(self.client_context, "XXX")
        self.assertIsNotNone(result)
        self.assertEqual("TRANSLATE INVALID COMMAND", result)

        result = extension.execute(self.client_context, "TRANSLATE")
        self.assertIsNotNone(result)
        self.assertEqual("TRANSLATE INVALID COMMAND", result)

        result = extension.execute(self.client_context, "TRANSLATE FROM")
        self.assertIsNotNone(result)
        self.assertEqual("TRANSLATE INVALID COMMAND", result)

        result = extension.execute(self.client_context, "TRANSLATE FROM EN")
        self.assertIsNotNone(result)
        self.assertEqual("TRANSLATE INVALID COMMAND", result)

        result = extension.execute(self.client_context, "TRANSLATE FROM EN TO")
        self.assertIsNotNone(result)
        self.assertEqual("TRANSLATE INVALID COMMAND", result)

        result = extension.execute(self.client_context, "TRANSLATE FROM EN TO FR")
        self.assertIsNotNone(result)
        self.assertEqual("TRANSLATE INVALID COMMAND", result)

    @unittest.skipIf(Externals.google_translate is False, Externals.google_translate_disabled)
    def test_valid_scores_command(self):

        extension = TranslateExtension()
        self.assertIsNotNone(extension)

        result = extension.execute(self.client_context, "TRANSLATE ENABLED")
        self.assertIsNotNone(result)
        self.assertEqual("TRANSLATE ENABLED", result)

        result = extension.execute(self.client_context, "TRANSLATE FROM EN TO FR HELLO I LOVE YOU")
        self.assertIsNotNone(result)
        self.assertEqual("TRANSLATED SALUT JE T'AIME", result)
