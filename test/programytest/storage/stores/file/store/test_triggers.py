import os
import os.path
import unittest
from unittest.mock import patch
from programy.storage.stores.file.config import FileStorageConfiguration
from programy.storage.stores.file.config import FileStoreConfiguration
from programy.storage.stores.file.engine import FileStorageEngine
from programy.storage.stores.file.store.triggers import FileTriggersStore
from programy.triggers.config import TriggerConfiguration
from programy.triggers.manager import TriggerManager


class FileTriggersStoreTests(unittest.TestCase):

    def test_initialise(self):
        config = FileStorageConfiguration()
        engine = FileStorageEngine(config)
        engine.initialise()
        store = FileTriggersStore(engine)
        self.assertEqual(store.storage_engine, engine)

    def test_storage_path(self):
        config = FileStorageConfiguration()
        engine = FileStorageEngine(config)
        engine.initialise()
        store = FileTriggersStore(engine)

        self.assertEquals('/tmp/triggers/triggers.txt', store._get_storage_path())
        self.assertIsInstance(store.get_storage(), FileStoreConfiguration)

    def test_process_line(self):
        config = FileStorageConfiguration()
        engine = FileStorageEngine(config)
        engine.initialise()
        store = FileTriggersStore(engine)

        trigger_config = TriggerConfiguration()
        trigger_config._manager = TriggerConfiguration.LOCAL_MANAGER
        mgr = TriggerManager.load_trigger_manager(trigger_config)

        self.assertFalse(store._process_line("", mgr))
        self.assertFalse(store._process_line("TRIGGER1", mgr))
        self.assertFalse(store._process_line("#", mgr))
        self.assertFalse(store._process_line("#TRIGGER1:programy.triggers.null.NullTrigger", mgr))

    def test_load_file_contents(self):
        config = FileStorageConfiguration()
        engine = FileStorageEngine(config)
        engine.initialise()
        store = FileTriggersStore(engine)

        trigger_config = TriggerConfiguration()
        trigger_config._manager = TriggerConfiguration.LOCAL_MANAGER
        mgr = TriggerManager.load_trigger_manager(trigger_config)

        self.assertTrue(store._load_file_contents(mgr, os.path.dirname(__file__) + os.sep + "data" + os.sep + "triggers" + os.sep + "triggers.txt"))

    def patch_load_triggers_from_file(self, filename, collection):
        raise Exception("Mock Exception")

    @patch("programy.storage.stores.file.store.triggers.FileTriggersStore._load_triggers_from_file", patch_load_triggers_from_file)
    def test_load_file_contents_with_exception(self):
        config = FileStorageConfiguration()
        engine = FileStorageEngine(config)
        engine.initialise()
        store = FileTriggersStore(engine)

        trigger_config = TriggerConfiguration()
        trigger_config._manager = TriggerConfiguration.LOCAL_MANAGER
        mgr = TriggerManager.load_trigger_manager(trigger_config)

        self.assertFalse(store._load_file_contents(os.path.dirname(__file__) + os.sep + "data" + os.sep + "triggers" + os.sep + "triggers.txt", mgr))

    def test_load_triggers(self):
        config = FileStorageConfiguration()
        config._triggers_storage = FileStoreConfiguration(file=os.path.dirname(__file__) + os.sep + "data" + os.sep + "triggers" + os.sep + "triggers.txt", fileformat="text", encoding="utf-8", delete_on_start=False)
        engine = FileStorageEngine(config)
        engine.initialise()
        store = FileTriggersStore(engine)

        trigger_config = TriggerConfiguration()
        trigger_config._manager = TriggerConfiguration.LOCAL_MANAGER

        mgr = TriggerManager.load_trigger_manager(trigger_config)
        store.load(mgr)

        self.assertTrue(mgr.has_trigger_event("TRIGGER1"))
        self.assertTrue(mgr.has_trigger_event("TRIGGER2"))
        self.assertTrue(mgr.has_trigger_event("TRIGGER3"))
        self.assertFalse(mgr.has_trigger_event("TRIGGER4"))
