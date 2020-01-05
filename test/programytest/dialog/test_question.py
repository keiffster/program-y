import unittest

from programy.dialog.question import Question
from programy.dialog.sentence import Sentence
from programytest.client import TestClient
from programy.dialog.splitter.regex import RegexSentenceSplitter
from programy.config.bot.splitter import BotSentenceSplitterConfiguration


class QuestionTests(unittest.TestCase):

    def setUp(self):
        client = TestClient()
        self._client_context = client.create_client_context("test1")

    def test_question_set_sentencesy(self):
        question = Question.create_from_text(self._client_context, "")
        self.assertIsNotNone(question)
        self.assertEqual(0, len(question.sentences))

        question.sentences = [Sentence(self._client_context, "Sentence One"), Sentence(self._client_context, "Sentence Two")]
        self.assertEqual(2, len(question.sentences))
        self.assertEqual("Sentence One = N/A, Sentence Two = N/A", question.debug_info(self._client_context))

        self.assertEquals(-1, question.current_sentence_no)
        question.current_sentence_no = 1
        self.assertEquals(1, question.current_sentence_no)

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
        self.assertEqual("Hello There", question.sentence(0).text(self._client_context))
        self.assertEqual("How Are you", question.sentence(1).text(self._client_context))
        with self.assertRaises(Exception):
            question.sentence(2)

    def test_question_create_from_sentence(self):
        sentence = Sentence(self._client_context, "One Two Three")
        question = Question.create_from_sentence(sentence)
        self.assertIsNotNone(question)
        self.assertEqual(1, len(question.sentences))
        self.assertEqual(sentence.text(self._client_context), question.sentence(0).text(self._client_context))
        with self.assertRaises(Exception):
            question.sentence(1)

    def test_question_create_from_question(self):
        question = Question.create_from_text(self._client_context, "Hello There")
        new_question = Question.create_from_question(question)
        self.assertIsNotNone(new_question)
        self.assertEqual(1, len(new_question.sentences))
        self.assertEqual("Hello There", question.sentence(0).text(self._client_context))
        with self.assertRaises(Exception):
            question.sentence(1)

    def test_combine_answers(self):
        question = Question()
        sentence1 = Sentence(self._client_context, "Hi")
        sentence1._response = "Hello"
        question.sentences.append(sentence1)
        sentence2 = Sentence(self._client_context, "Hi Again")
        question.sentences.append(sentence2)
        sentence2._response = "World"

        self.assertEqual(2, len(question.sentences))
        self.assertEqual(question.sentences[0]._response, "Hello")
        self.assertEqual(question.sentences[1]._response, "World")

        sentences = question.combine_sentences(self._client_context)
        self.assertEqual("Hi. Hi Again", sentences)

        combined = question.combine_answers()
        self.assertIsNotNone(combined)
        self.assertEqual(combined, "Hello. World")

        self.assertEquals("Hi = Hello, Hi Again = World", question.debug_info(self._client_context))

    def test_next_previous_sentences(self):
        question = Question.create_from_text(self._client_context, "Hello There. How Are you")
        self.assertEqual("How Are you", question.current_sentence().text(self._client_context))
        self.assertEqual("Hello There", question.previous_nth_sentence(1).text(self._client_context))

    def test_next_previous_sentences_exception(self):
        question = Question.create_from_text(self._client_context, "Hello There. How Are you")
        with self.assertRaises(Exception):
            question.previous_nth_sentence(2)

    def test_next_previous_nth_sentences(self):
        question = Question.create_from_text(self._client_context, "Hello There. How Are you")
        self.assertEqual("How Are you", question.current_sentence().text(self._client_context))
        self.assertEqual("How Are you", question.previous_nth_sentence(0).text(self._client_context))
        self.assertEqual("Hello There", question.previous_nth_sentence(1).text(self._client_context))

    def test_to_json(self):
        question = Question()
        sentence1 = Sentence(self._client_context, "Hi")
        sentence1._response = "Hello"
        question.sentences.append(sentence1)
        sentence2 = Sentence(self._client_context, "Hi Again")
        question.sentences.append(sentence2)
        sentence2._response = "World"

        json_data = question.to_json()
        self.assertIsNotNone(json_data)

        self.assertEqual(False, json_data["srai"])
        self.assertEqual(-1, json_data["current_sentence_no"])
        self.assertEqual({}, json_data["properties"])
        self.assertEqual(2, len(json_data["sentences"]))

    def test_from_json(self):

        json_data = {'srai': False,
                     'sentences': [
                         {'words': ['Hi'], 'response': 'Hello', 'positivity': 0.0, 'subjectivity': 0.5},
                         {'words': ['Hi', 'Again'], 'response': 'World', 'positivity': 0.0, 'subjectivity': 0.5}],
                     'current_sentence_no': -1,
                     'properties': {}
                     }

        question = Question.from_json(self._client_context, json_data)
        self.assertIsNotNone(question)

        self.assertEqual(False, question.srai)
        self.assertEqual({}, question.properties)
        self.assertEqual(-1, question._current_sentence_no)
        self.assertEqual(2, len(question.sentences))
        splitter = RegexSentenceSplitter(BotSentenceSplitterConfiguration())
        self.assertIsNotNone(splitter)

        self.assertEqual(["This is a basic sentence"], splitter.split("This is a basic sentence"))
