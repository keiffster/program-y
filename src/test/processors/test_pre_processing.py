import unittest
from programy.processors.pre.removepunctuation import RemovePunctuationPreProcessor
from programy.processors.pre.toupper import ToUpperPreProcessor
from programy.processors.pre.normalize import NormalizePreProcessor
from programy.bot import Bot
from programy.brain import Brain
from programy.config.brain import BrainConfiguration
from programy.config.bot import BotConfiguration


class PreProcessingTests(unittest.TestCase):

    def setUp(self):
        self.bot = Bot(Brain(BrainConfiguration()), config=BotConfiguration())

    def test_pre_cleanup(self):

        test_str = "Hello World!"

        punctuation_processor = RemovePunctuationPreProcessor()
        pass1_str = punctuation_processor.process(self.bot, "testid", test_str)
        self.assertEqual("Hello World", pass1_str)

        normalize_processor = NormalizePreProcessor()
        pass2_str = normalize_processor.process(self.bot, "testid", pass1_str)
        self.assertEqual("Hello World", pass2_str)

        toupper_processor = ToUpperPreProcessor()
        pass3_str = toupper_processor.process(self.bot, "testid", pass2_str)
        self.assertEqual("HELLO WORLD", pass3_str)
