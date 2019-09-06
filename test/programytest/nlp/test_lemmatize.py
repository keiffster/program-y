import unittest

from programy.nlp.lemmatize import Lemmatizer


class LemmatizerTests(unittest.TestCase):

    def test_lemmatize(self):
        self.assertEquals("octopus", Lemmatizer.lemmatize("octopi"))
        self.assertEquals("octopus", Lemmatizer.lemmatize("octopus"))
        self.assertEquals("", Lemmatizer.lemmatize(("")))

        self.assertEquals("mouse", Lemmatizer.lemmatize('mice'))
        self.assertEquals("fish", Lemmatizer.lemmatize('fish'))
        self.assertEquals("sheep", Lemmatizer.lemmatize('sheep'))
        self.assertEquals("holly", Lemmatizer.lemmatize('hollies'))

