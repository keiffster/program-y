import unittest
import os

from programy.processors.post.removehtml import RemoveHTMLPostProcessor
from programy.context import ClientContext

from programytest.client import TestClient

class RemoveHTMLTests(unittest.TestCase):

    def test_remove_html(self):
        processor = RemoveHTMLPostProcessor()

        context = ClientContext(TestClient(), "testid")

        result = processor.process(context, "Hello World")
        self.assertIsNotNone(result)
        self.assertEqual("Hello World", result)

        result = processor.process(context, "Hello <br/> World")
        self.assertIsNotNone(result)
        if os.name == 'posix':
            self.assertEqual("Hello\nWorld", result)
        elif os.name == 'nt':
            self.assertEqual("Hello\r\nWorld", result)
        else:
            raise Exception("Unknown os [%s]"%os.name)

        result = processor.process(context, "Hello <br /> World")
        self.assertIsNotNone(result)
        if os.name == 'posix':
            self.assertEqual("Hello\nWorld", result)
        elif os.name == 'nt':
            self.assertEqual("Hello\r\nWorld", result)
        else:
            raise Exception("Unknown os [%s]"%os.name)
