import unittest

from programy.utils.oob.clear import ClearOutOfBandProcessor
import xml.etree.ElementTree as ET

class ClearOutOfBandProcessorTests(unittest.TestCase):

    def test_processor(self):
        oob_processor = ClearOutOfBandProcessor()
        self.assertIsNotNone(oob_processor)

        oob_content = ET.fromstring("<clear>logs</clear>")
        self.assertEqual("CLEAR", oob_processor.process_out_of_bounds(None, "console", oob_content))
