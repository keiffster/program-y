import unittest
from programy.processors.pre.splitchinese import SplitChinesePreProcessor
from programy.context import ClientContext

from programytest.client import TestClient


class SplitChineseTests(unittest.TestCase):

    def test_split_chinese(self):
        processor = SplitChinesePreProcessor()

        context = ClientContext(TestClient(), "testid")
        
        result = processor.process(context, "Hello")
        self.assertIsNotNone(result)
        self.assertEqual("Hello", result)

        result = processor.process(context, "Hello World")
        self.assertIsNotNone(result)
        self.assertEqual("Hello World", result)

        result = processor.process(context, "你好")
        self.assertIsNotNone(result)
        self.assertEqual("你 好", result)

        result = processor.process(context, "问你好")
        self.assertIsNotNone(result)
        self.assertEqual("问 你 好", result)

        result = processor.process(context, "XX你好")
        self.assertIsNotNone(result)
        self.assertEqual("XX 你 好", result)

        result = processor.process(context, "XX你好 YY")
        self.assertIsNotNone(result)
        self.assertEqual("XX 你 好 YY", result)

        result = processor.process(context, "XX你好YY")
        self.assertIsNotNone(result)
        self.assertEqual("XX 你 好 YY", result)
