import unittest
import unittest.mock

from programy.oob.search import SearchOutOfBandProcessor
import xml.etree.ElementTree as ET

class SearchOutOfBandProcessorTests(unittest.TestCase):

    def test_processor_xml_parsing(self):
        oob_processor = SearchOutOfBandProcessor()
        self.assertIsNotNone(oob_processor)

        self.assertFalse(oob_processor.parse_oob_xml(None))

        oob = unittest.mock.Mock()
        oob.text = None
        self.assertFalse(oob_processor.parse_oob_xml(oob))

        oob = unittest.mock.Mock()
        oob.text = "Kinghorn"
        self.assertTrue(oob_processor.parse_oob_xml(oob))

    def test_processor(self):
        oob_processor = SearchOutOfBandProcessor()
        self.assertIsNotNone(oob_processor)

        oob_content = ET.fromstring("<search>process</search>")
        self.assertEqual("SEARCH", oob_processor.process_out_of_bounds(None, "console", oob_content))
