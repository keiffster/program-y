import unittest
import os.path
import shutil

from programy.storage.stores.file.store.braintree import FileBraintreeStore
from programy.storage.stores.file.engine import FileStorageEngine
from programy.storage.stores.file.config import FileStorageConfiguration
from programy.storage.stores.file.store.config import FileStoreConfiguration
from programytest.client import TestClient

class FileBraintreeStoreTests(unittest.TestCase):

    def test_initialise(self):
        config = FileStorageConfiguration()
        engine = FileStorageEngine(config)
        engine.initialise()
        store = FileBraintreeStore(engine)
        self.assertEqual(store.storage_engine, engine)

    def test_save_braintree(self):
        config = FileStorageConfiguration()
        config._categories_storage = FileStoreConfiguration(dirs=[os.path.dirname(__file__) + os.sep + "data" + os.sep + "categories"], extension="aiml", subdirs=False, format="xml", encoding="utf-8", delete_on_start=False)
        tmpdir = os.path.dirname(__file__) + os.sep + "braintree"
        tmpfile = tmpdir + os.sep + "braintree.xml"
        config.braintree_storage._dirs = [tmpfile]
        config.braintree_storage._has_single_file = True
        engine = FileStorageEngine(config)
        engine.initialise()
        store = FileBraintreeStore(engine)

        path = store._get_dir_from_path(store._get_storage_path())
        if os.path.exists(path):
            shutil.rmtree(path)
        self.assertFalse(os.path.exists(path))

        test_client = TestClient()
        client_context = test_client.create_client_context("test1")
        pattern_graph = client_context.brain.aiml_parser.pattern_parser

        store.save_braintree(client_context, pattern_graph)

        self.assertTrue(os.path.exists(store._get_storage_path()))

        shutil.rmtree(tmpdir)
        self.assertFalse(os.path.exists(tmpdir))
