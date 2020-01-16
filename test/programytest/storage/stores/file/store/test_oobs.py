import os
import os.path
import unittest
from unittest.mock import patch
from programy.storage.stores.file.config import FileStorageConfiguration
from programy.storage.stores.file.config import FileStoreConfiguration
from programy.storage.stores.file.engine import FileStorageEngine
from programy.storage.stores.file.store.oobs import FileOOBStore
from programy.oob.handler import OOBHandler


class FileOOBStoreTests(unittest.TestCase):

    def test_initialise(self):
        config = FileStorageConfiguration()
        engine = FileStorageEngine(config)
        engine.initialise()
        store = FileOOBStore(engine)
        self.assertEqual(store.storage_engine, engine)

    def test_storage_path(self):
        config = FileStorageConfiguration()
        engine = FileStorageEngine(config)
        engine.initialise()
        store = FileOOBStore(engine)

        self.assertEquals('/tmp/oob/callmom.conf', store._get_storage_path())
        self.assertIsInstance(store.get_storage(), FileStoreConfiguration)

    def test_process_line(self):
        config = FileStorageConfiguration()
        engine = FileStorageEngine(config)
        engine.initialise()
        store = FileOOBStore(engine)

        handler = OOBHandler()

        self.assertFalse(store._process_line(handler, "", "test.conf"))
        self.assertFalse(store._process_line(handler, "OOB", "test.conf"))
        self.assertFalse(store._process_line(handler, "#", "test.conf"))
        self.assertFalse(store._process_line(handler, "#oob1=programy.oobs.default.DefaultOOB", "test.conf"))

    def test_load_file_contents(self):
        config = FileStorageConfiguration()
        engine = FileStorageEngine(config)
        engine.initialise()
        store = FileOOBStore(engine)

        handler = OOBHandler()

        self.assertEqual(13, store._load_file_contents(handler, os.path.dirname(__file__) + os.sep + "data" + os.sep + "oobs" + os.sep + "callmom.conf"))

    def patch_process_line(self, oob_handler, line, filename):
        raise Exception("Mock Exception")

    @patch("programy.storage.stores.file.store.oobs.FileOOBStore._process_line", patch_process_line)
    def test_load_file_contents_with_exception(self):
        config = FileStorageConfiguration()
        engine = FileStorageEngine(config)
        engine.initialise()
        store = FileOOBStore(engine)

        handler = OOBHandler()

        self.assertEqual(0, store._load_file_contents(handler, os.path.dirname(__file__) + os.sep + "data" + os.sep + "oobs" + os.sep + "callmom.conf"))

    def test_load_oobs(self):
        config = FileStorageConfiguration()
        config._oobs_storage = FileStoreConfiguration(file=os.path.dirname(__file__) + os.sep + "data" + os.sep + "oobs" + os.sep + "callmom.conf", fileformat="text", encoding="utf-8", delete_on_start=False)
        engine = FileStorageEngine(config)
        engine.initialise()
        store = FileOOBStore(engine)

        handler = OOBHandler()

        store.load(handler)

        self.assertIsNotNone(handler.oobs['default'])
        self.assertIsNotNone(handler.oobs['alarm'])
        self.assertIsNotNone(handler.oobs['camera'])

