import unittest

from programy.extensions.telecoms.minutes import TelecomMinutesExtension

class TelecomsMinutesExtensionTests(unittest.TestCase):

    def setUp(self):
        self.bot = None
        self.clientid = "testid"

    def test_minutes(self):

        minutes = TelecomMinutesExtension()
        self.assertIsNotNone(minutes)

        result = minutes.execute(self.bot, self.clientid, "NOW")
        self.assertIsNotNone(result)
        self.assertEqual("0 0", result)