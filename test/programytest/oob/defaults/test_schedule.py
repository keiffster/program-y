import unittest
import unittest.mock
import xml.etree.ElementTree as ET

from programy.oob.callmom.schedule import ScheduleOutOfBandProcessor
from programytest.client import TestClient


class ScheduleOutOfBandProcessorTests(unittest.TestCase):

    def setUp(self):
        client = TestClient()
        self._client_context = client.create_client_context("testid")

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
        self.assertEqual("SCHEDULE", oob_processor.process_out_of_bounds(self._client_context, oob_content))

    def test_processor_missing_title(self):
        oob_processor = ScheduleOutOfBandProcessor()
        self.assertIsNotNone(oob_processor)

        self.assertFalse(oob_processor.parse_oob_xml(None))

        oob = []
        self.assertFalse(oob_processor.parse_oob_xml(oob))

        oob = []
        oob.append(unittest.mock.Mock())
        oob[0].tag = "description"
        oob[0].text = "Are you free, my patio needs work"

        self.assertFalse(oob_processor.parse_oob_xml(oob))

    def test_processor_missing_description(self):
        oob_processor = ScheduleOutOfBandProcessor()
        self.assertIsNotNone(oob_processor)

        self.assertFalse(oob_processor.parse_oob_xml(None))

        oob = []
        self.assertFalse(oob_processor.parse_oob_xml(oob))

        oob = []
        oob.append(unittest.mock.Mock())
        oob[0].tag = "title"
        oob[0].text = "Lets meet!"

        self.assertFalse(oob_processor.parse_oob_xml(oob))

    def test_processor_missing_title_and_description(self):
        oob_processor = ScheduleOutOfBandProcessor()
        self.assertIsNotNone(oob_processor)

        self.assertFalse(oob_processor.parse_oob_xml(None))

        oob = []
        self.assertFalse(oob_processor.parse_oob_xml(oob))

        oob = []
        oob.append(unittest.mock.Mock())
        oob[0].tag = "other"
        oob[0].text = "Lets meet!"

        self.assertFalse(oob_processor.parse_oob_xml(oob))


