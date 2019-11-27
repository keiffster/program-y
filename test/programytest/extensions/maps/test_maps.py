import unittest
import unittest.mock
from unittest.mock import patch
from programy.extensions.maps.maps import GoogleMapsExtension
from programy.utils.geo.google import GoogleDistance
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


class MapsExtensionTests(unittest.TestCase):

    def setUp(self):
        client = TestClient()
        self.context = client.create_client_context("testid")

    def test_get_geo_locator(self):
        geocode = GoogleMapsExtension()
        self.assertIsInstance(geocode.get_geo_locator(), GoogleMaps)

    def test_maps_invalid(self):
        MockGoogleMaps.response = distance_payload
        googlemaps = MockGoogleMapsExtension()
        self.assertIsNotNone(googlemaps)

        self.assertIsNone(googlemaps.execute(self.context, "DISTANCE"))
        self.assertIsNone(googlemaps.execute(self.context, "DISTANCE TO"))
        self.assertIsNone(googlemaps.execute(self.context, "DISTANCE TO FROM OTHER"))
        self.assertIsNone(googlemaps.execute(self.context, "DIRECTIONS"))
        self.assertIsNone(googlemaps.execute(self.context, "DIRECTIONS TO"))
        self.assertIsNone(googlemaps.execute(self.context, "DIRECTIONS TO FROM OTHER"))
        self.assertIsNone(googlemaps.execute(self.context, "OTHER"))
        self.assertIsNone(googlemaps.execute(self.context, "SOMETHINGELSE EDINBURGH KINGHORN"))

    def test_maps_distance(self):
        MockGoogleMaps.response = distance_payload
        googlemaps = MockGoogleMapsExtension()
        self.assertIsNotNone(googlemaps)

        result = googlemaps.execute(self.context, "DISTANCE EDINBURGH KINGHORN")
        self.assertIsNotNone(result)
        self.assertEqual("DISTANCE DEC 25 FRAC 1 UNITS miles", result)

    def test_format_distance_for_programy(self):
        MockGoogleMaps.response = distance_payload
        googlemaps = MockGoogleMapsExtension()
        self.assertIsNotNone(googlemaps)

        distance = GoogleDistance("here", "there")
        distance._distance_text = "10 miles"
        self.assertEqual("DISTANCE DEC 10 FRAC 0 UNITS miles", googlemaps._format_distance_for_programy(distance))

        distance = GoogleDistance("here", "there")
        distance._distance_text = "22.45 km"
        self.assertEqual("DISTANCE DEC 22 FRAC 45 UNITS km", googlemaps._format_distance_for_programy(distance))

    def test_format_directions_for_programy(self):
        MockGoogleMaps.response = directions_payload
        googlemaps = MockGoogleMapsExtension()
        self.assertIsNotNone(googlemaps)

        directions = unittest.mock.Mock()
        directions.legs_as_a_string = lambda : "Leg As String"
        self.assertEqual("DIRECTIONS Leg As String", googlemaps._format_directions_for_programy(directions))

    def test_format_directions_for_programy_no_directions(self):
        MockGoogleMaps.response = directions_payload
        googlemaps = MockGoogleMapsExtension()
        self.assertIsNotNone(googlemaps)

        self.assertIsNone(googlemaps._format_directions_for_programy(None))

    def test_maps_direction(self):
        global directions
        MockGoogleMaps.response = directions_payload
        googlemaps = MockGoogleMapsExtension()
        self.assertIsNotNone(googlemaps)

        result = googlemaps.execute(self.context, "DIRECTIONS EDINBURGH KINGHORN")
        self.assertIsNotNone(result)
        self.assertTrue(result.startswith("DIRECTIONS Head west on Leith St/A900 toward Leith"))

    def patch_get_distance_between_addresses1(self, from_place, to_place):
        return None

    @patch("programy.utils.geo.google.GoogleMaps.get_distance_between_addresses", patch_get_distance_between_addresses1)
    def test_maps_distance_none(self):
        googlemaps = GoogleMapsExtension()
        self.assertIsNotNone(googlemaps)

        self.assertIsNone(googlemaps.execute(self.context, "DISTANCE EDINBURGH KINGHORN"))

    def patch_get_distance_between_addresses2(self, from_place, to_place):
        raise Exception("Mock Exception")

    @patch("programy.utils.geo.google.GoogleMaps.get_distance_between_addresses", patch_get_distance_between_addresses2)
    def test_maps_distance_exception(self):
        googlemaps = GoogleMapsExtension()
        self.assertIsNotNone(googlemaps)

        self.assertIsNone(googlemaps.execute(self.context, "DISTANCE EDINBURGH KINGHORN"))

    def patch_get_directions_between_addresses1(self, from_place, to_place):
        return None

    @patch("programy.utils.geo.google.GoogleMaps.get_directions_between_addresses", patch_get_directions_between_addresses1)
    def test_maps_direction_none(self):
        googlemaps = GoogleMapsExtension()
        self.assertIsNotNone(googlemaps)

        self.assertIsNone(googlemaps.execute(self.context, "DIRECTIONS EDINBURGH KINGHORN"))

    def patch_get_directions_between_addresses2(self, from_place, to_place):
        raise Exception("Mock Exception")

    @patch("programy.utils.geo.google.GoogleMaps.get_directions_between_addresses", patch_get_directions_between_addresses2)
    def test_maps_direction_exception(self):
        googlemaps = GoogleMapsExtension()
        self.assertIsNotNone(googlemaps)

        self.assertIsNone(googlemaps.execute(self.context, "DIRECTIONS EDINBURGH KINGHORN"))
