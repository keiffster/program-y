import unittest

from programy.oob.defaults.default import DefaultOutOfBandProcessor
import xml.etree.ElementTree as ET

from programytest.client import TestClient

class DefaultOutOfBandProcessorTests(unittest.TestCase):

    def setUp(self):
        client = TestClient()
        self._client_context = client.create_client_context("testid")

    def test_processor(self):
        oob_processor = DefaultOutOfBandProcessor()
        self.assertIsNotNone(oob_processor)

        self.assertEqual("", oob_processor.execute_oob_command(self._client_context))

        oob_content = ET.fromstring("<something>process</something>")
        self.assertEqual("", oob_processor.process_out_of_bounds(self._client_context, oob_content))