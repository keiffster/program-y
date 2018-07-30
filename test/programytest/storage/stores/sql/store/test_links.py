from programytest.storage.asserts.store.assert_links import LinkStoreAsserts

from programy.storage.stores.sql.store.links import SQLLinkStore
from programy.storage.stores.sql.engine import SQLStorageEngine
from programy.storage.stores.sql.config import SQLStorageConfiguration


class SQLLinkStoreTests(LinkStoreAsserts):

    def test_initialise(self):
        config = SQLStorageConfiguration()
        engine = SQLStorageEngine(config)
        engine.initialise()
        store = SQLLinkStore(engine)
        self.assertEquals(store.storage_engine, engine)

    def test_links_storage(self):
        config = SQLStorageConfiguration()
        engine = SQLStorageEngine(config)
        engine.initialise()
        store = SQLLinkStore(engine)
        self.assertEquals(store.storage_engine, engine)

        self.assert_links_storage(store)

