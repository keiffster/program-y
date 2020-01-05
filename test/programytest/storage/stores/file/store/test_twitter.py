import os.path
import shutil
from unittest.mock import patch
from programy.storage.stores.file.config import FileStorageConfiguration
from programy.storage.stores.file.engine import FileStorageEngine
from programy.storage.stores.file.store.twitter import FileTwitterStore
from programytest.storage.asserts.store.assert_twitter import TwitterStoreAsserts
from programy.storage.stores.file.config import FileStoreConfiguration


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

    def test_empty(self):
        config = FileStorageConfiguration()
        engine = FileStorageEngine(config)
        engine.initialise()
        store = FileTwitterStore(engine)

        if os.path.exists(store._get_storage_path()) is False:
            os.mkdir(store._get_storage_path())

        store.empty()

        self.assertFalse(os.path.exists(store._get_storage_path()))

    def test_storage_path(self):
        config = FileStorageConfiguration()
        engine = FileStorageEngine(config)
        engine.initialise()
        store = FileTwitterStore(engine)

        self.assertEquals('/tmp/twitter', store._get_storage_path())
        self.assertIsInstance(store.get_storage(), FileStoreConfiguration)

    def test_twitter_storage(self):
        config = FileStorageConfiguration()
        config.twitter_storage._dirs = [self._tmpfile]
        config.twitter_storage._has_single_file = True

        engine = FileStorageEngine(config)
        engine.initialise()
        store = FileTwitterStore(engine)

        self.assert_twitter_storage(store)

    def patch_write_message_ids_to_file(self, twitter_ids_file, last_direct_message_id, last_status_id):
        raise Exception("Mock Exception")

    @patch("programy.storage.stores.file.store.twitter.FileTwitterStore._write_message_ids_to_file", patch_write_message_ids_to_file)
    def test_store_last_message_ids(self):
        config = FileStorageConfiguration()
        config.twitter_storage._dirs = [self._tmpfile]
        config.twitter_storage._has_single_file = True

        engine = FileStorageEngine(config)
        engine.initialise()
        store = FileTwitterStore(engine)

        self.assertFalse(store.store_last_message_ids("99", "100"))

    def patch_load_message_ids_from_file(self, twitter_ids_file):
        raise Exception("Mock Exception")

    @patch("programy.storage.stores.file.store.twitter.FileTwitterStore._load_message_ids_from_file", patch_load_message_ids_from_file)
    def test_load_last_message_ids(self):
        config = FileStorageConfiguration()
        config.twitter_storage._dirs = [self._tmpfile]
        config.twitter_storage._has_single_file = True

        engine = FileStorageEngine(config)
        engine.initialise()
        store = FileTwitterStore(engine)

        last_direct_message_id, last_status_id = store.load_last_message_ids()

        self.assertEquals("-1", last_direct_message_id)
        self.assertEquals("-1", last_status_id)