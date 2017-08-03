import unittest

from programy.utils.oob.alarm import AlarmOutOfBandProcessor
import xml.etree.ElementTree as ET

class AlarmOutOfBandProcessorTests(unittest.TestCase):

    def test_processor_version1(self):
        oob_processor = AlarmOutOfBandProcessor()
        self.assertIsNotNone(oob_processor)

        oob_content = ET.fromstring("<alarm><hour>11</hour><minute>30</minute></alarm>")
        self.assertEqual("ALARM", oob_processor.process_out_of_bounds(None, "console", oob_content))

    def test_processor_version2(self):
        oob_processor = AlarmOutOfBandProcessor()
        self.assertIsNotNone(oob_processor)

        oob_content = ET.fromstring("<alarm><message>Alert!</message></alarm>")
        self.assertEqual("ALARM", oob_processor.process_out_of_bounds(None, "console", oob_content))
