import os
import unittest
import json
import unittest.mock

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

    def __init__(self, maps_file, weather_file):
        self._maps_file = maps_file
        self._weather_file = weather_file

    def get_geo_locator(self, bot):
        return MockGoogleMaps(self._maps_file)

    def get_met_office(self, bot):
        return MockMetOffice(self._weather_file)


class WeatherExtensionTests(unittest.TestCase):

    def setUp(self):
        client = TestClient()
        client.add_license_keys_store()
        self.context = client.create_client_context("testid")

        bot = unittest.mock.Mock()
        self.context.bot = bot
        self.context.brain = bot.brain


    def test_observation(self):
        latlong     = os.path.dirname(__file__) + os.sep + "google_latlong.json"
        observation = os.path.dirname(__file__) + os.sep + "observation.json"

        weather = MockWeatherExtension(latlong, observation)
        self.assertIsNotNone(weather)

        result = weather.execute(self.context, "OBSERVATION LOCATION KY39UR WHEN NOW")
        self.assertIsNotNone(result)
        self.assertEqual("WEATHER Partly cloudy (day) TEMP 12 3 VISIBILITY V 35000 VF Very Good WIND D SW DF South West S 10 PRESSURE P 1017 PT F PTF Falling HUMIDITY 57 3", result)

        result = weather.execute(self.context, "OBSERVATION OTHER KY39UR WHEN NOW")
        self.assertIsNone(result)

        result = weather.execute(self.context, "OBSERVATION LOCATION KY39UR OTHER NOW")
        self.assertIsNone(result)

        result = weather.execute(self.context, "")
        self.assertIsNone(result)

    def test_forecast5day(self):
        latlong     = os.path.dirname(__file__) + os.sep + "google_latlong.json"
        forecast       = os.path.dirname(__file__) + os.sep + "forecast_daily.json"

        weather = MockWeatherExtension(latlong, forecast)
        self.assertIsNotNone(weather)

        result = weather.execute(self.context, "FORECAST5DAY LOCATION KY39UR WHEN 1")
        self.assertIsNotNone(result)
        self.assertEqual("WEATHER TYPE Cloudy WINDDIR NW WINDGUST 7 WINDSPEED 4 TEMP 8 FEELS 8 HUMID 76 RAINPROB 8 VISTEXT Very good - Between 20-40 km WEATHER Cloudy", result)

    def test_forecast24hour(self):
        latlong     = os.path.dirname(__file__) + os.sep + "google_latlong.json"
        forecast = os.path.dirname(__file__) + os.sep + "forecast_3hourly.json"

        weather = MockWeatherExtension(latlong, forecast)
        self.assertIsNotNone(weather)

        result = weather.execute(self.context, "FORECAST24HOUR LOCATION KY39UR WHEN 1")
        self.assertIsNotNone(result)
        self.assertEqual("WEATHER Overcast TEMP 10 FEELS 10 WINDDIR NW WINDDIRFULL North West WINDSPEED 4 VIS Very good - Between 20-40 km UVINDEX 0 UVGUIDE None RAINPROB 8 HUMIDITY 73", result)
