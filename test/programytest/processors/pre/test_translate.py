import unittest

import programytest.externals as Externals
from programy.bot import Bot
from programy.config.bot.bot import BotConfiguration
from programy.processors.pre.translate import TranslatorPreProcessor
from programytest.client import TestClient


class MockClientContext(object):

    def __init__(self, bot):
        self.bot = bot


class MockTranslatorPreProcessor(TranslatorPreProcessor):

    def __init__(self):
        TranslatorPreProcessor.__init__(self)

    def _translate(self, context, translator, translator_config, word_string):
        raise Exception("Mock Exception")


class TranslatorPreProcessorTest(unittest.TestCase):

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
    def test_pre_process_translate(self):
        processor = TranslatorPreProcessor()

        context = MockClientContext(self.bot)

        self.assertEqual("Hello", processor.process(context, "Bonjour"))

    def test_pre_process_translate_disabled(self):
        processor = TranslatorPreProcessor()

        context = MockClientContext(self.bot)
        context.bot._from_translator = None

        self.assertEqual("Hello", processor.process(context, "Hello"))

    def test_pre_process_translate_exception(self):
        processor = MockTranslatorPreProcessor()

        context = MockClientContext(self.bot)

        self.assertEqual("Hello", processor.process(context, "Hello"))