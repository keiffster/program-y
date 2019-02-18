import unittest

from programytest.storage.asserts.store.assert_licensekeys import LicenseKeyStoreAsserts

from programy.storage.stores.sql.store.licensekeys import SQLLicenseKeysStore
from programy.storage.stores.sql.engine import SQLStorageEngine
from programy.storage.stores.sql.config import SQLStorageConfiguration

import programytest.storage.engines as Engines


class SQLLicenseKeysStoreTests(LicenseKeyStoreAsserts):

    @unittest.skipIf(Engines.sql is False, Engines.sql_disabled)
    def test_initialise(self):
        config = SQLStorageConfiguration()
        engine = SQLStorageEngine(config)
        engine.initialise()
        store = SQLLicenseKeysStore(engine)
        self.assertEqual(store.storage_engine, engine)

    @unittest.skipIf(Engines.sql is False, Engines.sql_disabled)
    def test_upload_license_keys_from_file(self):
        config = SQLStorageConfiguration()
        engine = SQLStorageEngine(config)
        engine.initialise()
        store = SQLLicenseKeysStore(engine)

        self.assert_upload_license_keys_from_file(store)
