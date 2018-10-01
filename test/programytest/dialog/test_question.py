import unittest

from programy.dialog.dialog import Sentence, Question, Conversation
from programy.bot import Bot
from programy.config.bot.bot import BotConfiguration
from programy.context import ClientContext

from programytest.client import TestClient


class QuestionTests(unittest.TestCase):

    def setUp(self):
        client = TestClient()
        self._client_context = client.create_client_context("test1")
        bot_config = BotConfiguration()
        bot_config.conversations._max_histories = 3
        self._bot = Bot(bot_config, client)

    def test_question_no_sentences_empty(self):
        question = Question.create_from_text(self._client_context, "")
        self.assertIsNotNone(question)
        self.assertEqual(0, len(question.sentences))

    def test_question_no_sentences_blank(self):
        question = Question.create_from_text(self._client_context, " ")
        self.assertIsNotNone(question)
        self.assertEqual(0, len(question.sentences))

    def test_question_one_sentence(self):
        question = Question.create_from_text(self._client_context, "Hello There")
        self.assertIsNotNone(question)
        self.assertEqual(1, len(question.sentences))

    def test_question_multi_sentence(self):
        question = Question.create_from_text(self._client_context, "Hello There. How Are you")
        self.assertIsNotNone(question)
        self.assertEqual(2, len(question.sentences))
        self.assertEqual("Hello There", question.sentence(0).text())
        self.assertEqual("How Are you", question.sentence(1).text())
        with self.assertRaises(Exception):
            question.sentence(2)

    def test_question_create_from_sentence(self):
        sentence = Sentence(self._client_context, "One Two Three")
        question = Question.create_from_sentence(sentence)
        self.assertIsNotNone(question)
        self.assertEqual(1, len(question.sentences))
        self.assertEqual(sentence.text(), question.sentence(0).text())
        with self.assertRaises(Exception):
            question.sentence(1)

    def test_question_create_from_question(self):
        question = Question.create_from_text(self._client_context, "Hello There")
        new_question = Question.create_from_question(question)
        self.assertIsNotNone(new_question)
        self.assertEqual(1, len(new_question.sentences))
        self.assertEqual("Hello There", question.sentence(0).text())
        with self.assertRaises(Exception):
            question.sentence(1)

    def test_combine_answers(self):
        question = Question()
        sentence1 = Sentence(self._client_context, "Hi")
        sentence1._response = "Hello"
        question._sentences.append(sentence1)
        sentence2 = Sentence(self._client_context, "Hi Again")
        question._sentences.append(sentence2)
        sentence2._response = "World"

        self.assertEqual(2, len(question._sentences))
        self.assertEqual(question._sentences[0]._response, "Hello")
        self.assertEqual(question._sentences[1]._response, "World")

        sentences = question.combine_sentences()
        self.assertEqual("Hi. Hi Again", sentences)

        combined = question.combine_answers()
        self.assertIsNotNone(combined)
        self.assertEqual(combined, "Hello. World")

    def test_next_previous_sentences(self):
        question = Question.create_from_text(self._client_context, "Hello There. How Are you")
        self.assertEqual("How Are you", question.current_sentence().text())
        self.assertEqual("Hello There", question.previous_nth_sentence(1).text())

    def test_next_previous_nth_sentences(self):
        question = Question.create_from_text(self._client_context, "Hello There. How Are you")
        self.assertEqual("How Are you", question.current_sentence().text())
        self.assertEqual("How Are you", question.previous_nth_sentence(0).text())
        self.assertEqual("Hello There", question.previous_nth_sentence(1).text())

