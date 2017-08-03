import unittest

from programy.utils.oob.schedule import ScheduleOutOfBandProcessor
import xml.etree.ElementTree as ET

class ScheduleOutOfBandProcessorTests(unittest.TestCase):

    def test_processor(self):
        oob_processor = ScheduleOutOfBandProcessor()
        self.assertIsNotNone(oob_processor)

        oob_content = ET.fromstring("<schedule><title>Lets meet!</title><description>How about a meeting</description></schedule>")
        self.assertEqual("SCHEDULE", oob_processor.process_out_of_bounds(None, "console", oob_content))
