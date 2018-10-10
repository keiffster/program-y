import unittest
from programy.processors.pre.removepunctuation import RemovePunctuationPreProcessor
from programy.processors.pre.toupper import ToUpperPreProcessor
from programy.processors.pre.normalize import NormalizePreProcessor
from programy.processors.pre.demojize import DemojizePreProcessor
from programy.bot import Bot
from programy.config.bot.bot import BotConfiguration
from programy.context import ClientContext

from programytest.client import TestClient


class PreProcessingTests(unittest.TestCase):

    def test_pre_cleanup(self):
        self.client = TestClient()

        context = ClientContext(self.client, "testid")
        context.bot = Bot(config=BotConfiguration(), client=self.client)
        context.brain = context.bot.brain
        test_str = "This is my Location!"

        punctuation_processor = RemovePunctuationPreProcessor()
        test_str = punctuation_processor.process(context, test_str)
        self.assertEqual("This is my Location!", test_str)

        normalize_processor = NormalizePreProcessor()
        test_str = normalize_processor.process(context, test_str)
        self.assertEqual("This is my Location!", test_str)

        toupper_processor = ToUpperPreProcessor()
        test_str = toupper_processor.process(context, test_str)
        self.assertEqual("THIS IS MY LOCATION!", test_str)

        demojize_processpr = DemojizePreProcessor()
        test_str = demojize_processpr.process(context, test_str)
        self.assertEqual(test_str, test_str)