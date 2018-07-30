import unittest

from programy.extensions.telecoms.minutes import TelecomMinutesExtension

from programytest.client import TestClient

class TelecomsMinutesExtensionTests(unittest.TestCase):

    def setUp(self):
        client = TestClient()
        self.context = client.create_client_context("testid")

    def test_minutes(self):

        minutes = TelecomMinutesExtension()
        self.assertIsNotNone(minutes)

        result = minutes.execute(self.context, "NOW")
        self.assertIsNotNone(result)
        self.assertEqual("0 0", result)