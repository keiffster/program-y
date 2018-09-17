import unittest

from programytest.storage.asserts.store.assert_licensekeys import LicenseKeyStoreAsserts

from programy.storage.stores.nosql.mongo.store.licensekeys import MongoLicenseKeysStore
from programy.storage.stores.nosql.mongo.engine import MongoStorageEngine
from programy.storage.stores.nosql.mongo.config import MongoStorageConfiguration

import programytest.storage.engines as Engines


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
