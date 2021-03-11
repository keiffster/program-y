import os
import unittest

from programy.context import ClientContext
from programy.processors.post.removehtml import RemoveHTMLPostProcessor
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

        result = processor.process(context, """ACCUWEATHER TEXTSEARCH LOCATION * <br />
            ACCUWEATHER CONDITIONS LOCATION * <br />
            ACCUWEATHER WEATHER LOCATION *""")
        self.assertIsNotNone(result)
        if os.name == 'posix':
            self.assertEqual("ACCUWEATHER TEXTSEARCH LOCATION *\nACCUWEATHER CONDITIONS LOCATION *\nACCUWEATHER WEATHER LOCATION *", result)
        elif os.name == 'nt':
            self.assertEqual("Hello\r\nWorld", result)
        else:
            raise Exception("Unknown os [%s]"%os.name)
