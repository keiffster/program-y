import os
import unittest

from programy.extensions.weather.weather import WeatherExtension
from programytest.aiml_tests.client import TestClient


class WeatherExtensionTests(unittest.TestCase):

    def setUp(self):
        self.test_client = TestClient()

        latlong     = os.path.dirname(__file__) + os.sep + "google_latlong.json"
        observation = os.path.dirname(__file__) + os.sep + "observation.json"
        threehourly = os.path.dirname(__file__) + os.sep + "forecast_3hourly.json"
        daily       = os.path.dirname(__file__) + os.sep + "forecast_daily.json"

        self.test_client.bot.license_keys.load_license_key_data("""
        GOOGLE_LATLONG=%s
        METOFFICE_API_KEY=TESTKEY
        CURRENT_OBSERVATION_RESPONSE_FILE=%s
        THREE_HOURLY_FORECAST_RESPONSE_FILE=%s
        DAILY_FORECAST_RESPONSE_FILE=%s
        """%(latlong, observation, threehourly, daily))
        self.clientid = "testid"

    def test_observation(self):

        weather = WeatherExtension()
        self.assertIsNotNone(weather)

        result = weather.execute(self.test_client.bot, self.clientid, "OBSERVATION LOCATION KY39UR WHEN NOW")
        self.assertIsNotNone(result)
        self.assertEquals("WEATHER Partly cloudy (day) TEMP 12 3 VISIBILITY V 35000 VF Very Good WIND D SW DF South West S 10 PRESSURE P 1017 PT F PTF Falling HUMIDITY 57 3", result)

        result = weather.execute(self.test_client.bot, self.clientid, "OBSERVATION OTHER KY39UR WHEN NOW")
        self.assertIsNone(result)

        result = weather.execute(self.test_client.bot, self.clientid, "OBSERVATION LOCATION KY39UR OTHER NOW")
        self.assertIsNone(result)

        result = weather.execute(self.test_client.bot, self.clientid, "")
        self.assertIsNone(result)

    def test_forecast3(self):

        weather = WeatherExtension()
        self.assertIsNotNone(weather)

        result = weather.execute(self.test_client.bot, self.clientid, "FORECAST3 LOCATION KY39UR WHEN NOW")
        self.assertIsNotNone(result)
        self.assertEquals("WEATHER Overcast TEMP 10 FEELS 10 WINDDIR NW WINDDIRFULL North West WINDSPEED 4 VIS Very good - Between 20-40 km UVINDEX 0 UVGUIDE None RAINPROB 8 HUMIDITY 73", result)

    def test_forecast24(self):

        weather = WeatherExtension()
        self.assertIsNotNone(weather)

        result = weather.execute(self.test_client.bot, self.clientid, "FORECAST24 LOCATION KY39UR WHEN NOW")
        self.assertIsNotNone(result)
        self.assertEquals("WEATHER TYPE Cloudy WINDDIR NW WINDGUST 7 WINDSPEED 4 TEMP 8 FEELS 8 HUMID 76 RAINPROB 8 VISTEXT Very good - Between 20-40 km WEATHER Cloudy", result)
