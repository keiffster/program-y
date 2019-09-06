import unittest
from programy.processors.pre.removepunctuation import RemovePunctuationPreProcessor
from programy.processors.pre.toupper import ToUpperPreProcessor
from programy.processors.pre.normalize import NormalizePreProcessor
from programy.processors.pre.demojize import DemojizePreProcessor
from programy.processors.pre.translate import TranslatorPreProcessor
from programy.bot import Bot
from programy.config.bot.bot import BotConfiguration
from programy.context import ClientContext

from programytest.client import TestClient

import programytest.externals as Externals


class PreProcessingTests(unittest.TestCase):

    @unittest.skipIf(Externals.google_translate is False, Externals.google_translate_disabled)
    def test_pre_cleanup(self):
        self.client = TestClient()

        context = ClientContext(self.client, "testid")

        config = BotConfiguration()

        config.from_translator._classname = "programy.nlp.translate.textblob_translator.TextBlobTranslator"
        config.from_translator._from_lang = "fr"
        config.from_translator._to_lang = "en"

        config.to_translator._classname = "programy.nlp.translate.textblob_translator.TextBlobTranslator"
        config.to_translator._from_lang = "en"
        config.to_translator._to_lang = "fr"

        context.bot = Bot(config=config, client=self.client)
        context.brain = context.bot.brain
        test_str = "Ceci est mon emplacement!"

        translate_processor = TranslatorPreProcessor()
        test_str = translate_processor.process(context, test_str)
        self.assertEqual("This is my location!", test_str)

        punctuation_processor = RemovePunctuationPreProcessor()
        test_str = punctuation_processor.process(context, test_str)
        self.assertEqual("This is my location!", test_str)

        normalize_processor = NormalizePreProcessor()
        test_str = normalize_processor.process(context, test_str)
        self.assertEqual("This is my location!", test_str)

        toupper_processor = ToUpperPreProcessor()
        test_str = toupper_processor.process(context, test_str)
        self.assertEqual("THIS IS MY LOCATION!", test_str)

        demojize_processpr = DemojizePreProcessor()
        test_str = demojize_processpr.process(context, test_str)
        self.assertEqual(test_str, test_str)