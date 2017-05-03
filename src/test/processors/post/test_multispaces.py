import unittest
from programy.processors.post.multispaces import RemoveMultiSpacePostProcessor
from programy.bot import Bot
from programy.brain import Brain
from programy.config.brain import BrainConfiguration
from programy.config.bot import BotConfiguration

class RemoveMultiSpaceTests(unittest.TestCase):

    def setUp(self):
        self.bot = Bot(Brain(BrainConfiguration()), config=BotConfiguration())

    def test_remove_multi_spaces(self):
        processor = RemoveMultiSpacePostProcessor()

        result = processor.process(self.bot, "testid", "Hello World")
        self.assertIsNotNone(result)
        self.assertEqual("Hello World", result)

        result = processor.process(self.bot, "testid", "Hello World ")
        self.assertIsNotNone(result)
        self.assertEqual("Hello World", result)

        result = processor.process(self.bot, "testid", " Hello World")
        self.assertIsNotNone(result)
        self.assertEqual("Hello World", result)

        result = processor.process(self.bot, "testid", " Hello  World ")
        self.assertIsNotNone(result)
        self.assertEqual("Hello World", result)
