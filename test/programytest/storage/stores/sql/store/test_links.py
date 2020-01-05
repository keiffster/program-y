import unittest
from unittest.mock import patch
import programytest.storage.engines as Engines
from programy.storage.stores.sql.config import SQLStorageConfiguration
from programy.storage.stores.sql.engine import SQLStorageEngine
from programy.storage.stores.sql.store.links import SQLLinkStore
from programytest.storage.asserts.store.assert_links import LinkStoreAsserts


class SQLLinkStoreTests(LinkStoreAsserts):

    @unittest.skipIf(Engines.sql is False, Engines.sql_disabled)
    def test_initialise(self):
        config = SQLStorageConfiguration()
        engine = SQLStorageEngine(config)
        engine.initialise()
        store = SQLLinkStore(engine)
        self.assertEqual(store.storage_engine, engine)

    @unittest.skipIf(Engines.sql is False, Engines.sql_disabled)
    def test_links_storage(self):
        config = SQLStorageConfiguration()
        engine = SQLStorageEngine(config)
        engine.initialise()
        store = SQLLinkStore(engine)
        self.assertEqual(store.storage_engine, engine)

        self.assert_links_storage(store)

    def patch_delete_link(self, userid):
        raise Exception("Mock Exception")

    @patch("programy.storage.stores.sql.store.links.SQLLinkStore._delete_link", patch_delete_link)
    @unittest.skipIf(Engines.sql is False, Engines.sql_disabled)
    def test_remove_link_with_exception(self):
        config = SQLStorageConfiguration()
        engine = SQLStorageEngine(config)
        engine.initialise()
        store = SQLLinkStore(engine)
        self.assertEqual(store.storage_engine, engine)

        self.assert_remove_link_with_exception(store)

    def patch_get_link(self, userid):
        return None

    @patch("programy.storage.stores.sql.store.links.SQLLinkStore._get_link", patch_get_link)
    @unittest.skipIf(Engines.sql is False, Engines.sql_disabled)
    def test_update_link_not_found(self):
        config = SQLStorageConfiguration()
        engine = SQLStorageEngine(config)
        engine.initialise()
        store = SQLLinkStore(engine)
        self.assertEqual(store.storage_engine, engine)

        self.assert_update_link_not_found(store)
