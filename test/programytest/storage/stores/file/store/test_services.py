import os
import os.path
import unittest
from unittest.mock import patch
from programy.storage.stores.file.config import FileStorageConfiguration
from programy.storage.stores.file.config import FileStoreConfiguration
from programy.storage.stores.file.engine import FileStorageEngine
from programy.storage.stores.file.store.services import FileServiceStore
from programy.services.handler import ServiceHandler


class FileServiceStoreTests(unittest.TestCase):

    def test_initialise(self):
        config = FileStorageConfiguration()
        engine = FileStorageEngine(config)
        engine.initialise()
        store = FileServiceStore(engine)
        self.assertEqual(store.storage_engine, engine)

    def test_storage_path(self):
        config = FileStorageConfiguration()
        engine = FileStorageEngine(config)
        engine.initialise()
        store = FileServiceStore(engine)

        self.assertEquals('/tmp/services', store._get_storage_path())
        self.assertIsInstance(store.get_storage(), FileStoreConfiguration)

    def test_load_file_contents(self):
        config = FileStorageConfiguration()
        engine = FileStorageEngine(config)
        engine.initialise()
        store = FileServiceStore(engine)

        handler = ServiceHandler()

        self.assertEqual(1, store._load_file_contents(handler, os.path.dirname(__file__) + os.sep + "data" + os.sep + "services" + os.sep + "wikipedia.yaml"))

    def patch_process_service_yaml(self, handler, file, filename):
        raise Exception("Mock Exception")

    @patch("programy.storage.stores.file.store.services.FileServiceStore._process_service_yaml", patch_process_service_yaml)
    def test_load_file_contents_with_exception(self):
        config = FileStorageConfiguration()
        engine = FileStorageEngine(config)
        engine.initialise()
        store = FileServiceStore(engine)

        handler = ServiceHandler()

        self.assertEqual(0, store._load_file_contents(handler, os.path.dirname(__file__) + os.sep + "data" + os.sep + "services" + os.sep + "wikipedia.yaml"))

    def test_load_services(self):
        config = FileStorageConfiguration()
        config._services_storage = FileStoreConfiguration(dirs=[os.path.dirname(__file__) + os.sep + "data" + os.sep + "services"] , extension="yaml", fileformat="text", encoding="utf-8", delete_on_start=False)
        engine = FileStorageEngine(config)
        engine.initialise()
        store = FileServiceStore(engine)

        handler = ServiceHandler()

        store.load_all(handler)

        self.assertIsNotNone(handler.services['wikipedia'])

