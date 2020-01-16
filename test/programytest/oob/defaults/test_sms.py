import unittest
import unittest.mock
import xml.etree.ElementTree as ET

from programy.oob.callmom.sms import SMSOutOfBandProcessor
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

    def test_processor_none(self):
        oob_processor = SMSOutOfBandProcessor()
        self.assertIsNotNone(oob_processor)

        self.assertFalse(oob_processor.parse_oob_xml(None))

    def test_processor_missing_no_oob(self):
        oob_processor = SMSOutOfBandProcessor()
        self.assertIsNotNone(oob_processor)

        self.assertFalse(oob_processor.parse_oob_xml(ET.fromstring("<oob></oob>")))

    def test_processor_missing_recipient(self):
        oob_processor = SMSOutOfBandProcessor()
        self.assertIsNotNone(oob_processor)

        self.assertFalse(oob_processor.parse_oob_xml(ET.fromstring("<oob><message>Hello</message></oob>")))

    def test_processor_missing_message(self):
        oob_processor = SMSOutOfBandProcessor()
        self.assertIsNotNone(oob_processor)

        self.assertFalse(oob_processor.parse_oob_xml(ET.fromstring("<oob><recipient>07771597630</recipient></oob>")))

    def test_processor_missing_recipient_and_message(self):
        oob_processor = SMSOutOfBandProcessor()
        self.assertIsNotNone(oob_processor)

        self.assertFalse(oob_processor.parse_oob_xml(ET.fromstring("<oob><other>Something</other></oob>")))
