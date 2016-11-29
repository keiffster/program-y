import unittest
from programy.processors.post.denormalize import DenormalizePostProcessor
from programy.bot import Bot
from programy.brain import Brain
from programy.config import BrainConfiguration, BotConfiguration


class DenormalizeTests(unittest.TestCase):

    def setUp(self):
        self.bot = Bot(Brain(BrainConfiguration()), config=BotConfiguration())

    def test_denormalize(self):
        processor = DenormalizePostProcessor ()

        result = processor.process(self.bot, "testid", "Hello")
        self.assertIsNotNone(result)
        self.assertEqual("Hello", result)
