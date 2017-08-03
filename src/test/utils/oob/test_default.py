import unittest

from programy.utils.oob.default import DefaultOutOfBandProcessor
import xml.etree.ElementTree as ET

class DefaultOutOfBandProcessorTests(unittest.TestCase):

    def test_processor(self):
        oob_processor = DefaultOutOfBandProcessor()
        self.assertIsNotNone(oob_processor)

        self.assertEqual("DEFAULT", oob_processor.execute_oob_command(None, "testid"))

        oob_content = ET.fromstring("<something>process</something>")
        self.assertEqual("<?xml version='1.0' encoding='utf8'?>\n<something>process</something>", oob_processor.process_out_of_bounds(None, "testid", oob_content))