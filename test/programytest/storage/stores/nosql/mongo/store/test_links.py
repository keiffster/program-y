from programytest.storage.asserts.store.assert_links import LinkStoreAsserts

from programy.storage.stores.nosql.mongo.store.links import MongoLinkStore
from programy.storage.stores.nosql.mongo.engine import MongoStorageEngine
from programy.storage.stores.nosql.mongo.config import MongoStorageConfiguration


class MongoLinkStoreTests(LinkStoreAsserts):

    def test_initialise(self):
        config = MongoStorageConfiguration()
        engine = MongoStorageEngine(config)
        engine.initialise()
        store = MongoLinkStore(engine)
        self.assertEquals(store.storage_engine, engine)

    def test_links_storage(self):
        config = MongoStorageConfiguration()
        engine = MongoStorageEngine(config)
        engine.initialise()
        store = MongoLinkStore(engine)
        self.assertEquals(store.storage_engine, engine)

        self.assert_links_storage(store)
