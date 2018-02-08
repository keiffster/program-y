import unittest
import os
import json

from programy.extensions.weather.weather import WeatherExtension
from programytest.aiml_tests.client import TestClient
from programy.utils.weather.metoffice import MetOffice
from programy.utils.geo.google import GoogleMaps

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

    maps_file = None
    weather_file = None

    def get_geo_locator(self, bot):
        return MockGoogleMaps(MockWeatherExtension.maps_file)

    def get_met_office(self, bot):
        return MockMetOffice(MockWeatherExtension.weather_file)


class WeathersTestsClient(TestClient):

    def __init__(self):
        TestClient.__init__(self, debug=True)

    def load_configuration(self, arguments):
        super(WeathersTestsClient, self).load_configuration(arguments)
        self.configuration.brain_configuration.files.aiml_files._files=[os.path.dirname(__file__)]


class WeathersAIMLTests(unittest.TestCase):


    def setUp (self):
        WeathersAIMLTests.test_client = WeathersTestsClient()
        WeathersAIMLTests.test_client.bot.get_conversation("testid").properties["active"] = "true"

    def test_weather(self):
        MockWeatherExtension.maps_file = os.path.dirname(__file__) + os.sep + "google_latlong.json"
        MockWeatherExtension.weather_file = os.path.dirname(__file__) + os.sep + "observation.json"
        threehourly = os.path.dirname(__file__) + os.sep + "forecast_3hourly.json"
        daily       = os.path.dirname(__file__) + os.sep + "forecast_daily.json"

        response = WeathersAIMLTests.test_client.bot.ask_question("testid", "WEATHER LOCATION KY39UR WHEN TODAY")
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