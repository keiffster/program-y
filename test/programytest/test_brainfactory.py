import unittest

from programy.config.bot.bot import BotConfiguration
from programy.bot import Bot
from programy.brainfactory import BrainFactory

from programytest.client import TestClient


class BrainFactoryTests(unittest.TestCase):

    def test_init(self):

        client = TestClient()

        bot = Bot(BotConfiguration(), client)

        self.assertIsNotNone(bot.brain_factory)
        self.assertIsInstance(bot.brain_factory, BrainFactory)

        brain = bot.brain_factory.brain("brain")

        self.assertIsNotNone(brain)
