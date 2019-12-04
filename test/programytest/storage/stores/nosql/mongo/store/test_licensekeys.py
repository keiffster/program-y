import unittest
import os
from unittest.mock import patch
import programytest.storage.engines as Engines
from programy.storage.stores.nosql.mongo.config import MongoStorageConfiguration
from programy.storage.stores.nosql.mongo.engine import MongoStorageEngine
from programy.storage.stores.nosql.mongo.store.licensekeys import MongoLicenseKeysStore
from programytest.storage.asserts.store.assert_licensekeys import LicenseKeyStoreAsserts


class MongoLicenseKeysStoreTests(LicenseKeyStoreAsserts):

    @unittest.skipIf(Engines.mongo is False, Engines.mongo_disabled)
    def test_initialise(self):
        config = MongoStorageConfiguration()
        engine = MongoStorageEngine(config)
        engine.initialise()
        store = MongoLicenseKeysStore(engine)
        self.assertEqual(store.storage_engine, engine)

    @unittest.skipIf(Engines.mongo is False, Engines.mongo_disabled)
    def test_upload_license_keys_from_file(self):
        config = MongoStorageConfiguration()
        engine = MongoStorageEngine(config)
        engine.initialise()
        store = MongoLicenseKeysStore(engine)

        self.assert_upload_license_keys_from_file(store)

    def patch_read_lines_from_file(self, filename, verbose):
        raise Exception("Mock Exception")

    @unittest.skipIf(Engines.mongo is False, Engines.mongo_disabled)
    @patch("programy.storage.stores.nosql.mongo.store.licensekeys.MongoLicenseKeysStore._read_lines_from_file", patch_read_lines_from_file)
    def test_upload_from_file_with_exception(self):
        config = MongoStorageConfiguration()
        engine = MongoStorageEngine(config)
        engine.initialise()
        store = MongoLicenseKeysStore(engine)

        store.empty()

        count, success = store.upload_from_file(os.path.dirname(__file__) + os.sep + "data" + os.sep + "licenses" + os.sep + "test_license.keys")
        self.assertEquals(0, count)
        self.assertEquals(0, success)