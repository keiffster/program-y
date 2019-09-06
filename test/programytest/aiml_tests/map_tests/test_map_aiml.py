import unittest
import os

from programytest.client import TestClient


class MapAIMLTestClient(TestClient):

    def __init__(self):
        TestClient.__init__(self)

    def load_storage(self):
        super(MapAIMLTestClient, self).load_storage()
        self.add_default_stores()
        self.add_categories_store([os.path.dirname(__file__)])


class MapAIMLTests(unittest.TestCase):

    def setUp(self):
        client = MapAIMLTestClient()
        self._client_context = client.create_client_context("testid")

        self._client_context.brain.properties.load_from_text("""
             default-get:unknown
         """)
        self._client_context.bot.brain.dynamics.add_dynamic_map('romantodec', "programy.dynamic.maps.roman.MapRomanToDecimal", None)
        self._client_context.bot.brain.dynamics.add_dynamic_map('dectoroman', "programy.dynamic.maps.roman.MapDecimalToRoman", None)
        self._client_context.bot.brain.dynamics.add_dynamic_map('stemmer', "programy.dynamic.maps.stemmer.StemmerMap", None)
        self._client_context.bot.brain.dynamics.add_dynamic_map('lemmatize', "programy.dynamic.maps.lemmatize.LemmatizeMap", None)
        self._client_context.bot.brain.maps.add_map("testmap", {"1": "One", "2": "Two", "3": "Three"}, "file")

    def test_static_map(self):
        response = self._client_context.bot.ask_question(self._client_context,  "STATIC MAP TEST")
        self.assertEqual(response, "One.")

    def test_plural_map(self):
        response = self._client_context.bot.ask_question(self._client_context,  "PLURAL MAP TEST")
        self.assertEqual(response, "TWOS.")

    def test_singular_map(self):
        response = self._client_context.bot.ask_question(self._client_context,  "SINGULAR MAP TEST")
        self.assertEqual(response, "TWO.")

    def test_successor_map(self):
        response = self._client_context.bot.ask_question(self._client_context,  "SUCCESSOR MAP TEST")
        self.assertEqual(response, "667.")

    def test_predessor_map(self):
        response = self._client_context.bot.ask_question(self._client_context,  "PREDECESSOR MAP TEST")
        self.assertEqual(response, "666.")

    def test_dynamic_map_decimal(self):
        response = self._client_context.bot.ask_question(self._client_context,  "DYNAMIC MAP DECIMAL TO ROMAN")
        self.assertEqual(response, "20 is XX.")

    def test_dynamic_map_roman(self):
        response = self._client_context.bot.ask_question(self._client_context,  "DYNAMIC MAP ROMAN TO DECIMAL")
        self.assertEqual(response, "XX is 20.")

    def test_dynamic_map_stemmer(self):
        response = self._client_context.bot.ask_question(self._client_context,  "DYNAMIC MAP STEMMER")
        self.assertEqual(response, "Troubled stemmed is troubl.")

    def test_dynamic_map_lemmatize(self):
        response = self._client_context.bot.ask_question(self._client_context,  "DYNAMIC MAP LEMMATIZE")
        self.assertEqual(response, "The singular of octopi is octopus.")
