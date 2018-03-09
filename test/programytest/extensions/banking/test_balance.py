import unittest

from programy.extensions.banking.balance import BankingBalanceExtension

from programy.context import ClientContext

from programytest.aiml_tests.client import TestClient

class BankBalanceExtensionTests(unittest.TestCase):

    def setUp(self):
        self.context = ClientContext(TestClient(), "testid")

    def test_balance(self):

        balance = BankingBalanceExtension()
        self.assertIsNotNone(balance)

        result = balance.execute(self.context, "NOW")
        self.assertIsNotNone(result)
        self.assertEqual("0 00 CREDIT", result)