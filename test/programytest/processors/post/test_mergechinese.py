import unittest

from programy.processors.post.mergechinese import MergeChinesePostProcessor
from programy.context import ClientContext

from programytest.client import TestClient


class MergeChineseTests(unittest.TestCase):

    def test_merge_chinese(self):
        processor = MergeChinesePostProcessor()

        context = ClientContext(TestClient(), "testid")
        
        result = processor.process(context, "Hello")
        self.assertIsNotNone(result)
        self.assertEqual("Hello", result)

        result = processor.process(context, "Hello World")
        self.assertIsNotNone(result)
        self.assertEqual("Hello World", result)

        result = processor.process(context, "你 好")
        self.assertIsNotNone(result)
        self.assertEqual("你好", result)

        result = processor.process(context, "问 你 好")
        self.assertIsNotNone(result)
        self.assertEqual("问你好", result)

        result = processor.process(context, "XX 你 好")
        self.assertIsNotNone(result)
        self.assertEqual("XX 你好", result)

        result = processor.process(context, "XX 你 好 YY")
        self.assertIsNotNone(result)
        self.assertEqual("XX 你好 YY", result)

