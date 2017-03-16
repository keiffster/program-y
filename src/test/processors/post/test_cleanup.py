import unittest
from programy.processors.post.cleanup import CleanUpPostProcessor
from programy.bot import Bot
from programy.brain import Brain
from programy.config.brain import BrainConfiguration
from programy.config.bot import BotConfiguration

class PostCleanUpTests(unittest.TestCase):

    def setUp(self):
        self.bot = Bot(Brain(BrainConfiguration()), config=BotConfiguration())

    def test_post_cleanup(self):
        processor = CleanUpPostProcessor()

        result = processor.process(self.bot, "testid", "Hello")
        self.assertIsNotNone(result)
        self.assertEqual("Hello", result)
