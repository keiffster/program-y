import os
import os.path
import unittest

from programy.storage.stores.file.config import FileStorageConfiguration
from programy.storage.stores.file.config import FileStoreConfiguration
from programy.storage.stores.file.engine import FileStorageEngine
from programy.storage.stores.file.store.licensekeys import FileLicenseStore
from programy.utils.license.keys import LicenseKeys


class FileLicenseKeysStoreTests(unittest.TestCase):

    def test_initialise(self):
        config = FileStorageConfiguration()
        engine = FileStorageEngine(config)
        engine.initialise()
        store = FileLicenseStore(engine)
        self.assertEqual(store.storage_engine, engine)

    def test_storage_path(self):
        config = FileStorageConfiguration()
        engine = FileStorageEngine(config)
        engine.initialise()
        store = FileLicenseStore(engine)

        self.assertEquals('/tmp/licenses/license.keys', store._get_storage_path())
        self.assertIsInstance(store.get_storage(), FileStoreConfiguration)

    def test_process_license_key_line(self):
        config = FileStorageConfiguration()
        engine = FileStorageEngine(config)
        engine.initialise()
        store = FileLicenseStore(engine)

        license_keys = LicenseKeys()

        self.assertFalse(store._process_license_key_line(license_keys, ""))
        self.assertFalse(store._process_license_key_line(license_keys, "#"))
        self.assertFalse(store._process_license_key_line(license_keys, "# Comment"))
        self.assertFalse(store._process_license_key_line(license_keys, "INVALID:Key"))
        self.assertTrue(store._process_license_key_line(license_keys, "VALID=KEY"))


    def test_load_license_key(self):
        config = FileStorageConfiguration()
        config._license_storage =  FileStoreConfiguration(file=os.path.dirname(__file__) + os.sep + "data" + os.sep + "licenses" + os.sep + "test_license.keys", fileformat="text", encoding="utf-8", delete_on_start=False)
        engine = FileStorageEngine(config)
        engine.initialise()
        store = FileLicenseStore(engine)

        store.empty()

        license_keys = LicenseKeys()
        store.load(license_keys)

        self.assertTrue(license_keys.has_key("TESTKEY1"))
        self.assertEqual("VALUE1", license_keys.get_key("TESTKEY1"))
        self.assertTrue(license_keys.has_key("TESTKEY2"))
        self.assertEqual("VERY LONG VALUE 2", license_keys.get_key("TESTKEY2"))

