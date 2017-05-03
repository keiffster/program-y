import unittest
from programy.processors.post.denormalize import DenormalizePostProcessor
from programy.processors.post.formatpunctuation import FormatPunctuationProcessor
from programy.processors.post.formatnumbers import FormatNumbersPostProcessor
from programy.processors.post.multispaces import RemoveMultiSpacePostProcessor
from programy.bot import Bot
from programy.brain import Brain
from programy.config.brain import BrainConfiguration
from programy.config.bot import BotConfiguration


class PostProcessingTests(unittest.TestCase):

    def setUp(self):
        self.bot = Bot(Brain(BrainConfiguration()), config=BotConfiguration())
        self.bot.brain.denormals.process_splits([" dot com ",".com"])
        self.bot.brain.denormals.process_splits([" atsign ","@"])
        self.denormalize = DenormalizePostProcessor()
        self.punctuation = FormatPunctuationProcessor()
        self.numbers = FormatNumbersPostProcessor()
        self.multispaces = RemoveMultiSpacePostProcessor()

    def process_test_string(self, string):
        string = self.denormalize.process(self.bot, "testid", string)
        string = self.punctuation.process(self.bot, "testid", string)
        string = self.numbers.process(self.bot, "testid", string)
        string = self.multispaces.process(self.bot, "testid", string)
        return string

    def test_post_cleanup(self):

        result = self.process_test_string("Hello World")
        self.assertIsNotNone(result)
        self.assertEqual("Hello World", result)

        result = self.process_test_string("Hello World . This is It! ")
        self.assertIsNotNone(result)
        self.assertEqual("Hello World. This is It!", result)

        result = self.process_test_string("Is the result 23 . 45 ?")
        self.assertIsNotNone(result)
        self.assertEqual("Is the result 23.45?", result)

        result = self.process_test_string("My email address is ybot atsign programy dot com")
        self.assertIsNotNone(result)
        self.assertEqual("My email address is ybot@programy.com", result)

        result = self.process_test_string("He said ' Hello World '.")
        self.assertIsNotNone(result)
        self.assertEqual("He said 'Hello World'.", result)



