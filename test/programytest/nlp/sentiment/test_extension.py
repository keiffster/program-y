import unittest

from programy.bot import Bot
from programy.config.bot.bot import BotConfiguration
from programy.nlp.sentiment.extension import SentimentExtension

from programytest.client import TestClient


class SentimentExtensionTests(unittest.TestCase):

    def setUp(self):
        self._client = TestClient()

        config = BotConfiguration()
        config.sentiment_analyser._classname = "programy.nlp.sentiment.textblob_sentiment.TextBlobSentimentAnalyser"
        config.sentiment_analyser._scores = "programy.nlp.sentiment.scores.SentimentScores"

        self.client_context = self._client.create_client_context("testuser")

        self.client_context._bot = Bot(config=config, client=self._client)
        self.client_context._bot.initiate_sentiment_analyser()

    def test_invalid_command(self):

        extension = SentimentExtension()
        self.assertIsNotNone(extension)

        result = extension.execute(self.client_context, "XXX")
        self.assertIsNotNone(result)
        self.assertEqual("SENTIMENT INVALID COMMAND", result)

        result = extension.execute(self.client_context, "SENTIMENT")
        self.assertIsNotNone(result)
        self.assertEqual("SENTIMENT INVALID COMMAND", result)

        result = extension.execute(self.client_context, "SENTIMENT SCOREX")
        self.assertIsNotNone(result)
        self.assertEqual("SENTIMENT INVALID COMMAND", result)

        result = extension.execute(self.client_context, "SENTIMENT FEELING")
        self.assertIsNotNone(result)
        self.assertEqual("SENTIMENT INVALID COMMAND", result)

        result = extension.execute(self.client_context, "SENTIMENT FEELING LAST")
        self.assertIsNotNone(result)
        self.assertEqual("SENTIMENT INVALID COMMAND", result)

        result = extension.execute(self.client_context, "SENTIMENT SCORES")
        self.assertIsNotNone(result)
        self.assertEqual("SENTIMENT INVALID COMMAND", result)

        result = extension.execute(self.client_context, "SENTIMENT CURRENT")
        self.assertIsNotNone(result)
        self.assertEqual("SENTIMENT INVALID COMMAND", result)

    def test_valid_scores_command(self):

        extension = SentimentExtension()
        self.assertIsNotNone(extension)

        result = extension.execute(self.client_context, "SENTIMENT ENABLED")
        self.assertIsNotNone(result)
        self.assertEqual("SENTIMENT ENABLED", result)

        result = extension.execute(self.client_context, "SENTIMENT FEELING LAST 1")
        self.assertIsNotNone(result)
        self.assertEqual("SENTIMENT FEELING NEUTRAL AND NEUTRAL", result)

        result = extension.execute(self.client_context, "SENTIMENT FEELING OVERALL")
        self.assertIsNotNone(result)
        self.assertEqual("SENTIMENT FEELING NEUTRAL AND NEUTRAL", result)

        result = extension.execute(self.client_context, "SENTIMENT SCORE I LIKE YOU")
        self.assertIsNotNone(result)
        self.assertEqual("SENTIMENT SCORES POSITIVITY NEUTRAL SUBJECTIVITY COMPLETELY OBJECTIVE", result)
