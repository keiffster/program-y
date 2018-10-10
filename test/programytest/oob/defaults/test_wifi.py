import unittest
import unittest.mock

from programy.oob.defaults.wifi import WifiOutOfBandProcessor
import xml.etree.ElementTree as ET

from programytest.client import TestClient

class WifiOutOfBandProcessorTests(unittest.TestCase):

    def setUp(self):
        client = TestClient()
        self._client_context = client.create_client_context("testid")

    def test_processor_xml_parsing(self):
        oob_processor = WifiOutOfBandProcessor()
        self.assertIsNotNone(oob_processor)

        self.assertFalse(oob_processor.parse_oob_xml(None))

        oob = unittest.mock.Mock()
        oob.text = None
        self.assertFalse(oob_processor.parse_oob_xml(oob))

        oob = unittest.mock.Mock()
        oob.text = "on"
        self.assertTrue(oob_processor.parse_oob_xml(oob))

    def test_processor_on(self):
        oob_processor = WifiOutOfBandProcessor()
        self.assertIsNotNone(oob_processor)

        oob_content = ET.fromstring("<wifi>on</wifi>")
        self.assertEqual("WIFI", oob_processor.process_out_of_bounds(self._client_context, oob_content))

    def test_processor_off(self):
        oob_processor = WifiOutOfBandProcessor()
        self.assertIsNotNone(oob_processor)

        oob_content = ET.fromstring("<wifi>off</wifi>")
        self.assertEqual("WIFI", oob_processor.process_out_of_bounds(self._client_context, oob_content))
