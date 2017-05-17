import unittest

from programy.extensions.energy.usage import EnergyUsageExtension

class EnergyUsageExtensionTests(unittest.TestCase):

    def setUp(self):
        self.bot = None
        self.clientid = "testid"

    def test_usage(self):

        usage = EnergyUsageExtension()
        self.assertIsNotNone(usage)

        result = usage.execute(self.bot, self.clientid, "NOW")
        self.assertIsNotNone(result)
        self.assertEqual("0 0 KWh", result)