import unittest
import xml.etree.ElementTree as ET

from programy.utils.oob.dial import DialOutOfBandProcessor

class DialOutOfBandProcessorTests(unittest.TestCase):

    def test_processor(self):
        oob_processor = DialOutOfBandProcessor()
        self.assertIsNotNone(oob_processor)

        oob_content = ET.fromstring("<dial>911</dial>")
        self.assertEqual("DIAL", oob_processor.process_out_of_bounds(None, "console", oob_content))