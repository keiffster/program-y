import unittest
from programy.processors.post.removehtml import RemoveHTMLPostProcessor
from programy.bot import Bot
from programy.brain import Brain
from programy.config.brain import BrainConfiguration
from programy.config.bot import BotConfiguration

class RemoveHTMLTests(unittest.TestCase):

    def setUp(self):
        self.bot = Bot(Brain(BrainConfiguration()), config=BotConfiguration())

    def test_remove_html(self):
        processor = RemoveHTMLPostProcessor()

        result = processor.process(self.bot, "testid", "Hello World")
        self.assertIsNotNone(result)
        self.assertEqual("Hello World", result)

        result = processor.process(self.bot, "testid", "Hello <br/> World")
        self.assertIsNotNone(result)
        self.assertEqual("Hello \nWorld", result)

        result = processor.process(self.bot, "testid", "Hello <br /> World")
        self.assertIsNotNone(result)
        self.assertEqual("Hello \nWorld", result)
