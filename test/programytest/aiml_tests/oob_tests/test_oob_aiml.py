import os
import unittest

from programytest.client import TestClient
from programytest.aiml_tests.oob_tests.test_oob import MockDialOutOfBandProcessor


class OOBTestClient(TestClient):

    def __init__(self):
        TestClient.__init__(self)

    def load_storage(self):
        super(OOBTestClient, self).load_storage()
        self.add_default_stores()
        self.add_categories_store([os.path.dirname(__file__)])
        self.add_oobs_store(os.path.dirname(__file__) + os.sep + "test-oobs.conf")


class OOBAIMLTests(unittest.TestCase):

    def setUp(self):
        client = OOBTestClient()
        self._client_context = client.create_client_context("testid")

    def test_oob_one_word(self):
        response = self._client_context.bot.ask_question(self._client_context,  "HELLO")
        self.assertEqual(response, "")

    def test_oob_content(self):
        response = self._client_context.bot.ask_question(self._client_context,  "HI THERE")
        self.assertEqual(response, "")

    def test_oob_xml_and_content(self):
        response = self._client_context.bot.ask_question(self._client_context,  "SAY HELLO")
        self.assertEqual(response, "")

    def test_oob_complex(self):
        response = self._client_context.bot.ask_question(self._client_context,  "FILE BUG REPORT")
        self.assertEqual(response, "To help the developers blah blah blah.")

    def test_embedded_aiml(self):
        response = self._client_context.bot.ask_question(self._client_context,  "DIAL 077777777")
        self.assertEqual(response, "Ok dialing 077777777.")
        self.assertEqual(MockDialOutOfBandProcessor.dialed, "077777777")

    def test_complex_embedded_aiml(self):
        response = self._client_context.bot.ask_question(self._client_context,  "DIAL AGAIN 077777777")
        self.assertEqual(response, "Ok dialing 077777777.")
        self.assertEqual(MockDialOutOfBandProcessor.dialed, "OK I dialled 077777777 but I will dial 077777777 AGAIN")