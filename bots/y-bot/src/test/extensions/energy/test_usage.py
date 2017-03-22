import unittest

from extensions.energy.usage import EnergyUsageExtension

class EnergyUsageExtensionTests(unittest.TestCase):

    def test_usage(self):

        usage = EnergyUsageExtension()
        self.assertIsNotNone(usage)

        result = usage.execute("NOW")
        self.assertIsNotNone(result)
        self.assertEqual("0 0 KWh", result)