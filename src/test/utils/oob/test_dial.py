import unittest
import xml.etree.ElementTree as ET

from programy.utils.oob.dial import DialOutOfBoundsProcessor

class DefaultOutOfBoundsProcessorTests(unittest.TestCase):

    def test_processor(self):
        oob_processor = DialOutOfBoundsProcessor()
        self.assertIsNotNone(oob_processor)
        oob_content = ET.fromstring("<dial>911</dial>")
        self.assertEqual("", oob_processor.process_out_of_bounds(None, "console", oob_content))