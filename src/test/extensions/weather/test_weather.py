import os
import unittest

from programy.extensions.weather.weather import WeatherExtension
from test.aiml_tests.client import TestClient


class WeatherExtensionTests(unittest.TestCase):

    def setUp(self):
        self.test_client = TestClient()

        latlong     = os.path.dirname(__file__) + "/google_latlong.json"
        observation = os.path.dirname(__file__) + "/observation.json"
        threehourly = os.path.dirname(__file__) + "/forecast_3hourly.json"
        daily       = os.path.dirname(__file__) + "/forecast_daily.json"

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

        result = weather.execute(self.test_client.bot, self.clientid, "LOCATION KY39UR WHEN NOW")
        self.assertIsNotNone(result)

        self.assertEquals("WEATHER Partly cloudy (day) TEMP 12 3 VISIBILITY V 35000 VF Very Good WIND D SW DF South West S 10 PRESSURE P 1017 PT F PTF Falling HUMIDITY 57 3", result)