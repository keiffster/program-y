import unittest

from programy.dialog.tokenizer.cjk import CjkTokenizer


class CjkTokenizerTests(unittest.TestCase):

    def test_cjk_tokenizer(self):
        tokenizer = CjkTokenizer()
        self.assertIsNotNone(tokenizer)

        self.assertEqual([], tokenizer.texts_to_words(""))
        self.assertEqual(["Hello"], tokenizer.texts_to_words("Hello"))
        self.assertEqual(["Hello", "World"], tokenizer.texts_to_words("Hello World"))
        self.assertEqual(["Hello", "World"], tokenizer.texts_to_words(" Hello   World "))

        self.assertEqual(["半", "宽", "韩", "文", "字", "母"], tokenizer.texts_to_words("半宽韩文字母"))
        self.assertEqual(["半", "宽", "韩", "文", "字", "母", "半", "宽", "平", "假", "名"], tokenizer.texts_to_words("半宽韩文字母 半宽平假名"))

        self.assertEqual("", tokenizer.words_to_texts([]))
        self.assertEqual("Hello", tokenizer.words_to_texts(["Hello"]))
        self.assertEqual("Hello World", tokenizer.words_to_texts(["Hello", "World"]))
        self.assertEqual("Hello World", tokenizer.words_to_texts(["Hello", "", "World"]))
        self.assertEqual("Hello World", tokenizer.words_to_texts([" Hello ", " World "]))

        self.assertEqual("半宽韩文字母", tokenizer.words_to_texts(["半", "宽", "韩", "文", "字", "母"]))
        self.assertEqual("半宽韩文字母 半宽平假名", tokenizer.words_to_texts(["半", "宽", "韩", "文", "字", "母", " ", "半", "宽", "平", "假", "名"]))

        self.assertEqual(["200", "万"], tokenizer.texts_to_words("200万"))
        self.assertEqual("200万", tokenizer.words_to_texts(["200", "万"]))

        self.assertEqual("(200万 ,100万 ,50万 )", tokenizer.words_to_texts(["(", "200万", ",", "100万", ",", "50万", ")"]))


        self.assertEqual(['你', '好', '！'], tokenizer.texts_to_words('你好！'))


        self.assertEqual(['你', '好', '！'], tokenizer.texts_to_words('你好！'))
        self.assertEqual(['X', '你', '好', 'X'], tokenizer.texts_to_words('X你好X'))
        self.assertEqual(['Hello', '你', 'WorldOK', '的'], tokenizer.texts_to_words('Hello你WorldOK的'))
        self.assertEqual(['200', '万', '元'], tokenizer.texts_to_words('200万元'))
        self.assertEqual(['#', '你', '好', 'OK', '#'], tokenizer.texts_to_words('#你好OK#'))
        self.assertEqual(['*', 'HELLO', '*'], tokenizer.texts_to_words('*HELLO*'))
        self.assertEqual(['*', 'HELLO', '你', '好', '*'], tokenizer.texts_to_words('*HELLO你好*'))
        self.assertEqual(['HELLO', '*', '你', '好', '*'], tokenizer.texts_to_words('HELLO*你好*'))
        self.assertEqual(['HELLO', '*', '你', '好', '*', 'NICE', 'OK'], tokenizer.texts_to_words('HELLO*你好*NICE OK'))
