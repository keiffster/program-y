import unittest
import unittest.mock

from programy.oob.schedule import ScheduleOutOfBandProcessor
import xml.etree.ElementTree as ET

class ScheduleOutOfBandProcessorTests(unittest.TestCase):

    def test_processor_xml_parsing(self):
        oob_processor = ScheduleOutOfBandProcessor()
        self.assertIsNotNone(oob_processor)

        self.assertFalse(oob_processor.parse_oob_xml(None))

        oob = []
        self.assertFalse(oob_processor.parse_oob_xml(oob))

        oob = []
        oob.append(unittest.mock.Mock())
        oob[0].tag = "title"
        oob[0].text = "Lets meet!"
        oob.append(unittest.mock.Mock())
        oob[1].tag = "description"
        oob[1].text = "Are you free, my patio needs work"

        self.assertTrue(oob_processor.parse_oob_xml(oob))

    def test_processor(self):
        oob_processor = ScheduleOutOfBandProcessor()
        self.assertIsNotNone(oob_processor)

        oob_content = ET.fromstring("<schedule><title>Lets meet!</title><description>How about a meeting</description></schedule>")
        self.assertEqual("SCHEDULE", oob_processor.process_out_of_bounds(None, "console", oob_content))
