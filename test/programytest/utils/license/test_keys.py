import unittest
import os

from programy.utils.license.keys import LicenseKeys

#############################################################################
#

class LicenseKeyTests(unittest.TestCase):

    def test_add_keys(self):
        keys = LicenseKeys()
        self.assertFalse(keys.has_key("KEY1"))
        keys.add_key("KEY1", "VALUE1")
        self.assertTrue(keys.has_key("KEY1"))
        self.assertEqual("VALUE1", keys.get_key("KEY1"))
        keys.add_key("KEY1", "VALUE2")
        self.assertTrue(keys.has_key("KEY1"))
        self.assertEqual("VALUE2", keys.get_key("KEY1"))

    def test_load_license_keys_file(self):
        keys = LicenseKeys()
        keys.add_key("KEY1", "Key1Data")
        keys.add_key("KEY2", "Key2Data")
        keys.add_key("KEY3", "KEY3 Data With Spaces")

        self.assertTrue(keys.has_key('KEY1'))
        self.assertEqual("Key1Data", keys.get_key("KEY1"))
        self.assertTrue(keys.has_key('KEY2'))
        self.assertEqual("Key2Data", keys.get_key("KEY2"))
        self.assertTrue(keys.has_key('KEY3'))
        self.assertEqual("KEY3 Data With Spaces", keys.get_key("KEY3"))
        with self.assertRaises(Exception):
            keys.get_key("KEY5")

