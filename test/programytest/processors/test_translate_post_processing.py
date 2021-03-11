import re
import unittest

import programytest.externals as Externals
from programy.bot import Bot
from programy.config.bot.bot import BotConfiguration
from programy.context import ClientContext
from programy.processors.post.denormalize import DenormalizePostProcessor
from programy.processors.post.emojize import EmojizePostProcessor
from programy.processors.post.formatnumbers import FormatNumbersPostProcessor
from programy.processors.post.formatpunctuation import FormatPunctuationProcessor
from programy.processors.post.multispaces import RemoveMultiSpacePostProcessor
from programy.processors.post.translate import TranslatorPostProcessor
from programytest.client import TestClient


class PostProcessingTests(unittest.TestCase):

    def post_process(self, output_str):
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
        context.bot.brain.denormals.add_to_lookup(" DOT COM ", [re.compile('(^DOT COM | DOT COM | DOT COM$)', re.IGNORECASE), '.COM '])
        context.bot.brain.denormals.add_to_lookup(" ATSIGN ",[re.compile('(^ATSIGN | ATSIGN | ATSIGN$)', re.IGNORECASE), '@'])

        denormalize = DenormalizePostProcessor()
        punctuation = FormatPunctuationProcessor()
        numbers = FormatNumbersPostProcessor()
        multispaces = RemoveMultiSpacePostProcessor()
        emojize = EmojizePostProcessor()
        translate = TranslatorPostProcessor()

        output_str = denormalize.process(context, output_str)
        output_str = punctuation.process(context, output_str)
        output_str = numbers.process(context, output_str)
        output_str = multispaces.process(context, output_str)
        output_str = emojize.process(context, output_str)
        output_str = translate.process(context, output_str)

        return output_str

    @unittest.skipIf(Externals.google_translate is False or Externals.all_externals is False, Externals.google_translate_disabled)
    def test_post_cleanup(self):
        result = self.post_process("Hello World")
        self.assertIsNotNone(result)
        self.assertEqual("Bonjour le monde", result)

    @unittest.skipIf(Externals.google_translate is False or Externals.all_externals is False,
                     Externals.google_translate_disabled)
    def test_post_cleanup_punctuation(self):
        result = self.post_process("Hello World . This is It! ")
        self.assertIsNotNone(result)
        self.assertEqual("Bonjour le monde. Ça y est!", result)

    @unittest.skipIf(Externals.google_translate is False or Externals.all_externals is False,
                     Externals.google_translate_disabled)
    def test_post_cleanup_denorm(self):
        result = self.post_process("My email address is ybot atsign programy dot com")
        self.assertIsNotNone(result)
        self.assertEqual("Mon adresse e-mail est ybot@programy.com", result)

    @unittest.skipIf(Externals.google_translate is False or Externals.all_externals is False,
                     Externals.google_translate_disabled)
    def test_post_cleanup_hello_world(self):
        result = self.post_process("He said hello world")
        self.assertIsNotNone(result)
        self.assertEqual('Il a dit bonjour le monde', result)

    @unittest.skipIf(Externals.google_translate is False or Externals.all_externals is False,
                     Externals.google_translate_disabled)
    def test_post_cleanup_hello_world_quotes(self):
        result = self.post_process("He said ' hello world '")
        self.assertIsNotNone(result)
        self.assertEqual("Il a dit 'bonjour le monde'", result)

