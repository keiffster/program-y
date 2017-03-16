import unittest

from programy.config.base import BaseConfigurationData

class BaseConfigurationDataTests(unittest.TestCase):

    def test_sub_bot_root(self):
        config = BaseConfigurationData("test")

        replaced = config.sub_bot_root("/data", "/root")
        self.assertIsNotNone(replaced)
        self.assertEqual(replaced, "/data")

        replaced = config.sub_bot_root("$BOT_ROOT/data", "/root")
        self.assertIsNotNone(replaced)
        self.assertEqual(replaced, "/root/data")

        replaced = config.sub_bot_root("$BOT_ROOT$BOT_ROOT/data", "/root")
        self.assertIsNotNone(replaced)
        self.assertEqual(replaced, "/root/root/data")

