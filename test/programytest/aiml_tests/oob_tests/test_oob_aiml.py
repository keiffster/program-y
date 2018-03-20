import unittest
import os

from programy.context import ClientContext
from programy.config.brain.oob import BrainOOBConfiguration

from programytest.aiml_tests.client import TestClient

class OOBTestClient(TestClient):

    def __init__(self):
        TestClient.__init__(self)

    def load_configuration(self, arguments):
        super(OOBTestClient, self).load_configuration(arguments)
        self.configuration.client_configuration.configurations[0].configurations[0].files.aiml_files._files = [os.path.dirname(__file__)]
        default = BrainOOBConfiguration("default")
        default._classname = "programy.oob.default.DefaultOutOfBandProcessor"
        self.configuration.client_configuration.configurations[0].configurations[0].oob._default = default


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
        self.assertEqual(response, "To help the developers blah blah blah")
