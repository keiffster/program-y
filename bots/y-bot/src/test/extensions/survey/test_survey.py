import unittest

from extensions.telecoms.minutes import TelecomMinutesExtension

class BankBalanceExtensionTests(unittest.TestCase):

    def test_balance(self):

        minutes = TelecomMinutesExtension()
        self.assertIsNotNone(minutes)

        result = minutes.execute("NOW")
        self.assertIsNotNone(result)
        self.assertEqual("0 0", result)