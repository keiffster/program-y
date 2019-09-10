import unittest
import os

from programy.processors.post.consoleformat import ConsoleFormatPostProcessor
from programy.context import ClientContext

from programytest.client import TestClient


class RemoveHTMLTests(unittest.TestCase):

    def test_format_console(self):
        processor = ConsoleFormatPostProcessor()

        context = ClientContext(TestClient(), "testid")
        result = processor.process(context, "Hello World")
        self.assertIsNotNone(result)
        self.assertEqual("Hello World", result)

        result = processor.process(context, "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Rationis enim perfectio est virtus; Sed quid attinet de rebus tam apertis plura requirere?")
        self.assertIsNotNone(result)
        if os.name == 'posix':
            self.assertEqual(
                "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Rationis enim perfectio\nest virtus; Sed quid attinet de rebus tam apertis plura requirere?",
                result)
        elif os.name == 'nt':
            self.assertEqual(
                "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Rationis enim perfectio\r\nest virtus; Sed quid attinet de rebus tam apertis plura requirere?",
                result)
        else:
            raise Exception("Unknown os [%s]"%os.name)

