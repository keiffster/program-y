import unittest
import os
import json

from programy.extensions.weather.weather import WeatherExtension
from programy.utils.weather.metoffice import MetOffice
from programy.utils.geo.google import GoogleMaps

from programytest.client import TestClient


class MockGoogleMaps(GoogleMaps):

    def __init__(self, response_file):
        self._response_file = response_file

    def _get_response_as_json(self, url):
        with open(self._response_file) as response_data:
            return json.load(response_data)


class MockMetOffice(MetOffice):

    def __init__(self, response_file):
        self._response_file = response_file

    def _get_response_as_json(self):
        with open(self._response_file) as response_data:
            return json.load(response_data)

    def get_forecast_data(self, lat, lon, forecast_type):
        return self._get_response_as_json()

    def get_observation_data(self, lat, lon):
        return self._get_response_as_json()


class MockWeatherExtension(WeatherExtension):

    def get_geo_locator(self, bot):
        return MockGoogleMaps(WeathersAIMLTests.maps_file)

    def get_met_office(self, bot):
        return MockMetOffice(WeathersAIMLTests.weather_file)


class WeathersTestsClient(TestClient):

    def __init__(self):
        TestClient.__init__(self, debug=True)

    def load_storage(self):
        super(WeathersTestsClient, self).load_storage()
        self.add_default_stores()
        self.add_categories_store([os.path.dirname(__file__)])


class WeathersAIMLTests(unittest.TestCase):

    maps_file = None
    weather_file = None

    def setUp (self):
        client = WeathersTestsClient()
        self._client_context = client.create_client_context("testid")

    def test_weather(self):
        WeathersAIMLTests.maps_file = os.path.dirname(__file__) + os.sep + "google_latlong.json"
        WeathersAIMLTests.weather_file = os.path.dirname(__file__) + os.sep + "observation.json"
        threehourly = os.path.dirname(__file__) + os.sep + "forecast_3hourly.json"
        daily       = os.path.dirname(__file__) + os.sep + "forecast_daily.json"

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