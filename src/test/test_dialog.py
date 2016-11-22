import unittest

from programy.dialog import Sentence, Question, Conversation
from programy.bot import Bot
from programy.brain import Brain
from programy.config import BrainConfiguration, BotConfiguration


#############################################################################
#
class SentenceTests(unittest.TestCase):

    def test_sentence_creation_empty(self):
        sentence = Sentence("")
        self.assertIsNotNone(sentence)
        self.assertEqual(0, sentence.num_words())
        with self.assertRaises(Exception):
            sentence.next_word()

    def test_sentence_creation_spaces(self):
        sentence = Sentence(" ")
        self.assertIsNotNone(sentence)
        self.assertEqual(0, sentence.num_words())
        with self.assertRaises(Exception):
            sentence.next_word()

    def test_split_into_words(self):
        sentence = Sentence("HELLO")
        self.assertIsNotNone(sentence)
        self.assertEqual(1, sentence.num_words())
        self.assertEqual("HELLO", sentence.word(0))
        self.assertEqual("HELLO", sentence.words_from_current_pos(0))

    def test_sentence_creation_one_word(self):
        sentence = Sentence("One")
        self.assertIsNotNone(sentence)
        self.assertEqual(1, sentence.num_words())

    def test_sentence_creation_two_words(self):
        sentence = Sentence("One Two")
        self.assertIsNotNone(sentence)
        self.assertEqual(2, sentence.num_words())

    def test_sentence_creation_two_words_diff_split_char(self):
        sentence = Sentence("One,Two", ",")
        self.assertIsNotNone(sentence)
        self.assertEqual(2, sentence.num_words())


#############################################################################
#
class QuestionTests(unittest.TestCase):

    def test_question_no_sentences_empty(self):
        question = Question.create_from_text("")
        self.assertIsNotNone(question)
        self.assertEqual(0, len(question.sentences))

    def test_question_no_sentences_blank(self):
        question = Question.create_from_text(" ")
        self.assertIsNotNone(question)
        self.assertEqual(0, len(question.sentences))

    def test_question_one_sentence(self):
        question = Question.create_from_text("Hello There")
        self.assertIsNotNone(question)
        self.assertEqual(1, len(question.sentences))

    def test_question_multi_sentence(self):
        question = Question.create_from_text("Hello There. How Are you")
        self.assertIsNotNone(question)
        self.assertEqual(2, len(question.sentences))

    def test_combine_answers(self):
        question = Question()
        sentence1 = Sentence("Hi")
        sentence1._response = "Hello"
        question._sentences.append(sentence1)
        sentence2 = Sentence("Hi Again")
        question._sentences.append(sentence2)
        sentence2._response = "World"

        self.assertEqual(2, len(question._sentences))
        self.assertEqual(question._sentences[0]._response, "Hello")
        self.assertEqual(question._sentences[1]._response, "World")

        combined = question.combine_answers()
        self.assertIsNotNone(combined)
        self.assertEqual(combined, "Hello. World")



#############################################################################
#
class ConversationTests(unittest.TestCase):

    def test_conversation(self):
        test_brain = Brain(BrainConfiguration())
        test_bot = Bot(test_brain, BotConfiguration())
        conversation = Conversation("test", test_bot, max_histories=3)
        self.assertIsNotNone(conversation)
        self.assertIsNotNone(conversation._bot)
        self.assertIsNotNone(conversation._clientid)
        self.assertEqual(conversation._clientid, "test")
        self.assertEqual(0, len(conversation._questions))
        self.assertEqual(3, conversation._max_histories)
        self.assertEqual(1, len(conversation._predicates))

        question = Question.create_from_text("Hello There")
        conversation.record_dialog(question)
        self.assertEqual(1, len(conversation._questions))

        question = Question.create_from_text("Hello There Again")
        conversation.record_dialog(question)
        self.assertEqual(2, len(conversation._questions))

        question = Question.create_from_text("Hello There Again Again")
        conversation.record_dialog(question)
        self.assertEqual(3, len(conversation._questions))

        question = Question.create_from_text("Hello There Again Again Again")
        conversation.record_dialog(question)
        self.assertEqual(3, len(conversation._questions))
