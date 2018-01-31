import unittest

from programy.parser.tokenizer import Tokenizer
from programy.parser.tokenizer import CjkTokenizer


class FactoryTests(unittest.TestCase):

    def test_default_tokenizer(self):
        tokenizer = Tokenizer()
        self.assertIsNotNone(tokenizer)

        self.assertEquals([], tokenizer.texts_to_words(""))
        self.assertEquals(["Hello"], tokenizer.texts_to_words("Hello"))
        self.assertEquals(["Hello", "World"], tokenizer.texts_to_words("Hello World"))
        self.assertEquals(["Hello", "World"], tokenizer.texts_to_words(" Hello   World "))

        self.assertEquals("", tokenizer.words_to_texts([]))
        self.assertEquals("Hello", tokenizer.words_to_texts(["Hello"]))
        self.assertEquals("Hello World", tokenizer.words_to_texts(["Hello", "World"]))
        self.assertEquals("Hello World", tokenizer.words_to_texts(["Hello", "", "World"]))
        self.assertEquals("Hello World", tokenizer.words_to_texts([" Hello ", " World "]))

    def test_cjk_tokenizer(self):
        tokenizer = CjkTokenizer()
        self.assertIsNotNone(tokenizer)

        self.assertEquals([], tokenizer.texts_to_words(""))
        self.assertEquals(["Hello"], tokenizer.texts_to_words("Hello"))
        self.assertEquals(["Hello", "World"], tokenizer.texts_to_words("Hello World"))
        self.assertEquals(["Hello", "World"], tokenizer.texts_to_words(" Hello   World "))

        self.assertEquals(["半", "宽", "韩", "文", "字", "母"], tokenizer.texts_to_words("半宽韩文字母"))
        self.assertEquals(["半", "宽", "韩", "文", "字", "母", "半", "宽", "平", "假", "名"], tokenizer.texts_to_words("半宽韩文字母 半宽平假名"))

        self.assertEquals("", tokenizer.words_to_texts([]))
        self.assertEquals("Hello", tokenizer.words_to_texts(["Hello"]))
        self.assertEquals("Hello World", tokenizer.words_to_texts(["Hello", "World"]))
        self.assertEquals("Hello World", tokenizer.words_to_texts(["Hello", "", "World"]))
        self.assertEquals("Hello World", tokenizer.words_to_texts([" Hello ", " World "]))

        self.assertEquals("半宽韩文字母", tokenizer.words_to_texts(["半", "宽", "韩", "文", "字", "母"]))
        self.assertEquals("半宽韩文字母 半宽平假名", tokenizer.words_to_texts(["半", "宽", "韩", "文", "字", "母", " ", "半", "宽", "平", "假", "名"]))

        self.assertEquals(["200", "万"], tokenizer.texts_to_words("200万"))
        self.assertEquals("200万", tokenizer.words_to_texts(["200", "万"]))

        self.assertEquals("(200万 ,100万 ,50万 )", tokenizer.words_to_texts(["(", "200万", ",", "100万", ",", "50万", ")"]))

