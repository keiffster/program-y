import unittest

from programy.dialog.dialog import Sentence, Question, Conversation
from programy.bot import Bot
from programy.config.bot.bot import BotConfiguration
from programy.parser.tokenizer import Tokenizer
from programy.context import ClientContext

from programytest.aiml_tests.client import TestClient

#############################################################################
#
class SentenceTests(unittest.TestCase):

    def setUp(self):
        self._bot = Bot(BotConfiguration())

    def test_sentence_creation_empty(self):
        sentence = Sentence(self._bot.brain.tokenizer, "")
        self.assertIsNotNone(sentence)
        self.assertEqual(0, sentence.num_words())
        with self.assertRaises(Exception):
            sentence.sentence.word(0)

    def test_sentence_creation_spaces(self):
        sentence = Sentence(self._bot.brain.tokenizer, " ")
        self.assertIsNotNone(sentence)
        self.assertEqual(0, sentence.num_words())
        with self.assertRaises(Exception):
            sentence.sentence.word(0)

    def test_split_into_words(self):
        sentence = Sentence(self._bot.brain.tokenizer, "HELLO")
        self.assertIsNotNone(sentence)
        self.assertEqual(1, sentence.num_words())
        self.assertEqual("HELLO", sentence.word(0))
        self.assertEqual("HELLO", sentence.words_from_current_pos(0))
        with self.assertRaises(Exception):
            sentence.sentence.word(1)
        self.assertEqual("HELLO", sentence.text())

    def test_sentence_creation_one_word(self):
        sentence = Sentence(self._bot.brain.tokenizer, "One")
        self.assertIsNotNone(sentence)
        self.assertEqual(1, sentence.num_words())
        with self.assertRaises(Exception):
            sentence.sentence.word(1)
        self.assertEqual("One", sentence.text())

    def test_sentence_creation_two_words(self):
        sentence = Sentence(self._bot.brain.tokenizer, "One Two")
        self.assertIsNotNone(sentence)
        self.assertEqual(2, sentence.num_words())
        self.assertEqual("One", sentence.word(0))
        self.assertEqual("Two", sentence.word(1))
        with self.assertRaises(Exception):
            sentence.sentence.word(2)
        self.assertEqual("One Two", sentence.text())

    def test_sentence_creation_two_words_diff_split_char(self):
        tokenizer = Tokenizer(",")
        sentence = Sentence(tokenizer, "One,Two",)
        self.assertIsNotNone(sentence)
        self.assertEqual(2, sentence.num_words())
        self.assertEqual("One", sentence.word(0))
        self.assertEqual("Two", sentence.word(1))
        with self.assertRaises(Exception):
            sentence.sentence.word(2)
        self.assertEqual("One,Two", sentence.text())

    def test_words_from_current_pos(self):
        sentence = Sentence(self._bot.brain.tokenizer, "One Two Three")
        self.assertIsNotNone(sentence)
        self.assertEqual("One Two Three", sentence.words_from_current_pos(0))
        self.assertEqual("Two Three", sentence.words_from_current_pos(1))
        self.assertEqual("Three", sentence.words_from_current_pos(2))
        with self.assertRaises(Exception):
            self.assertEqual("Three", sentence.words_from_current_pos(3))
        self.assertEqual("One Two Three", sentence.text())


