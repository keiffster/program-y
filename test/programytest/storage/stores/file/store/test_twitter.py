from programytest.storage.asserts.store.assert_twitter import TwitterStoreAsserts

from programy.storage.stores.file.store.twitter import FileTwitterStore
from programy.storage.stores.file.engine import FileStorageEngine
from programy.storage.stores.file.config import FileStorageConfiguration


class FileTwitterStoreTests(TwitterStoreAsserts):

    def test_initialise(self):
        config = FileStorageConfiguration()
        engine = FileStorageEngine(config)
        engine.initialise()
        store = FileTwitterStore(engine)
        self.assertEquals(store.storage_engine, engine)

    def test_twitter_storage(self):
        config = FileStorageConfiguration()
        engine = FileStorageEngine(config)
        engine.initialise()
        store = FileTwitterStore(engine)

        self.assert_twitter_storage(store)
