import unittest
from programy.processors.post.emojize import EmojizePostProcessor
from programy.bot import Bot
from programy.config.bot.bot import BotConfiguration
from programy.context import ClientContext

from programytest.client import TestClient


class EmojizePreProcessorTests(unittest.TestCase):

    def setUp(self):
        self.client = TestClient()
        self.bot = Bot(config=BotConfiguration(), client=self.client)

    def test_demojize(self):
        processor = EmojizePostProcessor()
        
        context = ClientContext(self.client, "TestUser")
        
        self.assertEqual("Python is 👍", processor.process(context, 'Python is :thumbs_up:'))
        self.assertEqual("Python is 👍", processor.process(context, 'Python is :thumbsup:'))
