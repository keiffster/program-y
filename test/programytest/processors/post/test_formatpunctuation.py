import unittest

from programy.context import ClientContext
from programy.processors.post.formatpunctuation import FormatPunctuationProcessor
from programytest.client import TestClient


class FormatNumbersTests(unittest.TestCase):

    def setUp(self):
        self.context = ClientContext(TestClient(), "testid")

    def test_format_punctuation_empty(self):
        processor = FormatPunctuationProcessor()
        result = processor.process(self.context, '')
        self.assertIsNotNone(result)
        self.assertEqual('', result)

    def test_format_punctuation(self):
        processor = FormatPunctuationProcessor()
        result = processor.process(self.context, 'Hello " World "')
        self.assertIsNotNone(result)
        self.assertEqual('Hello "World"', result)

    def test_format_punctuation2(self):
        processor = FormatPunctuationProcessor()
        result = processor.process(self.context, '"Hello World"')
        self.assertIsNotNone(result)
        self.assertEqual('"Hello World"', result)

    def test_format_punctuation3(self):
        processor = FormatPunctuationProcessor()
        result = processor.process(self.context, "' Hello World '")
        self.assertIsNotNone(result)
        self.assertEqual("'Hello World'", result)

    def test_format_punctuation4(self):
        processor = FormatPunctuationProcessor()
        result = processor.process(self.context, '" Hello World "')
        self.assertIsNotNone(result)
        self.assertEqual('"Hello World"', result)

    def test_format_punctuation5(self):
        processor = FormatPunctuationProcessor()
        result = processor.process(self.context, '"This" and "That"')
        self.assertIsNotNone(result)
        self.assertEqual('"This" and "That"', result)

    def test_format_punctuation6(self):
        processor = FormatPunctuationProcessor()
        result = processor.process(self.context, "Hello World .")
        self.assertIsNotNone(result)
        self.assertEqual("Hello World.", result)

    def test_format_punctuation7(self):
        processor = FormatPunctuationProcessor()
        result = processor.process(self.context, "Hello World ,")
        self.assertIsNotNone(result)
        self.assertEqual("Hello World,", result)

    def test_format_punctuation8(self):
        processor = FormatPunctuationProcessor()
        result = processor.process(self.context, "Hello World :")
        self.assertIsNotNone(result)
        self.assertEqual("Hello World:", result)

    def test_format_punctuation9(self):
        processor = FormatPunctuationProcessor()
        result = processor.process(self.context, "Hello World ;")
        self.assertIsNotNone(result)
        self.assertEqual("Hello World;", result)

    def test_format_punctuation10(self):
        processor = FormatPunctuationProcessor()
        result = processor.process(self.context, "Hello World ?")
        self.assertIsNotNone(result)
        self.assertEqual("Hello World?", result)

    def test_format_punctuation11(self):
        processor = FormatPunctuationProcessor()
        result = processor.process(self.context, "Hello World !")
        self.assertIsNotNone(result)
        self.assertEqual("Hello World!", result)

    def test_format_punctuation12(self):
        processor = FormatPunctuationProcessor()
        result = processor.process(self.context, "Hello World . This is it.")
        self.assertIsNotNone(result)
        self.assertEqual("Hello World. This is it.", result)

    def test_format_punctuation13(self):
        processor = FormatPunctuationProcessor()
        result = processor.process(self.context, "Hello World . 23.45.")
        self.assertIsNotNone(result)
        self.assertEqual("Hello World. 23.45.", result)

    def test_format_punctuation14(self):
        processor = FormatPunctuationProcessor()
        result = processor.process(self.context, "Hello World  . Hi .")
        self.assertIsNotNone(result)
        self.assertEqual("Hello World. Hi.", result)
