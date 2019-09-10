import unittest

from programy.nlp.ngrams import NGramsCreator


class NGramsCreatorTests(unittest.TestCase):

    def test_get_ngrams_3(self):
        ngrams = NGramsCreator.get_ngrams("Now is better than never.")
        self.assertIsNotNone(ngrams)
        self.assertEquals([['Now', 'is', 'better'], ['is', 'better', 'than'], ['better', 'than', 'never']], ngrams)
