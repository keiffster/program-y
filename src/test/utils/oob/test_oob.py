import unittest

from programy.utils.oob.oob import OutOfBandProcessor
import xml.etree.ElementTree as ET

class OutOfBandProcessorTests(unittest.TestCase):

    def test_processor(self):
        oob_processor = OutOfBandProcessor()
        self.assertIsNotNone(oob_processor)
        self.assertIsNone(oob_processor._xml)

        oob_content = ET.fromstring("<something>process</something>")
        oob_processor.parse_oob_xml(oob_content)
        self.assertIsNotNone(oob_processor._xml)

        self.assertEqual("", oob_processor.execute_oob_command(None, "testid"))

        self.assertEqual("", oob_processor.process_out_of_bounds(None, "testid", oob_content))
