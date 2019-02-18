import unittest
from programy.processors.post.translate import TranslatorPostProcessor
from programy.bot import Bot
from programy.config.bot.bot import BotConfiguration

from programytest.client import TestClient


class MockClientContext(object):

    def __init__(self, bot):
        self.bot = bot


class TranslatorPostProcessorTest(unittest.TestCase):

    def setUp(self):
        self.client = TestClient()
        config = BotConfiguration()

        config.from_translator._classname = "programy.translate.textblob_translator.TextBlobTranslator"
        config.from_translator._from_lang = "fr"
        config.from_translator._to_lang = "en"

        config.to_translator._classname = "programy.translate.textblob_translator.TextBlobTranslator"
        config.to_translator._from_lang = "en"
        config.to_translator._to_lang = "fr"

        self.bot = Bot(config=config, client=self.client)
        self.bot.initiate_translator()

    def test_post_process_translate(self):
        processor = TranslatorPostProcessor()

        context = MockClientContext(self.bot)

        self.assertEqual("Bonjour", processor.process(context, "Hello"))