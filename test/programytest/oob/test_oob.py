import unittest

from programy.oob.oob import OutOfBandProcessor
import xml.etree.ElementTree as ET
from programy.context import ClientContext

from programytest.aiml_tests.client import TestClient

class OutOfBandProcessorTests(unittest.TestCase):

    def setUp(self):
        self._client_context = ClientContext(TestClient(), "testid")
        self._client_context.bot = self._client_context.client.bot
        self._client_context.brain = self._client_context.bot.brain

    def test_processor(self):
        oob_processor = OutOfBandProcessor()
        self.assertIsNotNone(oob_processor)
        self.assertIsNone(oob_processor._xml)

        oob_content = ET.fromstring("<something>process</something>")
        oob_processor.parse_oob_xml(oob_content)
        self.assertIsNotNone(oob_processor._xml)

        self.assertEqual("", oob_processor.execute_oob_command(self._client_context))

        self.assertEqual("", oob_processor.process_out_of_bounds(self._client_context, oob_content))
