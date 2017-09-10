import unittest
import unittest.mock

from programy.oob.alarm import AlarmOutOfBandProcessor
import xml.etree.ElementTree as ET

class AlarmOutOfBandProcessorTests(unittest.TestCase):

    def test_processor_xml_parsing(self):
        oob_processor = AlarmOutOfBandProcessor()
        self.assertIsNotNone(oob_processor)

        self.assertFalse(oob_processor.parse_oob_xml(None))

        oob = []
        self.assertFalse(oob_processor.parse_oob_xml(oob))

        oob = []
        oob.append(unittest.mock.Mock())
        oob[0].tag = "hour"
        oob[0].text = "11"
        oob.append(unittest.mock.Mock())
        oob[1].tag = "minute"
        oob[1].text = "30"
        self.assertTrue(oob_processor.parse_oob_xml(oob))

        oob = []
        oob.append(unittest.mock.Mock())
        oob[0].tag = "message"
        oob[0].text = "hello"
        self.assertTrue(oob_processor.parse_oob_xml(oob))

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
