import unittest
from programy.processors.post.formatnumbers import FormatNumbersPostProcessor
from programy.context import ClientContext

from programytest.client import TestClient

class FormatNmbersTests(unittest.TestCase):

    def test_format_numbers(self):
        processor = FormatNumbersPostProcessor()

        context = ClientContext(TestClient(), "testid")

        result = processor.process(context, "23")
        self.assertIsNotNone(result)
        self.assertEqual("23", result)

        result = processor.process(context, "23.45")
        self.assertIsNotNone(result)
        self.assertEqual("23.45", result)

        result = processor.process(context, "23. 45")
        self.assertIsNotNone(result)
        self.assertEqual("23.45", result)

        result = processor.process(context, "23 . 45")
        self.assertIsNotNone(result)
        self.assertEqual("23.45", result)

        result = processor.process(context, "23,450")
        self.assertIsNotNone(result)
        self.assertEqual("23,450", result)

        result = processor.process(context, "23, 450")
        self.assertIsNotNone(result)
        self.assertEqual("23,450", result)

        result = processor.process(context, "23, 450, 000")
        self.assertIsNotNone(result)
        self.assertEqual("23,450,000", result)
