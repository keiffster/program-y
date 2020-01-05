import unittest
from unittest.mock import patch
import programytest.externals as Externals
from programy.bot import Bot
from programy.config.bot.bot import BotConfiguration
from programy.processors.post.translate import TranslatorPostProcessor
from programytest.client import TestClient


class MockClientContext(object):

    def __init__(self, bot):
        self.bot = bot


class TranslatorPostProcessorTest(unittest.TestCase):

    def setUp(self):
        self.client = TestClient()
        config = BotConfiguration()

        config.from_translator._classname = "programy.nlp.translate.textblob_translator.TextBlobTranslator"
        config.from_translator._from_lang = "fr"
        config.from_translator._to_lang = "en"

        config.to_translator._classname = "programy.nlp.translate.textblob_translator.TextBlobTranslator"
        config.to_translator._from_lang = "en"
        config.to_translator._to_lang = "fr"

        self.bot = Bot(config=config, client=self.client)
        self.bot.initiate_translator()

    @unittest.skipIf(Externals.google_translate is False or Externals.all_externals is False, Externals.google_translate_disabled)
    def test_post_process_translate(self):
        processor = TranslatorPostProcessor()

        context = MockClientContext(self.bot)

        self.assertTrue(processor.process(context, "Hello") in ["Bonjour", "Salut"])

    def test_post_process_translate_translater_unavailable(self):
        processor = TranslatorPostProcessor()

        context = MockClientContext(self.bot)

        context.bot._to_translator = None

        self.assertFalse(processor.process(context, "Hello") in ["Bonjour", "Salut"])

    def patch_translate(self, context, translator, word_string, translator_config):
        raise Exception("Mock Exception")

    @patch("programy.processors.post.translate.TranslatorPostProcessor._translate", patch_translate)
    def test_post_process_translate_translater_exception(self):
        processor = TranslatorPostProcessor()

        context = MockClientContext(self.bot)

        self.assertEquals("Hello", processor.process(context, "Hello"))
