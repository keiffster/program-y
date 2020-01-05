import unittest

from programy.config.bot.splitter import BotSentenceSplitterConfiguration
from programy.dialog.splitter.splitter import SentenceSplitter


class SentenceSplitterTests(unittest.TestCase):

    def test_initiate_spellchecker(self):

        config = BotSentenceSplitterConfiguration()
        self.assertIsNotNone(config)

        splitter = SentenceSplitter(config)
        self.assertIsNotNone(splitter)
        self.assertIsInstance(splitter, SentenceSplitter)

        with self.assertRaises(NotImplementedError):
            splitter.split("This sentence")

    def test_remove_punctuation(self):

        config = BotSentenceSplitterConfiguration()
        self.assertIsNotNone(config)

        splitter = SentenceSplitter.initiate_sentence_splitter(config)
        self.assertIsNotNone(splitter)

        self.assertEqual("", splitter.remove_punctuation(""))
        self.assertEqual("", splitter.remove_punctuation("()"))
        self.assertEqual("Hello world", splitter.remove_punctuation("(Hello, world)"))