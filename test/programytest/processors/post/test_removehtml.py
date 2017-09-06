import unittest
import os

from programy.processors.post.removehtml import RemoveHTMLPostProcessor
from programy.bot import Bot
from programy.brain import Brain
from programy.config.sections.brain.brain import BrainConfiguration
from programy.config.sections.bot.bot import BotConfiguration

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
        if os.name == 'posix':
            self.assertEqual("Hello\nWorld", result)
        elif os.name == 'nt':
            self.assertEqual("Hello\r\nWorld", result)
        else:
            raise Exception("Unknown os [%s]"%os.name)

        result = processor.process(self.bot, "testid", "Hello <br /> World")
        self.assertIsNotNone(result)
        if os.name == 'posix':
            self.assertEqual("Hello\nWorld", result)
        elif os.name == 'nt':
            self.assertEqual("Hello\r\nWorld", result)
        else:
            raise Exception("Unknown os [%s]"%os.name)
