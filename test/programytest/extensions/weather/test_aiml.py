import unittest
import os
from programytest.aiml_tests.client import TestClient


class WeathersTestsClient(TestClient):

    def __init__(self):
        TestClient.__init__(self, debug=True)

    def load_configuration(self, arguments):
        super(WeathersTestsClient, self).load_configuration(arguments)
        self.configuration.brain_configuration.files.aiml_files._files=[os.path.dirname(__file__)]


class WeathersAIMLTests(unittest.TestCase):

    def setUp (self):
        WeathersAIMLTests.test_client = WeathersTestsClient()
        WeathersAIMLTests.test_client.bot.license_keys.load_license_key_data("""
        METOFFICE_API_KEY=TESTKEY
        """)

    def test_weather(self):
        latlong     = os.path.dirname(__file__) + os.sep + "google_latlong.json"
        observation = os.path.dirname(__file__) + os.sep + "observation.json"
        threehourly = os.path.dirname(__file__) + os.sep + "forecast_3hourly.json"
        daily       = os.path.dirname(__file__) + os.sep + "forecast_daily.json"

        response = WeathersAIMLTests.test_client.bot.ask_question("testid", "WEATHER LOCATION KY39UR WHEN TODAY")
        self.assertIsNotNone(response)
        self.assertEqual(response, "Today the weather is Partly cloudy (day) , with a temperature of 12 dot 3 \'C")

