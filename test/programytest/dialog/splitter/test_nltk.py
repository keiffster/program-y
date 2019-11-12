import unittest

from programy.config.bot.splitter import BotSentenceSplitterConfiguration
from programy.dialog.splitter.nltk import NLTKSentenceSplitter


class NLTKSentenceSplitterTests(unittest.TestCase):

    def test_not_implemented(self):

        splitter = NLTKSentenceSplitter(BotSentenceSplitterConfiguration())

        with self.assertRaises(NotImplementedError):
            splitter.split("Split this")