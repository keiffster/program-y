import unittest
import os
from unittest.mock import patch
import programytest.storage.engines as Engines
from programy.storage.stores.sql.config import SQLStorageConfiguration
from programy.storage.stores.sql.engine import SQLStorageEngine
from programy.storage.stores.sql.store.licensekeys import SQLLicenseKeysStore
from programytest.storage.asserts.store.assert_licensekeys import LicenseKeyStoreAsserts


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

    def patch_read_lines_from_file(self, filename, verbose):
        raise Exception("Mock Exception")

    @unittest.skipIf(Engines.sql is False, Engines.sql_disabled)
    @patch("programy.storage.stores.sql.store.licensekeys.SQLLicenseKeysStore._read_lines_from_file",
           patch_read_lines_from_file)
    def test_upload_from_file_with_exception(self):
        config = SQLStorageConfiguration()
        engine = SQLStorageEngine(config)
        engine.initialise()
        store = SQLLicenseKeysStore(engine)

        store.empty()

        count, success = store.upload_from_file(
            os.path.dirname(__file__) + os.sep + "data" + os.sep + "licenses" + os.sep + "test_license.keys")
        self.assertEquals(0, count)
