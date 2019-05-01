import unittest

from programy.config.brain.brain import BrainConfiguration
from programy.brain import Brain
from programy.config.bot.bot import BotConfiguration
from programy.bot import Bot
from programy.brainfactory import DefaultBrainSelector
from programy.clients.config import ClientConfigurationData

from programytest.client import TestClient


class DefaultBrainSelectorTests(unittest.TestCase):

    def test_selection_no_brain(self):

        config = ClientConfigurationData(name="test")
        selector = DefaultBrainSelector(config, {})

        selected = selector.select_brain()

        self.assertIsNone(selected)

    def test_selection_single_brain(self):

        client = TestClient()

        bot = Bot(BotConfiguration(), client)

        brain1 = Brain(bot, BrainConfiguration())
        brains = {"brain1": brain1}

        config = ClientConfigurationData(name="test")
        selector = DefaultBrainSelector(config, brains)

        selected = selector.select_brain()

        self.assertIsNotNone(selected)
        self.assertEquals(selected, brain1)

        selected = selector.select_brain()

        self.assertIsNotNone(selected)
        self.assertEquals(selected, brain1)

    def test_selection_multi_brain(self):

        client = TestClient()

        bot = Bot(BotConfiguration(), client)

        brain1 = Brain(bot, BrainConfiguration())
        brain2 = Brain(bot, BrainConfiguration())
        brain3 = Brain(bot, BrainConfiguration())
        brains = {"brain1": brain1, "brain2": brain2, "brain3": brain3}

        config = ClientConfigurationData(name="test")
        selector = DefaultBrainSelector(config, brains)

        selected = selector.select_brain()
        self.assertIsNotNone(selected)
        self.assertEquals(selected, brain1)

        selected = selector.select_brain()
        self.assertIsNotNone(selected)
        self.assertEquals(selected, brain2)

        selected = selector.select_brain()
        self.assertIsNotNone(selected)
        self.assertEquals(selected, brain3)

        selected = selector.select_brain()
        self.assertIsNotNone(selected)
        self.assertEquals(selected, brain1)
