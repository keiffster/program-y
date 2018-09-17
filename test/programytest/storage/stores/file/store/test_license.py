import unittest
import os
import os.path

from programy.storage.stores.file.store.licensekeys import FileLicenseStore
from programy.storage.stores.file.engine import FileStorageEngine
from programy.storage.stores.file.config import FileStorageConfiguration
from programy.utils.license.keys import LicenseKeys
from programy.storage.stores.file.config import FileStoreConfiguration

class FileLicenseKeysStoreTests(unittest.TestCase):

    def test_initialise(self):
        config = FileStorageConfiguration()
        engine = FileStorageEngine(config)
        engine.initialise()
        store = FileLicenseStore(engine)
        self.assertEqual(store.storage_engine, engine)

    def test_load_license_key(self):
        config = FileStorageConfiguration()
        config._license_storage =  FileStoreConfiguration(file=os.path.dirname(__file__) + os.sep + "data" + os.sep + "licenses" + os.sep + "test_license.keys", format="text", encoding="utf-8", delete_on_start=False)
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
