import unittest
import os

from programytest.client import TestClient

class SentimentTestClient(TestClient):

    def __init__(self):
        TestClient.__init__(self)

    def load_storage(self):
        super(SentimentTestClient, self).load_storage()
        self.add_default_stores()
        self.add_categories_store([os.path.dirname(__file__)])
        self.add_defaults_store(os.path.dirname(__file__) + os.sep + "defaults.txt")

    def load_configuration(self, arguments):
        super(SentimentTestClient, self).load_configuration(arguments)
        self.configuration.client_configuration.configurations[0]._sentiment._classname = "programy.nlp.sentiment.textblob_sentiment.TextBlobSentimentAnalyser"
        self.configuration.client_configuration.configurations[0]._sentiment._scores = "programy.nlp.sentiment.scores.SentimentScores"


class SentimentAIMLTests(unittest.TestCase):

    def setUp(self):
        client = SentimentTestClient()
        self._client_context = client.create_client_context("testid")

    def test_conversation_sentiment(self):
        response = self._client_context.bot.ask_question(self._client_context,  "I LOVE FRED")
        self.assertIsNotNone(response)
        self.assertEqual(response, 'Done.')

        response = self._client_context.bot.ask_question(self._client_context, "CONVERSATION SENTIMENT")
        self.assertIsNotNone(response)
        self.assertEqual(response, '0.5 0.6.')

    def test_conversation_sentiment(self):
        response = self._client_context.bot.ask_question(self._client_context,  "I LOVE FRED")
        self.assertIsNotNone(response)
        self.assertEqual(response, 'Done.')

        response = self._client_context.bot.ask_question(self._client_context, "CURRENT SENTIMENT NUMERIC")
        self.assertIsNotNone(response)
        self.assertEqual(response, 'SENTIMENT SCORES POSITIVITY 0.5 SUBJECTIVITY 0.6.')

        response = self._client_context.bot.ask_question(self._client_context, "CURRENT SENTIMENT TEXT")
        self.assertIsNotNone(response)
        self.assertEqual(response, 'SENTIMENT SCORES POSITIVITY SOMEWHAT POSITIVE SUBJECTIVITY NEUTRAL.')

    def test_negative_sentiment(self):
        response = self._client_context.bot.ask_question(self._client_context,  "I REALLY REALLY HATE YOU")
        self.assertIsNotNone(response)
        self.assertEqual(response, 'Done.')

        response = self._client_context.bot.ask_question(self._client_context, "CURRENT SENTIMENT NUMERIC")
        self.assertIsNotNone(response)
        self.assertEqual(response, 'SENTIMENT SCORES POSITIVITY -0.8 SUBJECTIVITY 0.9.')

    def test_calc_sentiment_score(self):
        response = self._client_context.bot.ask_question(self._client_context,  "CALCULATE SENTIMENT SCORE I REALLY REALLY HATE YOU")
        self.assertIsNotNone(response)
        self.assertEqual(response, 'SENTIMENT SCORES POSITIVITY VERY NEGATIVE SUBJECTIVITY MOSTLY SUBJECTIVE.')

    def test_calc_sentiment_feeling_last_n(self):
        response = self._client_context.bot.ask_question(self._client_context,  "I LOVE FRED")
        self.assertIsNotNone(response)
        self.assertEqual(response, 'Done.')

        response = self._client_context.bot.ask_question(self._client_context,  "CALCULATE SENTIMENT FEELING LAST 1")
        self.assertIsNotNone(response)
        self.assertEqual(response, 'SENTIMENT FEELING NEUTRAL AND NEUTRAL.')

    def test_calc_sentiment_feeling_overall(self):
        response = self._client_context.bot.ask_question(self._client_context,  "CALCULATE SENTIMENT FEELING OVERALL")
        self.assertIsNotNone(response)
        self.assertEqual(response, 'SENTIMENT FEELING NEUTRAL AND COMPLETELY OBJECTIVE.')

    def test_get_positivity_score(self):
        response = self._client_context.bot.ask_question(self._client_context,  "GET SENTIMENT POSITIVITY 0 dot 0")
        self.assertIsNotNone(response)
        self.assertEqual(response, 'NEUTRAL.')

    def test_get_subjectivity_score(self):
        response = self._client_context.bot.ask_question(self._client_context,  "GET SENTIMENT POSITIVITY 0 dot 0")
        self.assertIsNotNone(response)
        self.assertEqual(response, 'NEUTRAL.')

    def test_sentiment_enabled(self):
        response = self._client_context.bot.ask_question(self._client_context,  "IS SENTIMENT ENABLED")
        self.assertIsNotNone(response)
        self.assertEqual(response, 'SENTIMENT ENABLED.')


