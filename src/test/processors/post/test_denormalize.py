import unittest
from programy.processors.post.denormalize import DenormalizePostProcessor
from programy.bot import Bot
from programy.brain import Brain
from programy.config.brain import BrainConfiguration
from programy.config.bot import BotConfiguration


class DenormalizeTests(unittest.TestCase):

    def setUp(self):
        self.bot = Bot(Brain(BrainConfiguration()), config=BotConfiguration())
        self.bot.brain.denormals.process_splits([" dot com ",".com"])

    def test_denormalize(self):
        processor = DenormalizePostProcessor ()

        result = processor.process(self.bot, "testid", "Hello")
        self.assertIsNotNone(result)
        self.assertEqual("Hello", result)

        result = processor.process(self.bot, "testid", "hello dot com")
        self.assertIsNotNone(result)
        self.assertEqual("hello.com", result)
