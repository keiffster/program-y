import unittest
import os
import os.path

from programy.utils.license.keys import LicenseKeys


class LicenseKeyStoreAsserts(unittest.TestCase):

    def assert_upload_license_keys_from_file(self, store):
        store.empty()

        store.upload_from_file(os.path.dirname(__file__) + os.sep + "data" + os.sep + "licenses" + os.sep + "test_license.keys")

        license_keys = LicenseKeys()
        store.load(license_keys)

        self.assertTrue(license_keys.has_key("TESTKEY1"))
        self.assertEqual("VALUE1", license_keys.get_key("TESTKEY1"))
        self.assertTrue(license_keys.has_key("TESTKEY2"))
        self.assertEqual("VERY LONG VALUE 2", license_keys.get_key("TESTKEY2"))
