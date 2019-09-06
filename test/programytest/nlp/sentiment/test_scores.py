from unittest import TestCase

from programy.nlp.sentiment.scores import SentimentScores


class SentimentScoresTests(TestCase):

    def test_positivity(self):
        scorer = SentimentScores()

        self.assertEqual("EXTREMELY NEGATIVE", scorer.positivity(-1.0))

        self.assertEqual("VERY NEGATIVE", scorer.positivity(-0.8))

        self.assertEqual("QUITE NEGATIVE", scorer.positivity(-0.6))

        self.assertEqual("NEGATIVE", scorer.positivity(-0.4))

        self.assertEqual("SOMEWHAT NEGATIVE", scorer.positivity(-0.2))

        self.assertEqual("NEUTRAL", scorer.positivity(-0.09))
        self.assertEqual("NEUTRAL", scorer.positivity(0.0))
        self.assertEqual("NEUTRAL", scorer.positivity(0.09))

        self.assertEqual("SOMEWHAT POSITIVE", scorer.positivity(0.2))

        self.assertEqual("POSITIVE", scorer.positivity(0.4))

        self.assertEqual("QUITE POSITIVE", scorer.positivity(0.6))

        self.assertEqual("VERY POSITIVE", scorer.positivity(0.8))

        self.assertEqual("EXTREMELY POSITIVE", scorer.positivity(1.0))

    def test_subjectivity(self):
        scorer = SentimentScores()

        self.assertEqual("COMPLETELY OBJECTIVE", scorer.subjectivity(0.0))

        self.assertEqual("MOSTLY OBJECTIVE", scorer.subjectivity(0.01))
        self.assertEqual("MOSTLY OBJECTIVE", scorer.subjectivity(0.1))
        self.assertEqual("MOSTLY OBJECTIVE", scorer.subjectivity(0.2))

        self.assertEqual("SOMEWHAT OBJECTIVE", scorer.subjectivity(0.21))
        self.assertEqual("SOMEWHAT OBJECTIVE", scorer.subjectivity(0.3))
        self.assertEqual("SOMEWHAT OBJECTIVE", scorer.subjectivity(0.4))

        self.assertEqual("NEUTRAL", scorer.subjectivity(0.41))
        self.assertEqual("NEUTRAL", scorer.subjectivity(0.5))
        self.assertEqual("NEUTRAL", scorer.subjectivity(0.6))

        self.assertEqual("SOMEWHAT SUBJECTIVE", scorer.subjectivity(0.61))
        self.assertEqual("SOMEWHAT SUBJECTIVE", scorer.subjectivity(0.7))
        self.assertEqual("SOMEWHAT SUBJECTIVE", scorer.subjectivity(0.8))

        self.assertEqual("MOSTLY SUBJECTIVE", scorer.subjectivity(0.81))
        self.assertEqual("MOSTLY SUBJECTIVE", scorer.subjectivity(0.9))
        self.assertEqual("MOSTLY SUBJECTIVE", scorer.subjectivity(0.99))

        self.assertEqual("COMPLETELY SUBJECTIVE", scorer.subjectivity(1.0))