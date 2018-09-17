import os
import os.path

from programytest.storage.asserts.store.assert_category import CategoryStoreAsserts
from programy.storage.stores.file.store.categories import FileCategoryStore
from programy.storage.stores.file.engine import FileStorageEngine
from programy.storage.stores.file.config import FileStorageConfiguration
from programy.storage.stores.file.store.config import FileStoreConfiguration


class MockAIMLParser(object):

    def __init__(self):
        self._parsed_files = []

    def parse_from_file(self, filename, userid="*"):
        self._parsed_files.append(filename)


class FileCategoryStoreTests(CategoryStoreAsserts):

    def test_initialise(self):
        config = FileStorageConfiguration()
        engine = FileStorageEngine(config)
        engine.initialise()
        store = FileCategoryStore(engine)
        self.assertEqual(store.storage_engine, engine)

    def test_load_from_text_file(self):
        config = FileStorageConfiguration()
        file = os.path.dirname(__file__) + os.sep + "data" + os.sep + "categories" + os.sep + "kinghorn.aiml"
        self.assertTrue(os.path.exists(file))
        config._categories_storage = FileStoreConfiguration(file=file, format="xml", encoding="utf-8", delete_on_start=False)
        engine = FileStorageEngine(config)
        engine.initialise()
        store = FileCategoryStore(engine)

        parser = MockAIMLParser()
        store.load_all(parser)

        self.assertEqual(1, len(parser._parsed_files))
        self.assertTrue(parser._parsed_files[0].endswith("/kinghorn.aiml"))

    def test_load_from_test_dir_no_subdir(self):
        config = FileStorageConfiguration()
        dirs = os.path.dirname(__file__) + os.sep + "data" + os.sep + "categories"
        self.assertTrue(os.path.exists(dirs))
        config._categories_storage = FileStoreConfiguration(dirs=[dirs], extension="aiml", subdirs=False, format="xml", encoding="utf-8", delete_on_start=False)
        engine = FileStorageEngine(config)
        engine.initialise()
        store = FileCategoryStore(engine)

        parser = MockAIMLParser()
        store.load_all(parser)

        self.assertEqual(1, len(parser._parsed_files))
        self.assertTrue(parser._parsed_files[0].endswith("/kinghorn.aiml"))

    def test_load_from_test_dir_with_subdir(self):
        config = FileStorageConfiguration()
        dirs = os.path.dirname(__file__) + os.sep + "data" + os.sep + "categories"
        self.assertTrue(os.path.exists(dirs))
        config._categories_storage = FileStoreConfiguration(dirs=[dirs], extension="aiml", subdirs=True, format="xml", encoding="utf-8", delete_on_start=False)
        engine = FileStorageEngine(config)
        engine.initialise()
        store = FileCategoryStore(engine)

        parser = MockAIMLParser()
        store.load_all(parser)

        self.assertEqual(3, len(parser._parsed_files))
        self.assertTrue(parser._parsed_files[0].endswith("/kinghorn.aiml"))
        self.assertTrue(parser._parsed_files[1].endswith("/fife.aiml"))
        self.assertTrue(parser._parsed_files[2].endswith("/scotland.aiml"))
