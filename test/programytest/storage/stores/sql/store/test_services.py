import unittest
from unittest.mock import patch
import programytest.storage.engines as Engines
from programy.storage.stores.sql.config import SQLStorageConfiguration
from programy.storage.stores.sql.engine import SQLStorageEngine
from programy.storage.stores.sql.store.services import SQLServicesStore
from programytest.storage.asserts.store.assert_services import ServicesStoreAsserts


class SQLServicesStoreTests(ServicesStoreAsserts):

    @unittest.skipIf(Engines.sql is False, Engines.sql_disabled)
    def test_initialise(self):
        config = SQLStorageConfiguration()
        engine = SQLStorageEngine(config)
        engine.initialise()
        store = SQLServicesStore(engine)
        self.assertEqual(store.storage_engine, engine)

    @unittest.skipIf(Engines.sql is False, Engines.sql_disabled)
    def test_load_services(self):
        config = SQLStorageConfiguration()
        engine = SQLStorageEngine(config)
        engine.initialise()
        store = SQLServicesStore(engine)

        self.assert_load(store)

    @staticmethod
    def patch_instantiate_class(class_string):
        raise Exception("Mock Exception")

    @unittest.skipIf(Engines.sql is False, Engines.sql_disabled)
    @patch("programy.utils.classes.loader.ClassLoader.instantiate_class", patch_instantiate_class)
    def test_load_services_exception(self):
        config = SQLStorageConfiguration()
        engine = SQLStorageEngine(config)
        engine.initialise()
        store = SQLServicesStore(engine)

        self.assert_load_exception(store)

    @unittest.skipIf(Engines.sql is False, Engines.sql_disabled)
    def test_upload_from_file(self):
        config = SQLStorageConfiguration()
        engine = SQLStorageEngine(config)
        engine.initialise()
        store = SQLServicesStore(engine)

        self.assert_upload_from_file(store, verbose=False)

    @unittest.skipIf(Engines.sql is False, Engines.sql_disabled)
    def test_upload_from_file_verbose(self):
        config = SQLStorageConfiguration()
        engine = SQLStorageEngine(config)
        engine.initialise()
        store = SQLServicesStore(engine)

        self.assert_upload_from_file(store, verbose=True)

    def patch_load_services_from_file(self, filename, verbose):
        raise Exception("Mock Exception")

    @unittest.skipIf(Engines.sql is False, Engines.sql_disabled)
    @patch("programy.storage.stores.sql.store.services.SQLServicesStore._load_services_from_file",
           patch_load_services_from_file)
    def test_upload_from_file_exception(self):
        config = SQLStorageConfiguration()
        engine = SQLStorageEngine(config)
        engine.initialise()
        store = SQLServicesStore(engine)

        self.assert_upload_from_file_exception(store)
