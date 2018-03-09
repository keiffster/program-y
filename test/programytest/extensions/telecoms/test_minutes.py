import unittest

from programy.extensions.telecoms.minutes import TelecomMinutesExtension
from programy.context import ClientContext

from programytest.aiml_tests.client import TestClient

class TelecomsMinutesExtensionTests(unittest.TestCase):

    def setUp(self):
        self.context = ClientContext(TestClient(), "testid")

    def test_minutes(self):

        minutes = TelecomMinutesExtension()
        self.assertIsNotNone(minutes)

        result = minutes.execute(self.context, "NOW")
        self.assertIsNotNone(result)
        self.assertEqual("0 0", result)