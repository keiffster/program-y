import unittest
import os
from programy.extensions.weather.weather import WeatherExtension
from programy.utils.geo.google import GoogleMaps
from programy.utils.weather.metoffice import MetOffice
from programytest.client import TestClient
from programytest.extensions.weather.payloads.google_latlong import latlong_payload
from programytest.extensions.weather.payloads.observation import observation_payload


class MockGoogleMaps(GoogleMaps):

    response = None

    def _get_response_as_json(self, url):
        return MockGoogleMaps.response


class MockMetOffice(MetOffice):

    response = None

    def _get_response_as_json(self):
        return MockMetOffice.response

    def get_forecast_data(self, lat, lon, forecast_type):
        return self._get_response_as_json()

    def get_observation_data(self, lat, lon):
        return self._get_response_as_json()


class MockWeatherExtension(WeatherExtension):

    def get_geo_locator(self):
        return MockGoogleMaps()

    def get_met_office(self):
        return MockMetOffice()


class WeathersTestsClient(TestClient):

    def __init__(self):
        TestClient.__init__(self, debug=True)

    def load_storage(self):
        super(WeathersTestsClient, self).load_storage()
        self.add_default_stores()
        self.add_categories_store([os.path.dirname(__file__)])


class WeathersAIMLTests(unittest.TestCase):

    def setUp (self):
        client = WeathersTestsClient()
        self._client_context = client.create_client_context("testid")

    def test_weather(self):
        MockGoogleMaps.response = latlong_payload
        MockMetOffice.response = observation_payload

        response = self._client_context.bot.ask_question(self._client_context, "WEATHER LOCATION KY39UR WHEN TODAY")
        self.assertIsNotNone(response)
        self.assertEqual(response, "According to the UK Met Office, this it is partly cloudy (day) , with a temperature of around 12dot3'C , humidty is 57.3% , with pressure at 1017mb and falling .")

"""
WEATHER IN *
WEATHER LOCATION * WHEN *
FORECAST LOCATION * DAY *
FORECAST LOCATION * TIME *
WILL IT RAIN TODAY IN *
WILL IT RAIN TOMORROW IN *
"""