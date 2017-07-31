import unittest

from programy.utils.oob.default import DefaultOutOfBandProcessor
import xml.etree.ElementTree as ET

class DefaultOutOfBandProcessorTests(unittest.TestCase):

    def test_processor(self):
        oob_processor = DefaultOutOfBandProcessor()
        self.assertIsNotNone(oob_processor)
        oob_content = ET.fromstring("<something>process</something>")
        self.assertEqual("", oob_processor.process_out_of_bounds(None, "console", oob_content))