import os
import unittest
import unittest.mock
from programy.extensions.weather.weather import WeatherExtension
from programy.utils.geo.google import GoogleMaps
from programy.utils.weather.metoffice import MetOffice
from programytest.client import TestClient
from programytest.extensions.weather.payloads.google_latlong import latlong_payload
from programytest.extensions.weather.payloads.observation import observation_payload
from programytest.extensions.weather.payloads.forecast_3hourly import forecast_3hourly_payload
from programytest.extensions.weather.payloads.forecast_daily import forecast_daily_payload


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


class WeatherExtensionTests(unittest.TestCase):

    def setUp(self):
        client = TestClient()
        client.add_license_keys_store()
        self.context = client.create_client_context("testid")

        bot = unittest.mock.Mock()
        self.context.bot = bot
        self.context.brain = bot.brain

    def test_observation(self):
        MockGoogleMaps.response = latlong_payload
        MockMetOffice.response = observation_payload

        weather = MockWeatherExtension()
        self.assertIsNotNone(weather)

        result = weather.execute(self.context, "OBSERVATION LOCATION KY39UR WHEN NOW")
        self.assertIsNotNone(result)
        self.assertEqual("WEATHER Partly cloudy (day) TEMP 12 3 HUMIDITY 57 3 VISIBILITY V 35000 VF Very Good PRESSURE P 1017 PT F PTF Falling WIND D SW DF South West S 10", result)

        result = weather.execute(self.context, "OBSERVATION OTHER KY39UR WHEN NOW")
        self.assertIsNone(result)

        result = weather.execute(self.context, "OBSERVATION LOCATION KY39UR OTHER NOW")
        self.assertIsNone(result)

        result = weather.execute(self.context, "")
        self.assertIsNone(result)

    def test_forecast5day(self):
        MockGoogleMaps.response = latlong_payload
        MockMetOffice.response = forecast_daily_payload

        weather = MockWeatherExtension()
        self.assertIsNotNone(weather)

        result = weather.execute(self.context, "FORECAST5DAY LOCATION KY39UR WHEN 1")
        self.assertIsNotNone(result)
        self.assertEqual("WEATHER TYPE Cloudy WINDDIR NW WINDGUST 7 WINDSPEED 4 TEMP 8 FEELS 8 HUMID 76 RAINPROB 8 VISTEXT Very good - Between 20-40 km WEATHER Cloudy", result)

    def test_forecast24hour(self):
        MockGoogleMaps.response = latlong_payload
        MockMetOffice.response = forecast_3hourly_payload

        weather = MockWeatherExtension()
        self.assertIsNotNone(weather)

        result = weather.execute(self.context, "FORECAST24HOUR LOCATION KY39UR WHEN 1")

        self.assertIsNotNone(result)
        self.assertEqual("WEATHER Overcast TEMP 10 FEELS 10 WINDSPEED 4 UVINDEX 0 UVGUIDE None RAINPROB 8 HUMIDITY 73 WINDDIR NW WINDDIRFULL North West VIS Very good - Between 20-40 km", result)
