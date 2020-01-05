import os
import os.path
from unittest.mock import patch
from programy.mappings.maps import MapCollection
from programy.storage.stores.file.config import FileStorageConfiguration
from programy.storage.stores.file.config import FileStoreConfiguration
from programy.storage.stores.file.engine import FileStorageEngine
from programy.storage.stores.file.store.maps import FileMapsStore
from programytest.storage.asserts.store.assert_maps import MapStoreAsserts


class FileMapsStoreTests(MapStoreAsserts):

    def test_initialise(self):
        config = FileStorageConfiguration()
        engine = FileStorageEngine(config)
        engine.initialise()
        store = FileMapsStore(engine)
        self.assertEqual(store.storage_engine, engine)

    def test_storage_path(self):
        config = FileStorageConfiguration()
        engine = FileStorageEngine(config)
        engine.initialise()
        store = FileMapsStore(engine)

        self.assertEquals(['/tmp/maps'], store._get_storage_path())
        self.assertIsInstance(store.get_storage(), FileStoreConfiguration)

    def test_load_from_test_dir_no_subdir(self):
        config = FileStorageConfiguration()
        config._maps_storage = FileStoreConfiguration(dirs=[os.path.dirname(__file__) + os.sep + "data" + os.sep + "maps" + os.sep + "text"], extension="txt", subdirs=False, fileformat="text", encoding="utf-8", delete_on_start=False)
        engine = FileStorageEngine(config)
        engine.initialise()
        store = FileMapsStore(engine)

        map_collection = MapCollection()
        store.load_all(map_collection)

        self.assertTrue(map_collection.contains('TESTMAP'))
        the_map = map_collection.map('TESTMAP')
        self.assertIsNotNone(the_map)
        self.assertEqual("6", the_map['ANT'])

    def test_load_from_test_dir_with_subdir(self):
        config = FileStorageConfiguration()
        config._maps_storage = FileStoreConfiguration(dirs=[os.path.dirname(__file__) + os.sep + "data" + os.sep + "maps" + os.sep + "text"], extension="txt", subdirs=True, fileformat="text", encoding="utf-8", delete_on_start=False)
        engine = FileStorageEngine(config)
        engine.initialise()
        store = FileMapsStore(engine)

        map_collection = MapCollection()
        store.load_all(map_collection)

        self.assertTrue(map_collection.contains('TESTMAP'))
        the_map = map_collection.map('TESTMAP')
        self.assertIsNotNone(the_map)
        self.assertEqual("6", the_map['ANT'])

        self.assertTrue(map_collection.contains('TESTMAP2'))
        the_map = map_collection.map('TESTMAP2')
        self.assertIsNotNone(the_map)
        self.assertEqual("grrrrr", the_map['BEAR'])

    def patch_load_map_file(self, filename, the_map):
        raise Exception("Mock Exception")

    @patch ("programy.storage.stores.file.store.maps.FileMapsStore._load_map_file", patch_load_map_file)
    def test_load_with_exception(self):
        config = FileStorageConfiguration()
        engine = FileStorageEngine(config)
        engine.initialise()
        store = FileMapsStore(engine)

        map_collection = MapCollection()
        store.load(map_collection, os.path.dirname(__file__) + os.sep + "data" + os.sep + "maps" + os.sep + "text" + os.sep + "testmap.txt")

        self.assertFalse(map_collection.contains('TESTMAP'))
