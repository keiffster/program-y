import unittest
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

        test_str = "Hello World"

        normalize_processor = NormalizePreProcessor()
        pass1_str = normalize_processor.process(self.bot, "testid", test_str)
        self.assertEqual("Hello World", pass1_str)

        toupper_processor = ToUpperPreProcessor()
        pass2_str = toupper_processor.process(self.bot, "testid", pass1_str)
        self.assertEqual("HELLO WORLD", pass2_str)
