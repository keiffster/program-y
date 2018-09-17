from programytest.storage.asserts.store.assert_properties import PropertyStoreAsserts
import os
import os.path
import shutil

from programy.storage.stores.file.store.properties import FilePropertyStore
from programy.storage.stores.file.engine import FileStorageEngine
from programy.storage.stores.file.config import FileStorageConfiguration
from programy.mappings.properties import PropertiesCollection
from programy.storage.stores.file.config import FileStoreConfiguration


class FilePropertyStoreTests(PropertyStoreAsserts):

    def test_initialise(self):
        config = FileStorageConfiguration()
        engine = FileStorageEngine(config)
        engine.initialise()
        store = FilePropertyStore(engine)
        self.assertEqual(store.storage_engine, engine)

    def test_properties_storage(self):
        config = FileStorageConfiguration()
        tmpdir = os.path.dirname(__file__) + os.sep + "properties"
        tmpfile = tmpdir + os.sep + "properties.txt"
        config.properties_storage._dirs = [tmpfile]
        config.properties_storage._has_single_file = True
        engine = FileStorageEngine(config)
        engine.initialise()
        store = FilePropertyStore(engine)

        if os.path.exists(tmpdir) is False:
            os.mkdir(tmpdir)
        self.assertTrue(os.path.exists(tmpdir))

        self.assert_properties_storage(store)

        shutil.rmtree(tmpdir)
        self.assertFalse(os.path.exists(tmpdir))

    def test_property_storage(self):
        config = FileStorageConfiguration()
        tmpdir = os.path.dirname(__file__) + os.sep + "properties"
        tmpfile = tmpdir + os.sep + "properties.txt"
        config.properties_storage._dirs = [tmpfile]
        config.properties_storage._has_single_file = True
        engine = FileStorageEngine(config)
        engine.initialise()
        store = FilePropertyStore(engine)

        if os.path.exists(tmpdir) is False:
            os.mkdir(tmpdir)
        self.assertTrue(os.path.exists(tmpdir))

        self.assert_property_storage(store)

        shutil.rmtree(tmpdir)
        self.assertFalse(os.path.exists(tmpdir))

    def test_empty_properties(self):
        config = FileStorageConfiguration()
        tmpdir = os.path.dirname(__file__) + os.sep + "properties"
        tmpfile = tmpdir + os.sep + "properties.txt"
        config.properties_storage._dirs = [tmpfile]
        config.properties_storage._has_single_file = True
        engine = FileStorageEngine(config)
        engine.initialise()
        store = FilePropertyStore(engine)

        if os.path.exists(tmpdir) is False:
            os.mkdir(tmpdir)
        self.assertTrue(os.path.exists(tmpdir))

        self.assert_empty_properties(store)

        shutil.rmtree(tmpdir)
        self.assertFalse(os.path.exists(tmpdir))

    def test_load_properties(self):
        config = FileStorageConfiguration()
        config._properties_storage = FileStoreConfiguration(file=os.path.dirname(__file__) + os.sep + "data" + os.sep + "lookups" + os.sep + "text" + os.sep + "properties.txt", format="text", encoding="utf-8", delete_on_start=False)
        engine = FileStorageEngine(config)
        engine.initialise()
        store = FilePropertyStore(engine)

        collection = PropertiesCollection()
        store.load(collection)

        self.assertTrue(collection.has_key("name"))
        self.assertTrue("Y-Bot", collection.value("name"))
        self.assertTrue(collection.has_key("firstname"))
        self.assertTrue("Y", collection.value("firstname"))
        self.assertTrue(collection.has_key("middlename"))
        self.assertTrue("AIML", collection.value("middlename"))