import unittest
import unittest.mock

from programy.oob.email import EmailOutOfBandProcessor
import xml.etree.ElementTree as ET
from programy.context import ClientContext

from programytest.aiml_tests.client import TestClient

class EmailOutOfBandProcessorTests(unittest.TestCase):

    def setUp(self):
        self._client_context = ClientContext(TestClient(), "testid")
        self._client_context.bot = self._client_context.client.bot
        self._client_context.brain = self._client_context.bot.brain

    def test_processor_xml_parsing(self):
        oob_processor = EmailOutOfBandProcessor()
        self.assertIsNotNone(oob_processor)

        self.assertFalse(oob_processor.parse_oob_xml(None))

        oob = []
        self.assertFalse(oob_processor.parse_oob_xml(oob))

        oob = []
        oob.append(unittest.mock.Mock())
        oob[0].tag = "to"
        oob[0].text = "fred@west.com"
        oob.append(unittest.mock.Mock())
        oob[1].tag = "subject"
        oob[1].text = "Hello!"
        oob.append(unittest.mock.Mock())
        oob[2].tag = "body"
        oob[2].text = "Got any cement?"
        self.assertTrue(oob_processor.parse_oob_xml(oob))

    def test_email_processor_invalid(self):
        oob_processor = EmailOutOfBandProcessor()
        self.assertIsNotNone(oob_processor)

        oob_content = ET.fromstring("<email>process</email>")
        self.assertFalse(oob_processor.parse_oob_xml(oob_content))

    def test_email_processor_valid(self):
        oob_processor = EmailOutOfBandProcessor()
        self.assertIsNotNone(oob_processor)

        oob_content = ET.fromstring("<email><to>me@me.com</to><subject>test</subject><body>test body</body></email>")
        self.assertEqual("EMAIL", oob_processor.process_out_of_bounds(self._client_context, oob_content))