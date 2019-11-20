import unittest
from programy.nlp.stopwords import StopWords


class StopWordsTests(unittest.TestCase):

    def test_remove(self):
        stopwords = StopWords(language="english")
        self.assertIsNotNone(stopwords)
        self.assertIsNotNone(stopwords._words)

        self.assertEqual([""], stopwords.remove([""]))
        self.assertEqual([], stopwords.remove([]))
        self.assertEqual(['This', 'sentence'], stopwords.remove(["This", "is", "a", "sentence"]))

    def test_is_stopword(self):
        stopwords = StopWords(language="english")
        self.assertIsNotNone(stopwords)
        self.assertIsNotNone(stopwords._words)

        self.assertTrue(stopwords.is_stopword("is"))
        self.assertFalse(stopwords.is_stopword("python"))
        self.assertFalse(stopwords.is_stopword(""))
