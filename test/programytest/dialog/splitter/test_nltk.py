import unittest

from programy.dialog.splitter.nltk import NLTKSentenceSplitter
from programy.config.bot.splitter import BotSentenceSplitterConfiguration


class NLTKSentenceSplitterTests(unittest.TestCase):

    def test_not_implemented(self):

        splitter = NLTKSentenceSplitter(BotSentenceSplitterConfiguration())

        with self.assertRaises(NotImplementedError):
            splitter.split("Split this")