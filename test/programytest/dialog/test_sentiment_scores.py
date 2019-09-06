import unittest

from programy.dialog.sentence import Sentence
from programy.dialog.question import Question
from programy.dialog.conversation import Conversation
from programy.dialog.tokenizer.tokenizer import Tokenizer
from programy.bot import Bot
from programy.config.bot.bot import BotConfiguration

from programytest.client import TestClient


class SentimentScoreTests(unittest.TestCase):

    def setUp(self):
        self._client = TestClient()

        config = BotConfiguration()
        config.sentiment_analyser._classname = "programy.nlp.sentiment.textblob_sentiment.TextBlobSentimentAnalyser"
        config.sentiment_analyser._scores = "programy.nlp.sentiment.scores.SentimentScores"

        self.client_context = self._client.create_client_context("testuser")

        self.client_context._bot = Bot(config=config, client=self._client)
        self.client_context._bot.initiate_sentiment_analyser()

    def test_sentence_scores(self):
        sentence = Sentence(self.client_context, "")
        sentence.calculate_sentinment_score(self.client_context)
        self.assertEqual(0.0, sentence.positivity)
        self.assertEqual(0.5, sentence.subjectivity)

        sentence = Sentence(self.client_context, "I like you")
        sentence.calculate_sentinment_score(self.client_context)
        self.assertEqual(0.0, sentence.positivity)
        self.assertEqual(0.0, sentence.subjectivity)

        sentence = Sentence(self.client_context, "I hate you")
        sentence.calculate_sentinment_score(self.client_context)
        self.assertEqual(-0.8, sentence.positivity)
        self.assertEqual(0.9, sentence.subjectivity)

        sentence = Sentence(self.client_context, "I think like you")
        sentence.calculate_sentinment_score(self.client_context)
        self.assertEqual(0.0, sentence.positivity)
        self.assertEqual(0.0, sentence.subjectivity)

    def test_question_scores(self):
        question = Question.create_from_text(self.client_context, "")
        pos, sub = question.calculate_sentinment_score()
        self.assertEqual(0.0, pos)
        self.assertEqual(0.5, sub)

    def test_conversation_scores(self):
        conversation = Conversation(self.client_context)
        pos, sub = conversation.calculate_sentiment_score()
        self.assertEqual(0.0, pos)
        self.assertEqual(0.5, sub)

        question1 = Question.create_from_text(self.client_context, "Hello There")
        conversation.record_dialog(question1)
        pos, sub = conversation.calculate_sentiment_score()
        self.assertEqual(0.0, pos)
        self.assertEqual(0.0, sub)

        question2 = Question.create_from_text(self.client_context, "I really like you")
        conversation.record_dialog(question2)
        pos, sub = conversation.calculate_sentiment_score()
        self.assertEqual(0.1, pos)
        self.assertEqual(0.1, sub)

        question3 = Question.create_from_text(self.client_context, "Do you like me")
        conversation.record_dialog(question3)
        pos, sub = conversation.calculate_sentiment_score()
        self.assertEqual(0.06666666666666667, pos)
        self.assertEqual(0.06666666666666667, sub)
