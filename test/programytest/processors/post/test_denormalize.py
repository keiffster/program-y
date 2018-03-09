import unittest
from programy.processors.post.denormalize import DenormalizePostProcessor
from programy.bot import Bot
from programy.brain import Brain
from programy.config.brain.brain import BrainConfiguration
from programy.config.bot.bot import BotConfiguration
from programy.context import ClientContext

from programytest.aiml_tests.client import TestClient


class DenormalizeTests(unittest.TestCase):

    def setUp(self):
        self.bot = Bot(config=BotConfiguration())
        self.bot.brain.denormals.process_splits([" dot com ",".com"])

    def test_denormalize(self):
        processor = DenormalizePostProcessor ()

        context = ClientContext(TestClient(), "testid")
        context.bot = self.bot
        context.brain = self.bot.brain
        result = processor.process(context, "Hello")
        self.assertIsNotNone(result)
        self.assertEqual("Hello", result)

        result = processor.process(context, "hello dot com")
        self.assertIsNotNone(result)
        self.assertEqual("hello.com", result)
