import unittest

from programy.nlp.stopwords import StopWords


class StopWordsTests(unittest.TestCase):

    def test_remove(self):
        self.assertEquals([""], StopWords.remove([""]))
        self.assertEquals([], StopWords.remove([]))
        self.assertEquals(['This', 'sentence'], StopWords.remove(["This", "is", "a", "sentence"]))

    def test_is_stopword(self):
        self.assertTrue(StopWords.is_stopword("is"))
        self.assertFalse(StopWords.is_stopword("python"))
        self.assertFalse(StopWords.is_stopword(""))
