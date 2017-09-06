import unittest
from programy.processors.pre.toupper import ToUpperPreProcessor
from programy.bot import Bot
from programy.brain import Brain
from programy.config.sections.brain.brain import BrainConfiguration
from programy.config.sections.bot.bot import BotConfiguration


class ToUpperTests(unittest.TestCase):

    def setUp(self):
        self.bot = Bot(Brain(BrainConfiguration()), config=BotConfiguration())

    def test_to_upper(self):
        processor = ToUpperPreProcessor()

        result = processor.process(self.bot, "testid", "Hello")
        self.assertIsNotNone(result)
        self.assertEqual("HELLO", result)
