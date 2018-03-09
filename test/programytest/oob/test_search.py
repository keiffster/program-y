import unittest
import unittest.mock

from programy.oob.search import SearchOutOfBandProcessor
import xml.etree.ElementTree as ET
from programy.context import ClientContext

from programytest.aiml_tests.client import TestClient

class SearchOutOfBandProcessorTests(unittest.TestCase):

    def setUp(self):
        self._client_context = ClientContext(TestClient(), "testid")
        self._client_context.bot = self._client_context.client.bot
        self._client_context.brain = self._client_context.bot.brain

    def test_processor_xml_parsing(self):
        oob_processor = SearchOutOfBandProcessor()
        self.assertIsNotNone(oob_processor)

        self.assertFalse(oob_processor.parse_oob_xml(None))

        oob = unittest.mock.Mock()
        oob.text = None
        self.assertFalse(oob_processor.parse_oob_xml(oob))

        oob = unittest.mock.Mock()
        oob.text = "Kinghorn"
        self.assertTrue(oob_processor.parse_oob_xml(oob))

    def test_processor(self):
        oob_processor = SearchOutOfBandProcessor()
        self.assertIsNotNone(oob_processor)

        oob_content = ET.fromstring("<search>process</search>")
        self.assertEqual("SEARCH", oob_processor.process_out_of_bounds(self._client_context, oob_content))
