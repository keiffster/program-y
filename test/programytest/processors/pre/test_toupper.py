import unittest
from programy.processors.pre.toupper import ToUpperPreProcessor
from programy.context import ClientContext

from programytest.client import TestClient


class ToUpperTests(unittest.TestCase):

    def test_to_upper(self):
        processor = ToUpperPreProcessor()

        context = ClientContext(TestClient(), "testid")

        result = processor.process(context, "Hello")
        self.assertIsNotNone(result)
        self.assertEqual("HELLO", result)
