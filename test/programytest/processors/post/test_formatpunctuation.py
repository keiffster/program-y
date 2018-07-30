import unittest

from programy.processors.post.formatpunctuation import FormatPunctuationProcessor
from programy.context import ClientContext

from programytest.client import TestClient

class FormatNmbersTests(unittest.TestCase):

    def test_format_punctuation(self):
        processor = FormatPunctuationProcessor()

        context = ClientContext(TestClient(), "testid")
        
        result = processor.process(context, 'Hello " World "')
        self.assertIsNotNone(result)
        self.assertEqual('Hello "World"', result)

        result = processor.process(context, '"Hello World"')
        self.assertIsNotNone(result)
        self.assertEqual('"Hello World"', result)

        result = processor.process(context, "' Hello World '")
        self.assertIsNotNone(result)
        self.assertEqual("'Hello World'", result)

        result = processor.process(context, '" Hello World "')
        self.assertIsNotNone(result)
        self.assertEqual('"Hello World"', result)

        result = processor.process(context, '"This" and "That"')
        self.assertIsNotNone(result)
        self.assertEqual('"This" and "That"', result)

        result = processor.process(context, "Hello World .")
        self.assertIsNotNone(result)
        self.assertEqual("Hello World.", result)

        result = processor.process(context, "Hello World ,")
        self.assertIsNotNone(result)
        self.assertEqual("Hello World,", result)

        result = processor.process(context, "Hello World :")
        self.assertIsNotNone(result)
        self.assertEqual("Hello World:", result)

        result = processor.process(context, "Hello World ;")
        self.assertIsNotNone(result)
        self.assertEqual("Hello World;", result)

        result = processor.process(context, "Hello World ?")
        self.assertIsNotNone(result)
        self.assertEqual("Hello World?", result)

        result = processor.process(context, "Hello World !")
        self.assertIsNotNone(result)
        self.assertEqual("Hello World!", result)

        result = processor.process(context, "Hello World . This is it.")
        self.assertIsNotNone(result)
        self.assertEqual("Hello World. This is it.", result)

        result = processor.process(context, "Hello World . 23.45.")
        self.assertIsNotNone(result)
        self.assertEqual("Hello World. 23.45.", result)
