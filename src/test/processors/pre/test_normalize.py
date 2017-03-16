import unittest
from programy.processors.pre.normalize import NormalizePreProcessor
from programy.bot import Bot
from programy.brain import Brain
from programy.config.brain import BrainConfiguration
from programy.config.bot import BotConfiguration


class NormalizeTests(unittest.TestCase):

    def setUp(self):
        self.bot = Bot(Brain(BrainConfiguration()), config=BotConfiguration())

    def test_normalize(self):
        processor = NormalizePreProcessor()

        result = processor.process(self.bot, "testid", "Hello")
        self.assertIsNotNone(result)
        self.assertEqual("Hello", result)
