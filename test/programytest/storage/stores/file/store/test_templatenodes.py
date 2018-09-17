import unittest
import os
import os.path

from programy.storage.stores.file.store.nodes import FileTemplateNodeStore
from programy.storage.stores.file.engine import FileStorageEngine
from programy.storage.stores.file.config import FileStorageConfiguration
from programy.parser.template.factory import TemplateNodeFactory
from programy.storage.stores.file.config import FileStoreConfiguration


class FileTemplateNodeStoreTests(unittest.TestCase):

    def test_initialise(self):
        config = FileStorageConfiguration()
        engine = FileStorageEngine(config)
        engine.initialise()
        store = FileTemplateNodeStore(engine)
        self.assertEqual(store.storage_engine, engine)

    def test_load_variables(self):
        config = FileStorageConfiguration()
        config._template_nodes_storage = FileStoreConfiguration(file=os.path.dirname(__file__) + os.sep + "data" + os.sep + "nodes" + os.sep + "template_nodes.conf", format="text", encoding="utf-8", delete_on_start=False)
        engine = FileStorageEngine(config)
        engine.initialise()
        store = FileTemplateNodeStore(engine)

        collection = TemplateNodeFactory()
        store.load(collection)

        self.assertEqual(64, len(collection.nodes))
        self.assertTrue(collection.exists("lowercase"))