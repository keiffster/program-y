import unittest

from programy.processors.post.multispaces import RemoveMultiSpacePostProcessor
from programy.context import ClientContext

from programytest.client import TestClient

class RemoveMultiSpaceTests(unittest.TestCase):

    def test_remove_multi_spaces(self):
        processor = RemoveMultiSpacePostProcessor()

        context = ClientContext(TestClient(), "testid")
        
        result = processor.process(context, "Hello World")
        self.assertIsNotNone(result)
        self.assertEqual("Hello World", result)

        result = processor.process(context, "Hello World ")
        self.assertIsNotNone(result)
        self.assertEqual("Hello World", result)

        result = processor.process(context, " Hello World")
        self.assertIsNotNone(result)
        self.assertEqual("Hello World", result)

        result = processor.process(context, " Hello  World ")
        self.assertIsNotNone(result)
        self.assertEqual("Hello World", result)
