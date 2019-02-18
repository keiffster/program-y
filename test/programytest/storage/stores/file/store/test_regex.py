import unittest
import os
import os.path
import re

from programy.storage.stores.file.store.properties import FileRegexStore
from programy.storage.stores.file.engine import FileStorageEngine
from programy.storage.stores.file.config import FileStorageConfiguration
from programy.mappings.properties import RegexTemplatesCollection
from programy.storage.stores.file.config import FileStoreConfiguration

class FileRegexStoreTests(unittest.TestCase):

    def test_initialise(self):
        config = FileStorageConfiguration()
        engine = FileStorageEngine(config)
        engine.initialise()
        store = FileRegexStore(engine)
        self.assertEqual(store.storage_engine, engine)

    def test_load_regex(self):
        config = FileStorageConfiguration()
        config._regex_storage =  FileStoreConfiguration(file=os.path.dirname(__file__) + os.sep + "data" + os.sep + "lookups" + os.sep + "text" + os.sep + "regex-templates.txt", format="text", encoding="utf-8", delete_on_start=False)
        engine = FileStorageEngine(config)
        engine.initialise()
        store = FileRegexStore(engine)

        store.empty()

        collection = RegexTemplatesCollection()
        store.load(collection)

        self.assertTrue(collection.has_regex("anything"))
        self.assertEqual(re.compile('^.*$', re.IGNORECASE), collection.regex("anything"))
        self.assertTrue(collection.has_regex("legion"))
        self.assertFalse(collection.has_regex("XXXXX"))
