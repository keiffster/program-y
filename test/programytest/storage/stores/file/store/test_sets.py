import os
from unittest.mock import patch
from programy.mappings.sets import SetCollection
from programy.storage.stores.file.config import FileStorageConfiguration
from programy.storage.stores.file.config import FileStoreConfiguration
from programy.storage.stores.file.engine import FileStorageEngine
from programy.storage.stores.file.store.sets import FileSetsStore
from programytest.storage.asserts.store.assert_sets import SetStoreAsserts


class FileSetsStoreTests(SetStoreAsserts):

    def test_initialise(self):
        config = FileStorageConfiguration()
        engine = FileStorageEngine(config)
        engine.initialise()
        store = FileSetsStore(engine)
        self.assertEqual(store.storage_engine, engine)

    def test_storage_path(self):
        config = FileStorageConfiguration()
        engine = FileStorageEngine(config)
        engine.initialise()
        store = FileSetsStore(engine)

        self.assertEquals(['/tmp/sets'], store._get_storage_path())
        self.assertIsInstance(store.get_storage(), FileStoreConfiguration)

    def test_load_from_test_dir_no_subdir(self):
        config = FileStorageConfiguration()
        config._sets_storage = FileStoreConfiguration(dirs=[os.path.dirname(__file__) + os.sep + "data" + os.sep + "sets" + os.sep + "text"], extension="txt", subdirs=False, fileformat="text", encoding="utf-8", delete_on_start=False)
        engine = FileStorageEngine(config)
        engine.initialise()
        store = FileSetsStore(engine)

        set_collection = SetCollection()
        store.load_all(set_collection)

        self.assertTrue(set_collection.contains('TESTSET'))
        values = set_collection.set('TESTSET')
        self.assertTrue('VAL1' in values)
        self.assertTrue('VAL2' in values)
        self.assertTrue('VAL3' in values)
        self.assertTrue('VAL4' in values)

    def test_load_from_test_dir_with_subdir(self):
        config = FileStorageConfiguration()
        config._sets_storage = FileStoreConfiguration(dirs=[os.path.dirname(__file__) + os.sep + "data" + os.sep + "sets" + os.sep + "text"], extension="txt", subdirs=True, fileformat="text", encoding="utf-8", delete_on_start=False)
        engine = FileStorageEngine(config)
        engine.initialise()
        store = FileSetsStore(engine)

        set_collection = SetCollection()
        store.load_all(set_collection)

        self.assertTrue(set_collection.contains('TESTSET'))
        values = set_collection.set('TESTSET')
        self.assertTrue('VAL1' in values)
        self.assertTrue('VAL2' in values)
        self.assertTrue('VAL3' in values)
        self.assertTrue('VAL4' in values)

        self.assertTrue(set_collection.contains('TESTSET2'))
        values = set_collection.set('TESTSET2')
        self.assertEqual(4, len(values))
        self.assertTrue('VAL5' in values)
        self.assertTrue('VAL6' in values)
        self.assertTrue('VAL7' in values)
        self.assertTrue('VAL8' in values)

    def test_load(self):
        config = FileStorageConfiguration()
        engine = FileStorageEngine(config)
        engine.initialise()
        store = FileSetsStore(engine)

        set_collection = SetCollection()
        self.assertTrue(store.load(set_collection, os.path.dirname(__file__) + os.sep + "data" + os.sep + "sets" + os.sep + "text" + os.sep + "testset.txt"))

        self.assertTrue(set_collection.contains('TESTSET'))
        values = set_collection.set('TESTSET')
        self.assertTrue('VAL1' in values)
        self.assertTrue('VAL2' in values)
        self.assertTrue('VAL3' in values)
        self.assertTrue('VAL4' in values)

    def patch_load_sets_from_file(self, filename, the_set):
        raise Exception("Mock Exception")

    @patch("programy.storage.stores.file.store.sets.FileSetsStore._load_sets_from_file", patch_load_sets_from_file)
    def test_load_with_exception(self):
        config = FileStorageConfiguration()
        engine = FileStorageEngine(config)
        engine.initialise()
        store = FileSetsStore(engine)

        set_collection = SetCollection()
        self.assertFalse(store.load(set_collection, os.path.dirname(__file__) + os.sep + "data" + os.sep + "sets" + os.sep + "text" + os.sep + "testset.txt"))
