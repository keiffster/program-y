import unittest
import unittest.mock
import xml.etree.ElementTree as ET

from programy.oob.callmom.alarm import AlarmOutOfBandProcessor
from programytest.client import TestClient


class AlarmOutOfBandProcessorTests(unittest.TestCase):

    def setUp(self):
        client = TestClient()
        self._client_context = client.create_client_context("testid")

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
        self.assertEqual("ALARM", oob_processor.process_out_of_bounds(self._client_context, oob_content))

    def test_processor_version2(self):
        oob_processor = AlarmOutOfBandProcessor()
        self.assertIsNotNone(oob_processor)

        oob_content = ET.fromstring("<alarm><message>Alert!</message></alarm>")
        self.assertEqual("ALARM", oob_processor.process_out_of_bounds(self._client_context, oob_content))

    def test_missing_hour(self):
        oob_processor = AlarmOutOfBandProcessor()
        self.assertIsNotNone(oob_processor)

        oob = []
        oob.append(unittest.mock.Mock())
        oob[0].tag = "minute"
        oob[0].text = "30"
        self.assertFalse(oob_processor.parse_oob_xml(oob))

    def test_missing_minute(self):
        oob_processor = AlarmOutOfBandProcessor()
        self.assertIsNotNone(oob_processor)

        oob = []
        oob.append(unittest.mock.Mock())
        oob[0].tag = "hour"
        oob[0].text = "11"
        self.assertFalse(oob_processor.parse_oob_xml(oob))

    def test_missing_message(self):
        oob_processor = AlarmOutOfBandProcessor()
        self.assertIsNotNone(oob_processor)

        self.assertFalse(oob_processor.parse_oob_xml(None))

        oob = []
        self.assertFalse(oob_processor.parse_oob_xml(oob))

        oob = []
        oob.append(unittest.mock.Mock())
        self.assertFalse(oob_processor.parse_oob_xml(oob))

    def test_execute_oob_command_no_message(self):
        oob_processor = AlarmOutOfBandProcessor()
        self.assertIsNotNone(oob_processor)

        oob_processor._message = None
        oob_processor._hour = "1"
        oob_processor._min = "30"

        oob_processor.execute_oob_command(self._client_context)

    def test_execute_oob_command_no_message(self):
        oob_processor = AlarmOutOfBandProcessor()
        self.assertIsNotNone(oob_processor)

        oob_processor._message = None
        oob_processor._hour = None
        oob_processor._min = None

        oob_processor.execute_oob_command(self._client_context)
