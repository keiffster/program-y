import unittest
import unittest.mock

from programy.oob.dialog import DialogOutOfBandProcessor
import xml.etree.ElementTree as ET

class DialogOutOfBandProcessorTests(unittest.TestCase):

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
        self.assertEqual("DIALOG", oob_processor.process_out_of_bounds(None, "console", oob_content))
