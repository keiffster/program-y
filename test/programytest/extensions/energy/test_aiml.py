import unittest
import os

from programytest.client import TestClient


class EnergyUsageTestsClient(TestClient):

    def __init__(self):
        TestClient.__init__(self, debug=True)

    def load_storage(self):
        super(EnergyUsageTestsClient, self).load_storage()
        self.add_default_stores()
        self.add_categories_store([os.path.dirname(__file__)])


class EnergyUsageAIMLTests(unittest.TestCase):

    def setUp (self):
        client = EnergyUsageTestsClient()
        self._client_context = client.create_client_context("testid")

    def test_usage(self):
        response =  self._client_context.bot.ask_question(self._client_context, "WHAT IS MY ENERGY USAGE")
        self.assertIsNotNone(response)
        self.assertEqual(response, 'So far this month you have used 0 KWh of Gas and 0 KWh of Electricity.')

