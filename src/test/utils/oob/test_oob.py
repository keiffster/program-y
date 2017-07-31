import unittest

from programy.utils.oob.oob import OutOfBandProcessor
import xml.etree.ElementTree as ET

class OutOfBandProcessorTests(unittest.TestCase):

    def test_processor(self):
        oob_processor = OutOfBandProcessor()
        self.assertIsNotNone(oob_processor)
        oob_content = ET.fromstring("<something>process</something>")
        self.assertEqual("", oob_processor.process_out_of_bounds(None, "console", oob_content))
