import unittest

from programy.utils.oob.oob import OutOfBoundsProcessor
import xml.etree.ElementTree as ET

class OutOfBoundsProcessorTests(unittest.TestCase):

    def test_processor(self):
        oob_processor = OutOfBoundsProcessor()
        self.assertIsNotNone(oob_processor)
        oob_content = ET.fromstring("<something>process</something>")
        self.assertEqual("", oob_processor.process_out_of_bounds(None, "console", oob_content))
