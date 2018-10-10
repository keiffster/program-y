import unittest
import unittest.mock

from programy.oob.defaults.sms import SMSOutOfBandProcessor
import xml.etree.ElementTree as ET

from programytest.client import TestClient

class SMSOutOfBandProcessorTests(unittest.TestCase):

    def setUp(self):
        client = TestClient()
        self._client_context = client.create_client_context("testid")

    def test_processor_xml_parsing(self):
        oob_processor = SMSOutOfBandProcessor()
        self.assertIsNotNone(oob_processor)

        self.assertFalse(oob_processor.parse_oob_xml(None))

        oob = []
        self.assertFalse(oob_processor.parse_oob_xml(oob))

        oob = []
        oob.append(unittest.mock.Mock())
        oob[0].tag = "recipient"
        oob[0].text = "077777777"
        oob.append(unittest.mock.Mock())
        oob[1].tag = "message"
        oob[1].text = "Hello!"

        self.assertTrue(oob_processor.parse_oob_xml(oob))

    def test_processor(self):
        oob_processor = SMSOutOfBandProcessor()
        self.assertIsNotNone(oob_processor)

        oob_content = ET.fromstring("<sms><recipient>077777777</recipient><message>Hello!</message></sms>")
        self.assertEqual("SMS", oob_processor.process_out_of_bounds(self._client_context, oob_content))
