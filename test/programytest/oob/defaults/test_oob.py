import unittest
import xml.etree.ElementTree as ET

from programy.oob.callmom.oob import OutOfBandProcessor
from programytest.client import TestClient


class MockOutOfBandProcessor(OutOfBandProcessor):

    def __init__(self):
        OutOfBandProcessor.__init__(self)

    def parse_oob_xml(self, oob: ET.Element):
        return False


class OutOfBandProcessorTests(unittest.TestCase):

    def setUp(self):
        client = TestClient()
        self._client_context = client.create_client_context("testid")

    def test_processor(self):
        oob_processor = OutOfBandProcessor()
        self.assertIsNotNone(oob_processor)
        self.assertIsNone(oob_processor._xml)

        oob_content = ET.fromstring("<something>process</something>")
        oob_processor.parse_oob_xml(oob_content)
        self.assertIsNotNone(oob_processor._xml)

        self.assertEqual("", oob_processor.execute_oob_command(self._client_context))

        self.assertEqual("", oob_processor.process_out_of_bounds(self._client_context, oob_content))

    def test_failed_xml_parse(self):
        oob_processor = MockOutOfBandProcessor()

        self.assertEqual("", oob_processor.process_out_of_bounds(self._client_context, ""))

