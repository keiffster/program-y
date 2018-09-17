from programytest.storage.asserts.store.assert_maps import MapStoreAsserts
import os
import os.path

from programy.storage.stores.file.store.maps import FileMapsStore
from programy.storage.stores.file.engine import FileStorageEngine
from programy.storage.stores.file.config import FileStorageConfiguration
from programy.mappings.maps import MapCollection
from programy.storage.stores.file.config import FileStoreConfiguration

class FileMapsStoreTests(MapStoreAsserts):

    def test_initialise(self):
        config = FileStorageConfiguration()
        engine = FileStorageEngine(config)
        engine.initialise()
        store = FileMapsStore(engine)
        self.assertEqual(store.storage_engine, engine)

    def test_load_from_test_dir_no_subdir(self):
        config = FileStorageConfiguration()
        config._maps_storage = FileStoreConfiguration(dirs=[os.path.dirname(__file__) + os.sep + "data" + os.sep + "maps" + os.sep + "text"], extension="txt", subdirs=False, format="text", encoding="utf-8", delete_on_start=False)
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
        config._maps_storage = FileStoreConfiguration(dirs=[os.path.dirname(__file__) + os.sep + "data" + os.sep + "maps" + os.sep + "text"], extension="txt", subdirs=True, format="text", encoding="utf-8", delete_on_start=False)
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
