import unittest

import programytest.externals as Externals
from programy.bot import Bot
from programy.config.bot.bot import BotConfiguration
from programy.nlp.translate.extension import TranslateExtension
from programytest.client import TestClient


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

        result = extension.execute(self.client_context, "OTHER FROM EN TO FR HELLO I LOVE YOU")
        self.assertIsNotNone(result)
        self.assertEqual("TRANSLATE INVALID COMMAND", result)

        result = extension.execute(self.client_context, "TRANSLATE OTHER EN TO FR HELLO I LOVE YOU")
        self.assertIsNotNone(result)
        self.assertEqual("TRANSLATE INVALID COMMAND", result)

        result = extension.execute(self.client_context, "TRANSLATE FROM EN OTHER FR HELLO I LOVE YOU")
        self.assertIsNotNone(result)
        self.assertEqual("TRANSLATE INVALID COMMAND", result)

    def test_enabled(self):
        extension = TranslateExtension()
        self.assertIsNotNone(extension)

        result = extension.execute(self.client_context, "TRANSLATE ENABLED")
        self.assertEquals("TRANSLATE ENABLED", result)

        self.client_context.bot._from_translator = None

        result = extension.execute(self.client_context, "TRANSLATE ENABLED")
        self.assertEquals("TRANSLATE DISABLED", result)

    @unittest.skipIf(Externals.google_translate is False or Externals.all_externals is False, Externals.google_translate_disabled)
    def test_translate(self):
        extension = TranslateExtension()
        self.assertIsNotNone(extension)

        result = extension.execute(self.client_context, "TRANSLATE ENABLED")
        self.assertIsNotNone(result)
        self.assertEqual("TRANSLATE ENABLED", result)

        result = extension.execute(self.client_context, "TRANSLATE FROM EN TO FR HELLO I LOVE YOU")
        self.assertIsNotNone(result)
        self.assertEqual("TRANSLATED SALUT JE T'AIME", result)

    def test_translate_disabled(self):
        extension = TranslateExtension()
        self.assertIsNotNone(extension)

        self.client_context.bot._from_translator = None

        result = extension.execute(self.client_context, "TRANSLATE FROM EN TO FR HELLO I LOVE YOU")
        self.assertIsNotNone(result)
        self.assertEqual("TRANSLATE DISABLED", result)