#############################################################################
#
class QuestionTests(unittest.TestCase):

    def setUp(self):
        bot_config = BotConfiguration()
        bot_config.conversations._max_histories = 3
        self._bot = Bot(bot_config)

    def test_question_no_sentences_empty(self):
        question = Question.create_from_text(self._bot.brain.tokenizer, "")
        self.assertIsNotNone(question)
        self.assertEqual(0, len(question.sentences))

    def test_question_no_sentences_blank(self):
        question = Question.create_from_text(self._bot.brain.tokenizer, " ")
        self.assertIsNotNone(question)
        self.assertEqual(0, len(question.sentences))

    def test_question_one_sentence(self):
        question = Question.create_from_text(self._bot.brain.tokenizer, "Hello There")
        self.assertIsNotNone(question)
        self.assertEqual(1, len(question.sentences))

    def test_question_multi_sentence(self):
        question = Question.create_from_text(self._bot.brain.tokenizer, "Hello There. How Are you")
        self.assertIsNotNone(question)
        self.assertEqual(2, len(question.sentences))
        self.assertEqual("Hello There", question.sentence(0).text())
        self.assertEqual("How Are you", question.sentence(1).text())
        with self.assertRaises(Exception):
            question.sentence(2)

    def test_question_create_from_sentence(self):
        sentence = Sentence(self._bot.brain.tokenizer, "One Two Three")
        question = Question.create_from_sentence(sentence)
        self.assertIsNotNone(question)
        self.assertEqual(1, len(question.sentences))
        self.assertEqual(sentence.text(), question.sentence(0).text())
        with self.assertRaises(Exception):
            question.sentence(1)

    def test_question_create_from_question(self):
        question = Question.create_from_text(self._bot.brain.tokenizer, "Hello There")
        new_question = Question.create_from_question(question)
        self.assertIsNotNone(new_question)
        self.assertEqual(1, len(new_question.sentences))
        self.assertEqual("Hello There", question.sentence(0).text())
        with self.assertRaises(Exception):
            question.sentence(1)

    def test_combine_answers(self):
        question = Question()
        sentence1 = Sentence(self._bot.brain.tokenizer, "Hi")
        sentence1._response = "Hello"
        question._sentences.append(sentence1)
        sentence2 = Sentence(self._bot.brain.tokenizer, "Hi Again")
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
        question = Question.create_from_text(self._bot.brain.tokenizer, "Hello There. How Are you")
        self.assertEqual("How Are you", question.current_sentence().text())
        self.assertEqual("Hello There", question.previous_nth_sentence(1).text())

    def test_next_previous_nth_sentences(self):
        question = Question.create_from_text(self._bot.brain.tokenizer, "Hello There. How Are you")
        self.assertEqual("How Are you", question.current_sentence().text())
        self.assertEqual("How Are you", question.previous_nth_sentence(0).text())
        self.assertEqual("Hello There", question.previous_nth_sentence(1).text())


#############################################################################
#
class ConversationTests(unittest.TestCase):

    def test_conversation(self):

        client_context = ClientContext(TestClient(), "testid")
        client_context.bot = Bot(BotConfiguration())
        client_context.bot.configuration.conversations._max_histories = 3
        client_context.brain = client_context.bot.brain

        conversation = Conversation(client_context)
        self.assertIsNotNone(conversation)
        self.assertEqual(0, len(conversation._questions))
        self.assertEqual(3, conversation._max_histories)
        self.assertEqual(1, len(conversation._properties))

        with self.assertRaises(Exception):
            conversation.current_question()
        with self.assertRaises(Exception):
            conversation.previous_nth_question(0)

        question1 = Question.create_from_text(client_context.brain.tokenizer, "Hello There")
        conversation.record_dialog(question1)
        self.assertEqual(question1, conversation.current_question())
        with self.assertRaises(Exception):
            conversation.previous_nth_question(1)

        question2 = Question.create_from_text(client_context.brain.tokenizer, "Hello There Again")
        conversation.record_dialog(question2)
        self.assertEqual(question2, conversation.current_question())
        self.assertEqual(question1, conversation.previous_nth_question(1))
        with self.assertRaises(Exception):
            conversation.previous_nth_question(3)

        question3 = Question.create_from_text(client_context.brain.tokenizer, "Hello There Again Again")
        conversation.record_dialog(question3)
        self.assertEqual(question3, conversation.current_question())
        self.assertEqual(question2, conversation.previous_nth_question(1))
        with self.assertRaises(Exception):
            conversation.previous_nth_question(4)

        # Max Histories for this test is 3
        # Therefore we should see the first question, pop of the stack

        question4 = Question.create_from_text(client_context.brain.tokenizer, "Hello There Again Again Again")
        conversation.record_dialog(question4)
        self.assertEqual(question4, conversation.current_question())
        self.assertEqual(question3, conversation.previous_nth_question(1))
        with self.assertRaises(Exception):
            conversation.previous_nth_question(5)

