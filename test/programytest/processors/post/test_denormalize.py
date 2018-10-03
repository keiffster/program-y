import unittest
import re

from programy.processors.post.denormalize import DenormalizePostProcessor
from programy.bot import Bot
from programy.config.bot.bot import BotConfiguration
from programy.context import ClientContext

from programytest.client import TestClient


class DenormalizeTests(unittest.TestCase):

    def setUp(self):
        self.client = TestClient()
        self.bot = Bot(config=BotConfiguration(), client=self.client)
        self.bot.brain.denormals.add_to_lookup(" DOT COM ", [re.compile('(^DOT COM | DOT COM | DOT COM$)', re.IGNORECASE), '.COM '])

    def test_denormalize(self):
        processor = DenormalizePostProcessor ()

        context = ClientContext(self.client, "testid")
        context.bot = self.bot
        context.brain = self.bot.brain
        result = processor.process(context, "Hello")
        self.assertIsNotNone(result)
        self.assertEqual("Hello", result)

        result = processor.process(context, "hello dot com")
        self.assertIsNotNone(result)
        self.assertEqual("hello.com", result)
