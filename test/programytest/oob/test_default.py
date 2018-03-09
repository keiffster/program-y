import unittest

from programy.oob.default import DefaultOutOfBandProcessor
import xml.etree.ElementTree as ET
from programy.context import ClientContext

from programytest.aiml_tests.client import TestClient

class DefaultOutOfBandProcessorTests(unittest.TestCase):

    def setUp(self):
        self._client_context = ClientContext(TestClient(), "testid")
        self._client_context.bot = self._client_context.client.bot
        self._client_context.brain = self._client_context.bot.brain

    def test_processor(self):
        oob_processor = DefaultOutOfBandProcessor()
        self.assertIsNotNone(oob_processor)

        self.assertEqual("", oob_processor.execute_oob_command(self._client_context))

        oob_content = ET.fromstring("<something>process</something>")
        self.assertEqual("", oob_processor.process_out_of_bounds(self._client_context, oob_content))