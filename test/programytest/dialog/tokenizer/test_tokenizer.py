import unittest

from programy.dialog.tokenizer.tokenizer import Tokenizer
from programy.config.brain.tokenizer import BrainTokenizerConfiguration


class TokenizerTests(unittest.TestCase):

    def test_default_tokenizer(self):
        tokenizer = Tokenizer()
        self.assertIsNotNone(tokenizer)

        self.assertEqual([], tokenizer.texts_to_words(""))
        self.assertEqual(["Hello"], tokenizer.texts_to_words("Hello"))
        self.assertEqual(["Hello", "World"], tokenizer.texts_to_words("Hello World"))
        self.assertEqual(["Hello", "World"], tokenizer.texts_to_words(" Hello   World "))

        self.assertEqual("", tokenizer.words_to_texts([]))
        self.assertEqual("Hello", tokenizer.words_to_texts(["Hello"]))
        self.assertEqual("Hello World", tokenizer.words_to_texts(["Hello", "World"]))
        self.assertEqual("Hello World", tokenizer.words_to_texts(["Hello", "", "World"]))
        self.assertEqual("Hello World", tokenizer.words_to_texts([" Hello ", " World "]))

    def test_words_from_current_pos(self):
        tokenizer = Tokenizer()
        self.assertIsNotNone(tokenizer)

        self.assertEquals("B C", tokenizer.words_from_current_pos(["A", "B", "C"], 1))

    def test_words_from_current_pos_past_end(self):
        tokenizer = Tokenizer()
        self.assertIsNotNone(tokenizer)

        self.assertEquals("", tokenizer.words_from_current_pos(["A", "B", "C"], 5))

    def test_words_from_current_pos_no_words(self):
        tokenizer = Tokenizer()
        self.assertIsNotNone(tokenizer)

        self.assertEquals("", tokenizer.words_from_current_pos([], 5))
        self.assertEquals("", tokenizer.words_from_current_pos(None, 5))

    def test_load_tokenizer(self):
        config = BrainTokenizerConfiguration()
        config._classname = "programy.dialog.tokenizer.tokenizer.Tokenizer"
        tokenizer = Tokenizer.load_tokenizer(config)
        self.assertIsNotNone(tokenizer)
        self.assertIsInstance(tokenizer, Tokenizer)

    def test_load_invalid_tokenizer(self):
        config = BrainTokenizerConfiguration()
        config._classname = "programy.dialog.tokenizer.tokenizer.TokenizerXXX"
        tokenizer = Tokenizer.load_tokenizer(config)
        self.assertIsNotNone(tokenizer)
        self.assertIsInstance(tokenizer, Tokenizer)

    def test_load_tokenizer_classname_none(self):
        config = BrainTokenizerConfiguration()
        config._classname = None
        tokenizer = Tokenizer.load_tokenizer(config)
        self.assertIsNotNone(tokenizer)
        self.assertIsInstance(tokenizer, Tokenizer)
