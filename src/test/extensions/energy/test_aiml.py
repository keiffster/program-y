import unittest
import os
from test.aiml_tests.client import TestClient
from programy.config.brain import BrainFileConfiguration


class EnergyUsageTestsClient(TestClient):

    def __init__(self):
        TestClient.__init__(self, debug=True)

    def load_configuration(self, arguments):
        super(EnergyUsageTestsClient, self).load_configuration(arguments)
        self.configuration.brain_configuration._aiml_files = BrainFileConfiguration(files=os.path.dirname(__file__))

class EnergyUsageAIMLTests(unittest.TestCase):

    def setUp (self):
        EnergyUsageAIMLTests.test_client = EnergyUsageTestsClient()

    def test_usage(self):
        response = EnergyUsageAIMLTests.test_client.bot.ask_question("testif", "WHAT IS MY ENERGY USAGE")
        self.assertIsNotNone(response)
        self.assertEqual(response, 'So far this month you have used 0 KWh of Gas and 0 KWh of Electricity.')

