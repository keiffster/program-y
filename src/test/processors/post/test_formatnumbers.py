import unittest
from programy.processors.post.formatnumbers import FormatNumbersPostProcessor
from programy.bot import Bot
from programy.brain import Brain
from programy.config.brain import BrainConfiguration
from programy.config.bot import BotConfiguration

class FormatNmbersTests(unittest.TestCase):

    def setUp(self):
        self.bot = Bot(Brain(BrainConfiguration()), config=BotConfiguration())

    def test_format_numbers(self):
        processor = FormatNumbersPostProcessor()

        result = processor.process(self.bot, "testid", "23")
        self.assertIsNotNone(result)
        self.assertEqual("23", result)

        result = processor.process(self.bot, "testid", "23.45")
        self.assertIsNotNone(result)
        self.assertEqual("23.45", result)

        result = processor.process(self.bot, "testid", "23. 45")
        self.assertIsNotNone(result)
        self.assertEqual("23.45", result)

        result = processor.process(self.bot, "testid", "23 . 45")
        self.assertIsNotNone(result)
        self.assertEqual("23.45", result)

        result = processor.process(self.bot, "testid", "23,450")
        self.assertIsNotNone(result)
        self.assertEqual("23,450", result)

        result = processor.process(self.bot, "testid", "23, 450")
        self.assertIsNotNone(result)
        self.assertEqual("23,450", result)

        result = processor.process(self.bot, "testid", "23, 450, 000")
        self.assertIsNotNone(result)
        self.assertEqual("23,450,000", result)
