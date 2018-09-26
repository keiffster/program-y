import unittest
import unittest.mock

import xml.etree.ElementTree as ET

from programy.oob.defaults.dial import DialOutOfBandProcessor

from programytest.client import TestClient

class DialOutOfBandProcessorTests(unittest.TestCase):

    def setUp(self):
        client = TestClient()
        self._client_context = client.create_client_context("testid")

    def test_processor_xml_parsing(self):
        oob_processor = DialOutOfBandProcessor()
        self.assertIsNotNone(oob_processor)

        self.assertFalse(oob_processor.parse_oob_xml(None))

        oob = unittest.mock.Mock()
        oob.text = None
        self.assertFalse(oob_processor.parse_oob_xml(oob))

        oob = unittest.mock.Mock()
        oob.text = "911"
        self.assertTrue(oob_processor.parse_oob_xml(oob))

    def test_processor(self):
        oob_processor = DialOutOfBandProcessor()
        self.assertIsNotNone(oob_processor)

        oob_content = ET.fromstring("<dial>911</dial>")
        self.assertEqual("DIAL", oob_processor.process_out_of_bounds(self._client_context, oob_content))