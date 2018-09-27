import unittest

from programy.dialog.dialog import Sentence
from programy.bot import Bot
from programy.config.bot.bot import BotConfiguration
from programy.parser.tokenizer import Tokenizer

from programytest.client import TestClient


class SentenceTests(unittest.TestCase):

    def setUp(self):
        client = TestClient()
        self._bot = Bot(BotConfiguration(), client)

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

