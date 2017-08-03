import unittest

from programy.utils.oob.wifi import WifiOutOfBandProcessor
import xml.etree.ElementTree as ET

class WifiOutOfBandProcessorTests(unittest.TestCase):

    def test_processor_on(self):
        oob_processor = WifiOutOfBandProcessor()
        self.assertIsNotNone(oob_processor)

        oob_content = ET.fromstring("<wifi>on</wifi>")
        self.assertEqual("WIFI", oob_processor.process_out_of_bounds(None, "console", oob_content))

    def test_processor_off(self):
        oob_processor = WifiOutOfBandProcessor()
        self.assertIsNotNone(oob_processor)

        oob_content = ET.fromstring("<wifi>off</wifi>")
        self.assertEqual("WIFI", oob_processor.process_out_of_bounds(None, "console", oob_content))
