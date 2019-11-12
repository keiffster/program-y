import json
import os
import unittest

from programy.extensions.maps.maps import GoogleMapsExtension
from programy.utils.geo.google import GoogleMaps
from programytest.client import TestClient
from programytest.extensions.maps.payloads import directions_payload
from programytest.extensions.maps.payloads import distance_payload


class MockGoogleMaps(GoogleMaps):

    response = None

    def _get_response_as_json(self, url):
        return MockGoogleMaps.response


class MockGoogleMapsExtension(GoogleMapsExtension):

    def get_geo_locator(self):
        return MockGoogleMaps()


class MapsTestsClient(TestClient):

    def __init__(self):
        TestClient.__init__(self, debug=True)

    def load_storage(self):
        super(MapsTestsClient, self).load_storage()
        self.add_default_stores()
        self.add_categories_store([os.path.dirname(__file__)])


class MapsAIMLTests(unittest.TestCase):

    def setUp (self):
        client = MapsTestsClient()
        self._client_context = client.create_client_context("testid")

    def test_distance(self):
        MockGoogleMaps.response = distance_payload

        response = self._client_context.bot.ask_question(self._client_context, "DISTANCE EDINBURGH KINGHORN")
        self.assertIsNotNone(response)
        self.assertEqual(response, 'It is 25 . 1 miles.')

    def test_directions(self):
        MockGoogleMaps.response = directions_payload

        response = self._client_context.bot.ask_question(self._client_context, "DIRECTIONS EDINBURGH KINGHORN")
        self.assertIsNotNone(response)
        self.assertTrue(response.startswith("To get there Head west on Leith St"))
