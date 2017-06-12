import unittest
from programy.processors.pre.removepunctuation import RemovePunctuationPreProcessor
from programy.bot import Bot
from programy.brain import Brain
from programy.config.brain import BrainConfiguration
from programy.config.bot import BotConfiguration


class ToUpperTests(unittest.TestCase):

    def setUp(self):
        self.bot = Bot(Brain(BrainConfiguration()), config=BotConfiguration())

    def test_to_upper(self):
        processor = RemovePunctuationPreProcessor()

        result = processor.process(self.bot, "testid", "Hello!")
        self.assertIsNotNone(result)
        self.assertEqual("Hello", result)
