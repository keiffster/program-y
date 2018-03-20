import unittest
import os

from programy.context import ClientContext
from programy.bot import Bot
from programy.config.bot.bot import BotConfiguration
from programytest.aiml_tests.client import TestClient


class BankBalanceTestsClient(TestClient):

    def __init__(self):
        TestClient.__init__(self, debug=True)

    def load_configuration(self, arguments):
        super(BankBalanceTestsClient, self).load_configuration(arguments)
        self.configuration.client_configuration.configurations[0].configurations[0].files.aiml_files._files=[os.path.dirname(__file__)]


class BankBalanceAIMLTests(unittest.TestCase):

    def setUp (self):
        client = BankBalanceTestsClient()
        self._client_context = client.create_client_context("testid")

    def test_balance(self):
        response = self._client_context.bot.ask_question(self._client_context, "WHAT IS MY BANK BALANCE")
        self.assertIsNotNone(response)
        self.assertEqual(response, 'Your bank balance is currently £0.00.')

