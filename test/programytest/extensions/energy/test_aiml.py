import unittest
import os

from programy.context import ClientContext

from programytest.aiml_tests.client import TestClient


class EnergyUsageTestsClient(TestClient):

    def __init__(self):
        TestClient.__init__(self, debug=True)

    def load_configuration(self, arguments):
        super(EnergyUsageTestsClient, self).load_configuration(arguments)
        self.configuration.client_configuration.configurations[0].configurations[0].files.aiml_files._files=[os.path.dirname(__file__)]


class EnergyUsageAIMLTests(unittest.TestCase):

    def setUp (self):
        client = EnergyUsageTestsClient()
        self._client_context = client.create_client_context("testid")

    def test_usage(self):
        response =  self._client_context.bot.ask_question(self._client_context, "WHAT IS MY ENERGY USAGE")
        self.assertIsNotNone(response)
        self.assertEqual(response, 'So far this month you have used 0 KWh of Gas and 0 KWh of Electricity.')

