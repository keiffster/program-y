import unittest
import os

from programy.config.brain.oob import BrainOOBConfiguration

from programytest.client import TestClient

class OOBTestClient(TestClient):

    def __init__(self):
        TestClient.__init__(self)

    def load_storage(self):
        super(OOBTestClient, self).load_storage()
        self.add_default_stores()
        self.add_categories_store([os.path.dirname(__file__)])

    def load_configuration(self, arguments):
        super(OOBTestClient, self).load_configuration(arguments)
        default = BrainOOBConfiguration("default")
        default._classname = "programy.oob.defaults.default.DefaultOutOfBandProcessor"
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
        self.assertEqual(response, "To help the developers blah blah blah.")
