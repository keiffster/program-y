import unittest
from programy.processors.pre.splitchinese import SplitChinesePreProcessor
from programy.bot import Bot
from programy.brain import Brain
from programy.config.sections.brain.brain import BrainConfiguration
from programy.config.sections.bot.bot import BotConfiguration


class SplitChineseTests(unittest.TestCase):

    def setUp(self):
        self.bot = Bot(Brain(BrainConfiguration()), config=BotConfiguration())

    def test_split_chinese(self):
        processor = SplitChinesePreProcessor()

        result = processor.process(self.bot, "testid", "Hello")
        self.assertIsNotNone(result)
        self.assertEqual("Hello", result)

        result = processor.process(self.bot, "testid", "Hello World")
        self.assertIsNotNone(result)
        self.assertEqual("Hello World", result)

        result = processor.process(self.bot, "testid", "你好")
        self.assertIsNotNone(result)
        self.assertEqual("你 好", result)

        result = processor.process(self.bot, "testid", "问你好")
        self.assertIsNotNone(result)
        self.assertEqual("问 你 好", result)

        result = processor.process(self.bot, "testid", "XX你好")
        self.assertIsNotNone(result)
        self.assertEqual("XX 你 好", result)

        result = processor.process(self.bot, "testid", "XX你好 YY")
        self.assertIsNotNone(result)
        self.assertEqual("XX 你 好 YY", result)

        result = processor.process(self.bot, "testid", "XX你好YY")
        self.assertIsNotNone(result)
        self.assertEqual("XX 你 好 YY", result)
