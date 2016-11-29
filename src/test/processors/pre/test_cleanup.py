import unittest
from programy.processors.pre.cleanup import CleanUpPreProcessor
from programy.bot import Bot
from programy.brain import Brain
from programy.config import BrainConfiguration, BotConfiguration


class PreCleanUpTests(unittest.TestCase):

    def setUp(self):
        self.bot = Bot(Brain(BrainConfiguration()), config=BotConfiguration())

    def test_pre_cleanup(self):
        processor = CleanUpPreProcessor()

        result = processor.process(self.bot, "testid", "Hello")
        self.assertIsNotNone(result)
        self.assertEqual("HELLO", result)
