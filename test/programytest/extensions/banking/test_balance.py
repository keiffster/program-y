import unittest

from programy.extensions.banking.balance import BankingBalanceExtension

from programytest.client import TestClient

class BankBalanceExtensionTests(unittest.TestCase):

    def setUp(self):
        client = TestClient()
        self.context = client.create_client_context("testid")

    def test_balance(self):

        balance = BankingBalanceExtension()
        self.assertIsNotNone(balance)

        result = balance.execute(self.context, "NOW")
        self.assertIsNotNone(result)
        self.assertEqual("0 00 CREDIT", result)
