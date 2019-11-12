import unittest

from programy.config.bot.splitter import BotSentenceSplitterConfiguration
from programy.dialog.splitter.regex import RegexSentenceSplitter


class RegexSentenceSplitterTests(unittest.TestCase):

    def test_basic_sentence(self):
        splitter = RegexSentenceSplitter(BotSentenceSplitterConfiguration())
        self.assertIsNotNone(splitter)

        self.assertEqual(["This is a basic sentence"], splitter.split("This is a basic sentence"))

    def test_punctuation_at_end(self):
        splitter = RegexSentenceSplitter(BotSentenceSplitterConfiguration())
        self.assertIsNotNone(splitter)

        self.assertEqual(["Is this the first sentence"], splitter.split("Is this the first sentence?"))

    def test_fullstop(self):
        splitter = RegexSentenceSplitter(BotSentenceSplitterConfiguration())
        self.assertIsNotNone(splitter)

        self.assertEqual(["This is the first sentence",  "This is the second"], splitter.split("This is the first sentence. This is the second"))

    def test_comma(self):
        splitter = RegexSentenceSplitter(BotSentenceSplitterConfiguration())
        self.assertIsNotNone(splitter)

        self.assertEqual(["This is the first sentence",  "this is the second"], splitter.split("This is the first sentence, this is the second"))

    def test_exclamation_mark(self):
        splitter = RegexSentenceSplitter(BotSentenceSplitterConfiguration())
        self.assertIsNotNone(splitter)

        self.assertEqual(["This is the first sentence",  "This is the second"], splitter.split("This is the first sentence! This is the second"))

    def test_question_mark(self):
        splitter = RegexSentenceSplitter(BotSentenceSplitterConfiguration())
        self.assertIsNotNone(splitter)

        self.assertEqual(["Is this the first sentence",  "This is the second"], splitter.split("Is this the first sentence? This is the second"))

    def test_not_active(self):
        splitter = RegexSentenceSplitter(BotSentenceSplitterConfiguration())
        self.assertIsNotNone(splitter)
        splitter.active = RegexSentenceSplitter.OFF

        self.assertEqual(["This is a basic sentence"], splitter.split("This is a basic sentence"))
