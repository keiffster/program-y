import unittest
import os
from test.aiml_tests.client import TestClient
from programy.config.brain import BrainFileConfiguration

class WeathersTestsClient(TestClient):

    def __init__(self):
        TestClient.__init__(self, debug=True)

    def load_configuration(self, arguments):
        super(WeathersTestsClient, self).load_configuration(arguments)
        self.configuration.brain_configuration._aiml_files = BrainFileConfiguration(os.path.dirname(__file__)+"/../../../../aiml/extensions/weather", ".aiml", False)

class WeathersAIMLTests(unittest.TestCase):

    def setUp (self):

        WeathersAIMLTests.test_client = WeathersTestsClient()

        observation = os.path.dirname(__file__) + "/observation.json"
        threehourly = os.path.dirname(__file__) + "/forecast_3hourly.json"
        daily       = os.path.dirname(__file__) + "/forecast_daily.json"

        WeathersAIMLTests.test_client.bot.brain.license_keys.load_license_key_data("""
        METOFFICE_API_KEY=TESTKEY
        CURRENT_OBSERVATION_RESPONSE_FILE=%s
        THREE_HOURLY_FORECAST_RESPONSE_FILE=%s
        DAILY_FORECAST_RESPONSE_FILE=%s
        """%(observation, threehourly, daily))

    def test_weather(self):
        response = WeathersAIMLTests.test_client.bot.ask_question("testid", "WEATHER POSTCODE KY39UR WHEN TODAY")
        self.assertIsNotNone(response)
        self.assertEqual(response, "Today the weather is Partly cloudy (day) , with a temperature of 12 . 3 \'C Partly cloudy (day)")

