import unittest

from programy.dialog.splitter.regex import RegexSentenceSplitter
from programy.config.bot.splitter import BotSentenceSplitterConfiguration


class RegexSentenceSplitterTests(unittest.TestCase):

    def test_basic_sentence(self):
        splitter = RegexSentenceSplitter(BotSentenceSplitterConfiguration())
        self.assertIsNotNone(splitter)

        self.assertEquals(["This is a basic sentence"], splitter.split("This is a basic sentence"))

    def test_punctuation_at_end(self):
        splitter = RegexSentenceSplitter(BotSentenceSplitterConfiguration())
        self.assertIsNotNone(splitter)

        self.assertEquals(["Is this the first sentence"], splitter.split("Is this the first sentence?"))

    def test_fullstop(self):
        splitter = RegexSentenceSplitter(BotSentenceSplitterConfiguration())
        self.assertIsNotNone(splitter)

        self.assertEquals(["This is the first sentence",  "This is the second"], splitter.split("This is the first sentence. This is the second"))

    def test_comma(self):
        splitter = RegexSentenceSplitter(BotSentenceSplitterConfiguration())
        self.assertIsNotNone(splitter)

        self.assertEquals(["This is the first sentence",  "this is the second"], splitter.split("This is the first sentence, this is the second"))

    def test_exclamation_mark(self):
        splitter = RegexSentenceSplitter(BotSentenceSplitterConfiguration())
        self.assertIsNotNone(splitter)

        self.assertEquals(["This is the first sentence",  "This is the second"], splitter.split("This is the first sentence! This is the second"))

    def test_question_mark(self):
        splitter = RegexSentenceSplitter(BotSentenceSplitterConfiguration())
        self.assertIsNotNone(splitter)

        self.assertEquals(["Is this the first sentence",  "This is the second"], splitter.split("Is this the first sentence? This is the second"))

    """
    def test_abbreviation(self):
        splitter = RegexSentenceSplitter(BotSentenceSplitterConfiguration())
        self.assertIsNotNone(splitter)

        self.assertEquals(["Dr Smith is busy",  "Mr Jones is not"], splitter.split("Dr. Smith is busy. Mr. Jones is not"))

    def test_conjunction_and(self):
        splitter = RegexSentenceSplitter(BotSentenceSplitterConfiguration())
        self.assertIsNotNone(splitter)

        self.assertEquals(["The cow is black", "the horse is brown"], splitter.split("The cow is black and the horse is brown"))

    def test_conjunction_or(self):
        splitter = RegexSentenceSplitter(BotSentenceSplitterConfiguration())
        self.assertIsNotNone(splitter)

        self.assertEquals(["Is it towards the left", "towards the right"], splitter.split("Is it towards the left or towards the right"))
    """