import unittest
from programy.processors.pre.removepunctuation import RemovePunctuationPreProcessor
from programy.processors.pre.toupper import ToUpperPreProcessor
from programy.processors.pre.normalize import NormalizePreProcessor
from programy.bot import Bot
from programy.brain import Brain
from programy.config.sections.brain.brain import BrainConfiguration
from programy.config.sections.bot.bot import BotConfiguration


class PreProcessingTests(unittest.TestCase):

    def setUp(self):
        self.bot = Bot(Brain(BrainConfiguration()), config=BotConfiguration())

    def test_pre_cleanup(self):

        test_str = "This is my Location!"

        punctuation_processor = RemovePunctuationPreProcessor()
        test_str = punctuation_processor.process(self.bot, "testid", test_str)
        self.assertEqual("This is my Location", test_str)

        normalize_processor = NormalizePreProcessor()
        test_str = normalize_processor.process(self.bot, "testid", test_str)
        self.assertEqual("This is my Location", test_str)

        toupper_processor = ToUpperPreProcessor()
        test_str = toupper_processor.process(self.bot, "testid", test_str)
        self.assertEqual("THIS IS MY LOCATION", test_str)
