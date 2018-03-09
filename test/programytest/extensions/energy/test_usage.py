import unittest

from programy.extensions.energy.usage import EnergyUsageExtension
from programy.context import ClientContext

from programytest.aiml_tests.client import TestClient

class EnergyUsageExtensionTests(unittest.TestCase):

    def setUp(self):
        self.context = ClientContext(TestClient(), "testid")

    def test_usage(self):

        usage = EnergyUsageExtension()
        self.assertIsNotNone(usage)

        result = usage.execute(self.context, "NOW")
        self.assertIsNotNone(result)
        self.assertEqual("0 0 KWh", result)