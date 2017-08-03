import unittest

from programy.utils.oob.search import SearchOutOfBandProcessor
import xml.etree.ElementTree as ET

class SearchOutOfBandProcessorTests(unittest.TestCase):

    def test_processor(self):
        oob_processor = SearchOutOfBandProcessor()
        self.assertIsNotNone(oob_processor)

        oob_content = ET.fromstring("<search>process</search>")
        self.assertEqual("SEARCH", oob_processor.process_out_of_bounds(None, "console", oob_content))
