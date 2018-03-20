import unittest
import os
import json

from programy.extensions.geocode.geocode import GeoCodeExtension
from programy.utils.geo.google import GoogleMaps
from programy.context import ClientContext

from programytest.aiml_tests.client import TestClient


class MockGoogleMaps(GoogleMaps):

    def __init__(self, data_file_name):
        self._data_file_name = data_file_name

    def _get_response_as_json(self, url):
        with open(self._data_file_name, "r") as data_file:
            return json.load(data_file)


class MockGeoCodeExtension(GeoCodeExtension):

    def get_geo_locator(self):
        return  MockGoogleMaps(GeoCodeAIMLTests.LATLONG)


class GeoCodeTestsClient(TestClient):

    def __init__(self):
        TestClient.__init__(self, debug=True)

    def load_configuration(self, arguments):
        super(GeoCodeTestsClient, self).load_configuration(arguments)
        self.configuration.client_configuration.configurations[0].configurations[0].files.aiml_files._files=[os.path.dirname(__file__)]


class GeoCodeAIMLTests(unittest.TestCase):

    LATLONG = None

    def setUp (self):
        client = GeoCodeTestsClient()
        self._client_context = client.create_client_context("testid")

    def test_postcode1(self):
        GeoCodeAIMLTests.LATLONG = os.path.dirname(__file__) + os.sep + "google_latlong.json"
        self.assertTrue(os.path.exists(GeoCodeAIMLTests.LATLONG))
        response =self._client_context.bot.ask_question(self._client_context, "POSTCODE KY39UR")
        self.assertIsNotNone(response)
        self.assertEqual(response, 'LATITUDE DEC 56 FRAC 0720397 LONGITUDE DEC -3 FRAC 1752001')

    def test_postcode2(self):
        GeoCodeAIMLTests.LATLONG = os.path.dirname(__file__) + os.sep + "google_latlong.json"
        self.assertTrue(os.path.exists(GeoCodeAIMLTests.LATLONG))
        response =self._client_context.bot.ask_question(self._client_context, "POSTCODE KY3 9UR")
        self.assertIsNotNone(response)
        self.assertEqual(response, 'LATITUDE DEC 56 FRAC 0720397 LONGITUDE DEC -3 FRAC 1752001')

    def test_location(self):
        GeoCodeAIMLTests.LATLONG = os.path.dirname(__file__) + os.sep + "google_latlong.json"
        self.assertTrue(os.path.exists(GeoCodeAIMLTests.LATLONG))
        response =self._client_context.bot.ask_question(self._client_context, "LOCATION KINGHORN")
        self.assertIsNotNone(response)
        self.assertEqual(response, 'LATITUDE DEC 56 FRAC 0720397 LONGITUDE DEC -3 FRAC 1752001')
