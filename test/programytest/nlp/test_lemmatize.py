import unittest

from programy.nlp.lemmatize import Lemmatizer


class LemmatizerTests(unittest.TestCase):

    def test_lemmatize(self):
        self.assertEqual("octopus", Lemmatizer.lemmatize("octopi"))
        self.assertEqual("octopus", Lemmatizer.lemmatize("octopus"))
        self.assertEqual("", Lemmatizer.lemmatize(("")))
        self.assertEqual("", Lemmatizer.lemmatize((None)))

        self.assertEqual("mouse", Lemmatizer.lemmatize('mice'))
        self.assertEqual("fish", Lemmatizer.lemmatize('fish'))
        self.assertEqual("sheep", Lemmatizer.lemmatize('sheep'))
        self.assertEqual("holly", Lemmatizer.lemmatize('hollies'))

