import unittest
from programy.processors.post.emojize import EmojizePreProcessor
from programy.bot import Bot
from programy.config.bot.bot import BotConfiguration
from programy.context import ClientContext

from programytest.aiml_tests.client import TestClient


class EmojizeTests(unittest.TestCase):

    def setUp(self):
        self.bot = Bot(config=BotConfiguration())

    def test_demojize(self):
        processor = EmojizePreProcessor()
        
        context = ClientContext(TestClient(), "TestUser")
        
        self.assertEqual("Python is 👍", processor.process(context, 'Python is :thumbs_up:'))
        self.assertEqual("Python is 👍", processor.process(context, 'Python is :thumbsup:'))
