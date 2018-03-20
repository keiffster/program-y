import unittest
import os

from programy.context import ClientContext

from programytest.aiml_tests.client import TestClient


class MapAIMLTestClient(TestClient):

    def __init__(self):
        TestClient.__init__(self)

    def load_configuration(self, arguments):
        super(MapAIMLTestClient, self).load_configuration(arguments)
        self.configuration.client_configuration.configurations[0].configurations[0].files.aiml_files._files = [os.path.dirname(__file__)]


class MapAIMLTests(unittest.TestCase):

    def setUp(self):
        client = MapAIMLTestClient()
        self._client_context = client.create_client_context("testid")

        self._client_context.brain.properties.load_from_text("""
             default-get:unknown
         """)
        self._client_context.bot.brain.dynamics.add_dynamic_map('romantodec', "programy.dynamic.maps.roman.MapRomanToDecimal", None)
        self._client_context.bot.brain.dynamics.add_dynamic_map('dectoroman', "programy.dynamic.maps.roman.MapDecimalToRoman", None)
        self._client_context.bot.brain.maps.add_map("testmap", {"1": "One", "2": "Two", "3": "Three"})

    def test_static_map(self):
        response = self._client_context.bot.ask_question(self._client_context,  "STATIC MAP TEST")
        self.assertEqual(response, "One")

    def test_plural_map(self):
        response = self._client_context.bot.ask_question(self._client_context,  "PLURAL MAP TEST")
        self.assertEqual(response, "TWOS")

    def test_singular_map(self):
        response = self._client_context.bot.ask_question(self._client_context,  "SINGULAR MAP TEST")
        self.assertEqual(response, "TWO")

    def test_successor_map(self):
        response = self._client_context.bot.ask_question(self._client_context,  "SUCCESSOR MAP TEST")
        self.assertEqual(response, "667")

    def test_predessor_map(self):
        response = self._client_context.bot.ask_question(self._client_context,  "PREDECESSOR MAP TEST")
        self.assertEqual(response, "666")

    def test_dynamic_map(self):
        response = self._client_context.bot.ask_question(self._client_context,  "DYNAMIC MAP DECIMAL TO ROMAN")
        self.assertEqual(response, "20 is XX")

        response = self._client_context.bot.ask_question(self._client_context,  "DYNAMIC MAP ROMAN TO DECIMAL")
        self.assertEqual(response, "XX is 20")
