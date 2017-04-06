import unittest
import os

from programy.utils.license.keys import LicenseKeys

#############################################################################
#

class LicenseKeyTests(unittest.TestCase):

    def test_load_license_keys_data(self):
        keys = LicenseKeys()
        keys.load_license_key_data("""
        KEY1=Key1Data
        KEY2=Key2Data
        # This is a comment
        KEY3=KEY3 Data With Spaces
        This is not a key
        """)
        self.assertTrue(keys.has_key('KEY1'))
        self.assertEquals("Key1Data", keys.get_key("KEY1"))
        self.assertTrue(keys.has_key('KEY2'))
        self.assertEquals("Key2Data", keys.get_key("KEY2"))
        self.assertTrue(keys.has_key('KEY3'))
        self.assertEquals("KEY3 Data With Spaces", keys.get_key("KEY3"))
        with self.assertRaises(Exception):
            keys.get_key("KEY5")

    def test_load_license_keys_file(self):
        keys = LicenseKeys()
        keys.load_license_key_file(os.path.dirname(__file__)+"/test.keys")
        self.assertTrue(keys.has_key('KEY1'))
        self.assertEquals("Key1Data", keys.get_key("KEY1"))
        self.assertTrue(keys.has_key('KEY2'))
        self.assertEquals("Key2Data", keys.get_key("KEY2"))
        self.assertTrue(keys.has_key('KEY3'))
        self.assertEquals("KEY3 Data With Spaces", keys.get_key("KEY3"))
        with self.assertRaises(Exception):
            keys.get_key("KEY5")

