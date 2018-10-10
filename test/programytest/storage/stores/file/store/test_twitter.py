import os.path
import shutil

from programytest.storage.asserts.store.assert_twitter import TwitterStoreAsserts

from programy.storage.stores.file.store.twitter import FileTwitterStore
from programy.storage.stores.file.engine import FileStorageEngine
from programy.storage.stores.file.config import FileStorageConfiguration


class FileTwitterStoreTests(TwitterStoreAsserts):

    def setUp(self):
        self._tmpdir = os.path.dirname(__file__) + os.sep + "twitter"
        self._tmpfile = self._tmpdir + os.sep + "twitter.ids"

    def tearDown(self):
        if os.path.exists(self._tmpdir):
            shutil.rmtree(self._tmpdir)
        self.assertFalse(os.path.exists(self._tmpdir))

    def test_initialise(self):
        config = FileStorageConfiguration()

        config.twitter_storage._dirs = [self._tmpfile]
        config.twitter_storage._has_single_file = True

        engine = FileStorageEngine(config)
        engine.initialise()
        store = FileTwitterStore(engine)
        self.assertEqual(store.storage_engine, engine)

    def test_twitter_storage(self):
        config = FileStorageConfiguration()

        config.twitter_storage._dirs = [self._tmpfile]
        config.twitter_storage._has_single_file = True

        engine = FileStorageEngine(config)
        engine.initialise()
        store = FileTwitterStore(engine)

        self.assert_twitter_storage(store)
