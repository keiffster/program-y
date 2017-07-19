import unittest

from programy.utils.oob.default import DefaultOutOfBoundsProcessor
import xml.etree.ElementTree as ET

class DefaultOutOfBoundsProcessorTests(unittest.TestCase):

    def test_processor(self):
        oob_processor = DefaultOutOfBoundsProcessor()
        self.assertIsNotNone(oob_processor)
        oob_content = ET.fromstring("<something>process</something>")
        self.assertEqual("", oob_processor.process_out_of_bounds(None, "console", oob_content))