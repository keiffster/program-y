import unittest

from programy.oob.default import DefaultOutOfBandProcessor
import xml.etree.ElementTree as ET

class DefaultOutOfBandProcessorTests(unittest.TestCase):

    def test_processor(self):
        oob_processor = DefaultOutOfBandProcessor()
        self.assertIsNotNone(oob_processor)

        self.assertEqual("", oob_processor.execute_oob_command(None, "testid"))

        oob_content = ET.fromstring("<something>process</something>")
        self.assertEqual("", oob_processor.process_out_of_bounds(None, "testid", oob_content))