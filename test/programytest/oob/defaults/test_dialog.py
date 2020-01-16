import unittest
import unittest.mock
import xml.etree.ElementTree as ET

from programy.oob.callmom.dialog import DialogOutOfBandProcessor
from programytest.client import TestClient


class DialogOutOfBandProcessorTests(unittest.TestCase):

    def setUp(self):
        client = TestClient()
        self._client_context = client.create_client_context("testid")

    def test_processor_xml_parsing(self):
        oob_processor = DialogOutOfBandProcessor()
        self.assertIsNotNone(oob_processor)

        self.assertFalse(oob_processor.parse_oob_xml(None))

        oob = []
        self.assertFalse(oob_processor.parse_oob_xml(oob))

        oob = []
        oob.append(unittest.mock.Mock())
        oob[0].tag = "title"
        oob[0].text = "title"
        oob.append(unittest.mock.Mock())
        oob[1].tag = "list"
        oob[1].text = "contact1, contact2, contact3"
        self.assertTrue(oob_processor.parse_oob_xml(oob))

    def test_processor(self):
        oob_processor = DialogOutOfBandProcessor()
        self.assertIsNotNone(oob_processor)

        oob_content = ET.fromstring("<dialog><title>Which contact?</title><list>contact1, contact2, contact3</list></dialog>")
        self.assertEqual("DIALOG", oob_processor.process_out_of_bounds(self._client_context, oob_content))

    def test_processor_missing_title(self):
        oob_processor = DialogOutOfBandProcessor()
        self.assertIsNotNone(oob_processor)

        self.assertFalse(oob_processor.parse_oob_xml(None))

        oob = []
        self.assertFalse(oob_processor.parse_oob_xml(oob))

        oob = []
        oob.append(unittest.mock.Mock())
        oob[0].tag = "list"
        oob[0].text = "contact1, contact2, contact3"
        self.assertFalse(oob_processor.parse_oob_xml(oob))

    def test_processor_missing_list(self):
        oob_processor = DialogOutOfBandProcessor()
        self.assertIsNotNone(oob_processor)

        self.assertFalse(oob_processor.parse_oob_xml(None))

        oob = []
        self.assertFalse(oob_processor.parse_oob_xml(oob))

        oob = []
        oob.append(unittest.mock.Mock())
        oob[0].tag = "title"
        oob[0].text = "title"
        self.assertFalse(oob_processor.parse_oob_xml(oob))

    def test_processor_missing_title_and_list(self):
        oob_processor = DialogOutOfBandProcessor()
        self.assertIsNotNone(oob_processor)

        self.assertFalse(oob_processor.parse_oob_xml(None))

        oob = []
        self.assertFalse(oob_processor.parse_oob_xml(oob))

        oob = []
        oob.append(unittest.mock.Mock())
        oob[0].tag = "other"
        oob[0].text = "other"
        self.assertFalse(oob_processor.parse_oob_xml(oob))
