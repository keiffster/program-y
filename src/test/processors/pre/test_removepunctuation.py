import unittest
from programy.processors.pre.removepunctuation import RemovePunctuationPreProcessor
from programy.bot import Bot
from programy.brain import Brain
from programy.config.brain import BrainConfiguration
from programy.config.bot import BotConfiguration


class RemovePunctuationTests(unittest.TestCase):

    def setUp(self):
        self.bot = Bot(Brain(BrainConfiguration()), config=BotConfiguration())

    def test_remove_punctuation(self):
        processor = RemovePunctuationPreProcessor()

        result = processor.process(self.bot, "testid", "Hello!")
        self.assertIsNotNone(result)
        self.assertEqual("Hello", result)

        result = processor.process(self.bot, "testid", "$100")
        self.assertIsNotNone(result)
        self.assertEqual("$100", result)
