import unittest
from programy.bot import Bot
from programy.config.bot.bot import BotConfiguration
from programy.nlp.sentiment.extension import SentimentExtension
from programy.dialog.question import Question
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

        result = extension.execute(self.client_context, "")
        self.assertIsNotNone(result)
        self.assertEqual("SENTIMENT INVALID COMMAND", result)

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

        result = extension.execute(self.client_context, "SENTIMENT FEELING X")
        self.assertIsNotNone(result)
        self.assertEqual("SENTIMENT INVALID COMMAND", result)

        result = extension.execute(self.client_context, "SENTIMENT FEELING LAST")
        self.assertIsNotNone(result)
        self.assertEqual("SENTIMENT INVALID COMMAND", result)

        result = extension.execute(self.client_context, "SENTIMENT FEELING LAST ONE")
        self.assertIsNotNone(result)
        self.assertEqual("SENTIMENT INVALID COMMAND", result)

        result = extension.execute(self.client_context, "SENTIMENT FEELING OTHER    ")
        self.assertIsNotNone(result)
        self.assertEqual("SENTIMENT INVALID COMMAND", result)

        result = extension.execute(self.client_context, "SENTIMENT SCORES")
        self.assertIsNotNone(result)
        self.assertEqual("SENTIMENT INVALID COMMAND", result)

        result = extension.execute(self.client_context, "SENTIMENT CURRENT")
        self.assertIsNotNone(result)
        self.assertEqual("SENTIMENT INVALID COMMAND", result)

    def test_sentiment_enabled(self):

        extension = SentimentExtension()
        self.assertIsNotNone(extension)

        result = extension.execute(self.client_context, "SENTIMENT ENABLED")
        self.assertIsNotNone(result)
        self.assertEqual("SENTIMENT ENABLED", result)

    def test_sentiment_disabled(self):
        extension = SentimentExtension()
        self.assertIsNotNone(extension)

        self.client_context.bot._sentiment_analyser = None

        result = extension.execute(self.client_context, "SENTIMENT ENABLED")
        self.assertIsNotNone(result)
        self.assertEqual("SENTIMENT DISABLED", result)

    def test_sentiment_feeling_current_numeric(self):
        extension = SentimentExtension()
        self.assertIsNotNone(extension)

        conversation = self.client_context.bot.get_conversation(self.client_context)
        self.assertIsNotNone(conversation)
        conversation.properties['positivity'] = 0.00
        conversation.properties['subjectivity'] = 0.00

        result = extension.execute(self.client_context, "SENTIMENT CURRENT NUMERIC")
        self.assertIsNotNone(result)
        self.assertEqual("SENTIMENT SCORES POSITIVITY 0.0 SUBJECTIVITY 0.0", result)

    def test_sentiment_feeling_current_text(self):
        extension = SentimentExtension()
        self.assertIsNotNone(extension)

        conversation = self.client_context.bot.get_conversation(self.client_context)
        self.assertIsNotNone(conversation)
        conversation.properties['positivity'] = 0.00
        conversation.properties['subjectivity'] = 0.00

        result = extension.execute(self.client_context, "SENTIMENT CURRENT TEXT")
        self.assertIsNotNone(result)
        self.assertEqual("SENTIMENT SCORES POSITIVITY NEUTRAL SUBJECTIVITY COMPLETELY OBJECTIVE", result)

    def test_sentiment_feeling_current_other(self):
        extension = SentimentExtension()
        self.assertIsNotNone(extension)

        conversation = self.client_context.bot.get_conversation(self.client_context)
        self.assertIsNotNone(conversation)
        conversation.properties['positivity'] = 0.00
        conversation.properties['subjectivity'] = 0.00

        result = extension.execute(self.client_context, "SENTIMENT CURRENT OTHER")
        self.assertIsNotNone(result)
        self.assertEqual("SENTIMENT INVALID COMMAND", result)

    def test_sentiment_score(self):
        extension = SentimentExtension()
        self.assertIsNotNone(extension)

        result = extension.execute(self.client_context, "SENTIMENT SCORE I LIKE PEAS")
        self.assertIsNotNone(result)
        self.assertEqual("SENTIMENT SCORES POSITIVITY NEUTRAL SUBJECTIVITY COMPLETELY OBJECTIVE", result)

    def test_sentiment_score_no_analyser(self):
        extension = SentimentExtension()
        self.assertIsNotNone(extension)

        self.client_context.bot._sentiment_analyser = None

        result = extension.execute(self.client_context, "SENTIMENT SCORE I LIKE PEAS")
        self.assertIsNotNone(result)
        self.assertEqual("SENTIMENT DISABLED", result)

    def test_sentiment_feeling_last(self):
        extension = SentimentExtension()
        self.assertIsNotNone(extension)

        # Need to create a conversation first

        conversation = self.client_context.bot.get_conversation(self.client_context)
        question1 = Question.create_from_text(self.client_context, "Hello", self.client_context.bot.sentence_splitter)
        conversation.record_dialog(question1)
        question2 = Question.create_from_text(self.client_context, "Hello", self.client_context.bot.sentence_splitter)
        conversation.record_dialog(question2)
        conversation.recalculate_sentiment_score(self.client_context)

        result = extension.execute(self.client_context, "SENTIMENT FEELING LAST 1")
        self.assertIsNotNone(result)
        self.assertEqual("SENTIMENT FEELING NEUTRAL AND COMPLETELY OBJECTIVE", result)

    def test_sentiment_feeling_last_10(self):
        extension = SentimentExtension()
        self.assertIsNotNone(extension)

        # Need to create a conversation first

        conversation = self.client_context.bot.get_conversation(self.client_context)
        self.assertIsNotNone(conversation)
        question = Question.create_from_text(self.client_context, "Hello", self.client_context.bot.sentence_splitter)
        conversation.record_dialog(question)

        result = extension.execute(self.client_context, "SENTIMENT FEELING LAST 10")
        self.assertIsNotNone(result)
        self.assertEqual("SENTIMENT FEELING NEUTRAL AND NEUTRAL", result)

    def test_sentiment_feeling_overall(self):
        extension = SentimentExtension()
        self.assertIsNotNone(extension)

        result = extension.execute(self.client_context, "SENTIMENT FEELING OVERALL")
        self.assertIsNotNone(result)
        self.assertEqual("SENTIMENT FEELING NEUTRAL AND NEUTRAL", result)

    def test_sentiment_feeling_no_scores(self):
        extension = SentimentExtension()
        self.assertIsNotNone(extension)

        self.client_context.bot._sentiment_scores = None

        result = extension.execute(self.client_context, "SENTIMENT FEELING OVERALL")

        self.assertIsNotNone(result)
        self.assertEqual("SENTIMENT FEELING NEUTRAL AND NEUTRAL", result)

    def test_sentiment_feeling_disabled(self):
        extension = SentimentExtension()
        self.assertIsNotNone(extension)

        self.client_context.bot._sentiment_analyser = None

        result = extension.execute(self.client_context, "SENTIMENT FEELING LAST 1")
        self.assertIsNotNone(result)
        self.assertEqual("SENTIMENT DISABLED", result)

    def test_sentiment_score_disabled(self):
        extension = SentimentExtension()
        self.assertIsNotNone(extension)

        self.client_context.bot._sentiment_scores = None

        result = extension.execute(self.client_context, "SENTIMENT SCORE I LIKE YOU")
        self.assertIsNotNone(result)
        self.assertEqual("SENTIMENT SCORES POSITIVITY UNKNOWN SUBJECTIVITY UNKNOWN", result)

    def test_sentiment_sentiment_score(self):
        extension = SentimentExtension()
        self.assertIsNotNone(extension)

        result = extension.execute(self.client_context, "SENTIMENT SCORE I LIKE YOU")
        self.assertIsNotNone(result)
        self.assertEqual("SENTIMENT SCORES POSITIVITY NEUTRAL SUBJECTIVITY COMPLETELY OBJECTIVE", result)

    def test_sentiment_sentiment_positivity(self):
        extension = SentimentExtension()
        self.assertIsNotNone(extension)

        result = extension.execute(self.client_context, "SENTIMENT POSITIVITY 0.1")
        self.assertIsNotNone(result)
        self.assertEqual("NEUTRAL", result)

    def test_sentiment_sentiment_positivity(self):
        extension = SentimentExtension()
        self.assertIsNotNone(extension)

        result = extension.execute(self.client_context, "SENTIMENT SUBJECTIVITY 0.5")
        self.assertIsNotNone(result)
        self.assertEqual("NEUTRAL", result)

