import unittest

from programy.dialog.splitter.splitter import SentenceSplitter
from programy.config.bot.splitter import BotSentenceSplitterConfiguration

class SentenceSplitterTests(unittest.TestCase):

    def test_initiate_spellchecker(self):

        config = BotSentenceSplitterConfiguration()
        self.assertIsNotNone(config)

        splitter = SentenceSplitter.initiate_sentence_splitter(config)
        self.assertIsNotNone(splitter)
        self.assertIsInstance(splitter, SentenceSplitter)

    def test_remove_punctuation(self):

        config = BotSentenceSplitterConfiguration()
        self.assertIsNotNone(config)

        splitter = SentenceSplitter.initiate_sentence_splitter(config)
        self.assertIsNotNone(splitter)

        self.assertEquals("", splitter.remove_punctuation(""))
        self.assertEquals("", splitter.remove_punctuation("()"))
        self.assertEquals("Hello world", splitter.remove_punctuation("(Hello, world)"))