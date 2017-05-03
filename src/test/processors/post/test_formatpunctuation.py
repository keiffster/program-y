import unittest
from programy.processors.post.formatpunctuation import FormatPunctuationProcessor
from programy.bot import Bot
from programy.brain import Brain
from programy.config.brain import BrainConfiguration
from programy.config.bot import BotConfiguration

class FormatNmbersTests(unittest.TestCase):

    def setUp(self):
        self.bot = Bot(Brain(BrainConfiguration()), config=BotConfiguration())

    def test_format_punctuation(self):
        processor = FormatPunctuationProcessor()

        result = processor.process(self.bot, "testid", 'Hello " World "')
        self.assertIsNotNone(result)
        self.assertEqual('Hello "World"', result)

        result = processor.process(self.bot, "testid", '"Hello World"')
        self.assertIsNotNone(result)
        self.assertEqual('"Hello World"', result)

        result = processor.process(self.bot, "testid", "' Hello World '")
        self.assertIsNotNone(result)
        self.assertEqual("'Hello World'", result)

        result = processor.process(self.bot, "testid", '" Hello World "')
        self.assertIsNotNone(result)
        self.assertEqual('"Hello World"', result)

        result = processor.process(self.bot, "testid", '"This" and "That"')
        self.assertIsNotNone(result)
        self.assertEqual('"This" and "That"', result)

        result = processor.process(self.bot, "testid", "Hello World .")
        self.assertIsNotNone(result)
        self.assertEqual("Hello World.", result)

        result = processor.process(self.bot, "testid", "Hello World ,")
        self.assertIsNotNone(result)
        self.assertEqual("Hello World,", result)

        result = processor.process(self.bot, "testid", "Hello World :")
        self.assertIsNotNone(result)
        self.assertEqual("Hello World:", result)

        result = processor.process(self.bot, "testid", "Hello World ;")
        self.assertIsNotNone(result)
        self.assertEqual("Hello World;", result)

        result = processor.process(self.bot, "testid", "Hello World ?")
        self.assertIsNotNone(result)
        self.assertEqual("Hello World?", result)

        result = processor.process(self.bot, "testid", "Hello World !")
        self.assertIsNotNone(result)
        self.assertEqual("Hello World!", result)

        result = processor.process(self.bot, "testid", "Hello World . This is it.")
        self.assertIsNotNone(result)
        self.assertEqual("Hello World. This is it.", result)

        result = processor.process(self.bot, "testid", "Hello World . 23.45.")
        self.assertIsNotNone(result)
        self.assertEqual("Hello World. 23.45.", result)
