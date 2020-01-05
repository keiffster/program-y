import unittest

from programy.config.bot.splitter import BotSentenceSplitterConfiguration
from programy.dialog.splitter.spacy import SpacySentenceSplitter


class SpacySentenceSplitterTests(unittest.TestCase):

    def test_not_implemented(self):

        splitter = SpacySentenceSplitter(BotSentenceSplitterConfiguration())

        with self.assertRaises(NotImplementedError):
            splitter.split("Split this")