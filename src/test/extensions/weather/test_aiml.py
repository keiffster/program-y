import unittest
import os
from test.aiml_tests.client import TestClient
from programy.config.brain import BrainFileConfiguration

class WeathersTestsClient(TestClient):

    def __init__(self):
        TestClient.__init__(self, debug=True)

    def load_configuration(self, arguments):
        super(WeathersTestsClient, self).load_configuration(arguments)
        self.configuration.brain_configuration._aiml_files = BrainFileConfiguration(files=os.path.dirname(__file__))

class WeathersAIMLTests(unittest.TestCase):

    def setUp (self):

        WeathersAIMLTests.test_client = WeathersTestsClient()

        latlong     = os.path.dirname(__file__) + "/google_latlong.json"
        observation = os.path.dirname(__file__) + "/observation.json"
        threehourly = os.path.dirname(__file__) + "/forecast_3hourly.json"
        daily       = os.path.dirname(__file__) + "/forecast_daily.json"

        WeathersAIMLTests.test_client.bot.license_keys.load_license_key_data("""
        GOOGLE_LATLONG=%s
        METOFFICE_API_KEY=TESTKEY
        CURRENT_OBSERVATION_RESPONSE_FILE=%s
        THREE_HOURLY_FORECAST_RESPONSE_FILE=%s
        DAILY_FORECAST_RESPONSE_FILE=%s
        """%(latlong, observation, threehourly, daily))

    def test_weather(self):
        response = WeathersAIMLTests.test_client.bot.ask_question("testid", "WEATHER LOCATION KY39UR WHEN TODAY")
        self.assertIsNotNone(response)
        self.assertEqual(response, "Today the weather is Partly cloudy (day) , with a temperature of 12 dot 3 \'C")

