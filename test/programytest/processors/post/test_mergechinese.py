import unittest
from programy.processors.post.mergechinese import MergeChinesePostProcessor
from programy.bot import Bot
from programy.brain import Brain
from programy.config.sections.brain.brain import BrainConfiguration
from programy.config.sections.bot.bot import BotConfiguration


class MergeChineseTests(unittest.TestCase):

    def setUp(self):
        self.bot = Bot(Brain(BrainConfiguration()), config=BotConfiguration())

    def test_merge_chinese(self):
        processor = MergeChinesePostProcessor()

        result = processor.process(self.bot, "testid", "Hello")
        self.assertIsNotNone(result)
        self.assertEqual("Hello", result)

        result = processor.process(self.bot, "testid", "Hello World")
        self.assertIsNotNone(result)
        self.assertEqual("Hello World", result)

        result = processor.process(self.bot, "testid", "你 好")
        self.assertIsNotNone(result)
        self.assertEqual("你好", result)

        result = processor.process(self.bot, "testid", "问 你 好")
        self.assertIsNotNone(result)
        self.assertEqual("问你好", result)

        result = processor.process(self.bot, "testid", "XX 你 好")
        self.assertIsNotNone(result)
        self.assertEqual("XX 你好", result)

        result = processor.process(self.bot, "testid", "XX 你 好 YY")
        self.assertIsNotNone(result)
        self.assertEqual("XX 你好 YY", result)

