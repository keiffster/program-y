import unittest

from programy.nlp.sentiment.textblob_sentiment import TextBlobSentimentAnalyser


class TestTextBlobSentimentAnalyser(unittest.TestCase):

    def test_analyse_each(self):
        analyser = TextBlobSentimentAnalyser()
        results = analyser.analyse_each("Programy-Y is awesome. I love it")
        self.assertEquals([(1.0, 1.0), (0.5, 0.6)], results)

    def test_analyse_all(self):
        analyser = TextBlobSentimentAnalyser()
        results = analyser.analyse_all("Programy-Y is awesome. I love it")
        self.assertEquals((0.75, 0.8), results)