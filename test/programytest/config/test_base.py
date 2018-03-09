import unittest
import os

from programy.config.base import BaseConfigurationData


class BaseConfigurationDataTests(unittest.TestCase):

    def test_sub_bot_root(self):
        config = BaseConfigurationData("test")

        replaced = config.sub_bot_root( os.sep + "data",  os.sep + "root")
        self.assertIsNotNone(replaced)
        self.assertEqual(replaced,  os.sep + "data")

        replaced = config.sub_bot_root("$BOT_ROOT"+ os.sep + "data",  os.sep + "root")
        self.assertIsNotNone(replaced)
        self.assertEqual(replaced,  os.sep + "root" + os.sep + "data")

        replaced = config.sub_bot_root("$BOT_ROOT$BOT_ROOT"+ os.sep + "data",  os.sep + "root")
        self.assertIsNotNone(replaced)
        self.assertEqual(replaced,  os.sep + "root" + os.sep + "root" + os.sep + "data")

    def test_additionals(self):
        config = BaseConfigurationData("test")

        self.assertEqual([], config.additionals_to_add())

        config._additionals["key1"] = "value1"
        config._additionals["key2"] = "value2"

        self.assertTrue(config.exists("key1"))
        self.assertEqual("value1", config.value("key1"))

        self.assertTrue(config.exists("key2"))
        self.assertEqual("value2", config.value("key2"))

        self.assertFalse(config.exists("key3"))
