import os
import unittest

from programy.storage.factory import StorageFactory
from programy.storage.stores.file.config import FileStorageConfiguration
from programy.storage.stores.file.config import FileStoreConfiguration
from programy.storage.stores.file.engine import FileStorageEngine
from programy.triggers.config import TriggerConfiguration
from programy.triggers.manager import TriggerManager
from programy.triggers.local import LocalTriggerManager
from programytest.client import TestClient


class MockLocalTriggerManager(LocalTriggerManager):

    def __init__(self, config, except_on_load=False, except_on_trigger=False):
        LocalTriggerManager.__init__(self, config)
        self._except_on_load = except_on_load
        self._except_on_trigger = except_on_trigger

    def _load_trigger_from_store(self, storage_factory):
        if self._except_on_load:
            raise Exception("Mock Exception")

    def _trigger_trigger(self, trigger, client_context, additional, event):
        if self._except_on_trigger:
            raise Exception("Mock Exception")


class LocalTriggerManagerTests(unittest.TestCase):

    def test_load_triggers(self):
        config = TriggerConfiguration()
        config._manager = TriggerConfiguration.LOCAL_MANAGER

        mgr = TriggerManager.load_trigger_manager(config)

        trigger_file = os.path.dirname(__file__)  + os.sep + "triggers.txt"
        self.assertTrue(os.path.exists(trigger_file))

        config = FileStorageConfiguration()
        config._triggers_storage = FileStoreConfiguration(file=trigger_file, fileformat="text", encoding="utf-8", delete_on_start=False)
        engine = FileStorageEngine(config)
        engine.initialise()

        storage_factory = StorageFactory()

        storage_factory._storage_engines[StorageFactory.TRIGGERS] = engine
        storage_factory._store_to_engine_map[StorageFactory.TRIGGERS] = engine

        mgr.load_triggers(storage_factory)

        triggers = mgr.get_triggers("SYSTEM_STARTUP")
        self.assertIsNotNone(triggers)
        self.assertEqual(2, len(triggers))

        triggers = mgr.get_triggers("SYSTEM_SHUTDOWN")
        self.assertIsNotNone(triggers)
        self.assertEqual(1, len(triggers))

        triggers = mgr.get_triggers("CONVERSATION_START")
        self.assertIsNotNone(triggers)
        self.assertEqual(1, len(triggers))

        triggers = mgr.get_triggers("OTHER")
        self.assertEquals([], triggers)

        self.assertTrue("SYSTEM_STARTUP" in mgr.triggers)
        self.assertTrue("SYSTEM_SHUTDOWN" in mgr.triggers)
        self.assertTrue("CONVERSATION_START" in mgr.triggers)

        mgr.empty()

        self.assertFalse("SYSTEM_STARTUP" in mgr.triggers)
        self.assertFalse("SYSTEM_SHUTDOWN" in mgr.triggers)
        self.assertFalse("CONVERSATION_START" in mgr.triggers)

    def test_load_triggers_no_engine(self):
        config = TriggerConfiguration()
        config._manager = TriggerConfiguration.LOCAL_MANAGER

        mgr = TriggerManager.load_trigger_manager(config)

        trigger_file = os.path.dirname(__file__)  + os.sep + "triggers.txt"
        self.assertTrue(os.path.exists(trigger_file))

        config = FileStorageConfiguration()
        config._triggers_storage = FileStoreConfiguration(file=trigger_file, fileformat="text", encoding="utf-8", delete_on_start=False)
        engine = FileStorageEngine(config)
        engine.initialise()

        storage_factory = StorageFactory()

        mgr.load_triggers(storage_factory)

        self.assertFalse("SYSTEM_STARTUP" in mgr.triggers)
        self.assertFalse("SYSTEM_SHUTDOWN" in mgr.triggers)
        self.assertFalse("CONVERSATION_START" in mgr.triggers)

    def test_load_triggers_bad_triggers(self):
        config = TriggerConfiguration()
        config._manager = TriggerConfiguration.LOCAL_MANAGER

        mgr = TriggerManager.load_trigger_manager(config)

        trigger_file = os.path.dirname(__file__)  + os.sep + "bad_triggers.txt"
        self.assertTrue(os.path.exists(trigger_file))

        config = FileStorageConfiguration()
        config._triggers_storage = FileStoreConfiguration(file=trigger_file, fileformat="text", encoding="utf-8", delete_on_start=False)
        engine = FileStorageEngine(config)
        engine.initialise()

        storage_factory = StorageFactory()

        storage_factory._storage_engines[StorageFactory.TRIGGERS] = engine
        storage_factory._store_to_engine_map[StorageFactory.TRIGGERS] = engine

        mgr.load_triggers(storage_factory)

    def test_add_trigger(self):
        config = TriggerConfiguration()
        config._manager = TriggerConfiguration.LOCAL_MANAGER

        mgr = TriggerManager.load_trigger_manager(config)
        self.assertIsNotNone(mgr)

        mgr.add_trigger("SYSTEM_STARTUP", "programytest.triggers.trigger1.Trigger1")

        self.assertTrue("SYSTEM_STARTUP" in mgr.triggers)

    def test_add_triggers(self):
        config = TriggerConfiguration()
        config._manager = TriggerConfiguration.LOCAL_MANAGER

        mgr = TriggerManager.load_trigger_manager(config)
        self.assertIsNotNone(mgr)

        mgr.add_triggers({
            "SYSTEM_STARTUP": "programytest.triggers.trigger1.Trigger1",
            "SYSTEM_SHUTDOWN": "programytest.triggers.trigger1.Trigger1",
            "CONVERSATION_START": "programytest.triggers.trigger1.Trigger1"
        })

        self.assertTrue("SYSTEM_STARTUP" in mgr.triggers)
        self.assertTrue("SYSTEM_SHUTDOWN" in mgr.triggers)
        self.assertTrue("CONVERSATION_START" in mgr.triggers)

    def test_trigger_triggers(self):
        config = TriggerConfiguration()
        config._manager = TriggerConfiguration.LOCAL_MANAGER

        mgr = TriggerManager.load_trigger_manager(config)

        trigger_file = os.path.dirname(__file__)  + os.sep + "triggers.txt"

        config = FileStorageConfiguration()
        config._triggers_storage = FileStoreConfiguration(file=trigger_file, fileformat="text", encoding="utf-8", delete_on_start=False)
        engine = FileStorageEngine(config)
        engine.initialise()

        storage_factory = StorageFactory()

        storage_factory._storage_engines[StorageFactory.TRIGGERS] = engine
        storage_factory._store_to_engine_map[StorageFactory.TRIGGERS] = engine

        mgr.load_triggers(storage_factory)

        client = TestClient()
        client_context = client.create_client_context("testid")

        triggered = mgr.trigger("SYSTEM_STARTUP")
        self.assertTrue(triggered)

        triggered = mgr.trigger("SYSTEM_STARTUP", additional={"key": "value"})
        self.assertTrue(triggered)

        triggered = mgr.trigger("SYSTEM_STARTUP", additional={"event": "SYSTEM_STARTUP"})
        self.assertTrue(triggered)

        triggered = mgr.trigger("CONVERSATION_START", client_context)
        self.assertTrue(triggered)

        triggered = mgr.trigger("OTHER_EVENT")
        self.assertFalse(triggered)

        triggered = mgr.trigger("OTHER_EVENT", client_context)
        self.assertFalse(triggered)

        triggered = mgr.trigger("OTHER_EVENT", client_context, additional={"key": "value"})
        self.assertFalse(triggered)

    def test_trigger_exception(self):
        config = TriggerConfiguration()
        config._manager = TriggerConfiguration.LOCAL_MANAGER

        mgr = TriggerManager.load_trigger_manager(config)
        self.assertIsNotNone(mgr)

        mgr.add_trigger("SYSTEM_STARTUP", "programy.triggers.excepter.ExceptionTrigger")

        triggered = mgr.trigger("SYSTEM_STARTUP")
        self.assertTrue(triggered)

    def test_local_trigger_mgr_except_on_load(self):
        config = TriggerConfiguration()
        config._manager = TriggerConfiguration.LOCAL_MANAGER

        mgr = MockLocalTriggerManager(config, except_on_load=True)

        trigger_file = os.path.dirname(__file__)  + os.sep + "triggers.txt"
        self.assertTrue(os.path.exists(trigger_file))

        config = FileStorageConfiguration()
        config._triggers_storage = FileStoreConfiguration(file=trigger_file, fileformat="text", encoding="utf-8", delete_on_start=False)
        engine = FileStorageEngine(config)
        engine.initialise()

        storage_factory = StorageFactory()

        storage_factory._storage_engines[StorageFactory.TRIGGERS] = engine
        storage_factory._store_to_engine_map[StorageFactory.TRIGGERS] = engine

        mgr.load_triggers(storage_factory)

        self.assertFalse("SYSTEM_STARTUP" in mgr.triggers)
        self.assertFalse("SYSTEM_SHUTDOWN" in mgr.triggers)
        self.assertFalse("CONVERSATION_START" in mgr.triggers)

    def test_local_trigger_mgr_except_on_trigger(self):
        config = TriggerConfiguration()
        config._manager = TriggerConfiguration.LOCAL_MANAGER

        mgr = MockLocalTriggerManager(config, except_on_trigger=True)

        trigger_file = os.path.dirname(__file__)  + os.sep + "triggers.txt"
        self.assertTrue(os.path.exists(trigger_file))

        config = FileStorageConfiguration()
        config._triggers_storage = FileStoreConfiguration(file=trigger_file, fileformat="text", encoding="utf-8", delete_on_start=False)
        engine = FileStorageEngine(config)
        engine.initialise()

        storage_factory = StorageFactory()

        storage_factory._storage_engines[StorageFactory.TRIGGERS] = engine
        storage_factory._store_to_engine_map[StorageFactory.TRIGGERS] = engine

        mgr.load_triggers(storage_factory)

        triggered = mgr.trigger("SYSTEM_STARTUP")
        self.assertFalse(triggered)

    def test_local_trigger_mgr_no_additionals(self):
        config = TriggerConfiguration()
        config._manager = TriggerConfiguration.LOCAL_MANAGER

        mgr = TriggerManager.load_trigger_manager(config)

        trigger_file = os.path.dirname(__file__)  + os.sep + "triggers.txt"
        self.assertTrue(os.path.exists(trigger_file))

        config = FileStorageConfiguration()
        config._triggers_storage = FileStoreConfiguration(file=trigger_file, fileformat="text", encoding="utf-8", delete_on_start=False)
        engine = FileStorageEngine(config)
        engine.initialise()

        storage_factory = StorageFactory()

        storage_factory._storage_engines[StorageFactory.TRIGGERS] = engine
        storage_factory._store_to_engine_map[StorageFactory.TRIGGERS] = engine

        mgr.load_triggers(storage_factory)

        mgr.trigger("SYSTEM_STARTUP")

    def test_local_trigger_mgr_with_additionals_no_event(self):
        config = TriggerConfiguration()
        config._manager = TriggerConfiguration.LOCAL_MANAGER

        mgr = TriggerManager.load_trigger_manager(config)

        trigger_file = os.path.dirname(__file__)  + os.sep + "triggers.txt"
        self.assertTrue(os.path.exists(trigger_file))

        config = FileStorageConfiguration()
        config._triggers_storage = FileStoreConfiguration(file=trigger_file, fileformat="text", encoding="utf-8", delete_on_start=False)
        engine = FileStorageEngine(config)
        engine.initialise()

        storage_factory = StorageFactory()

        storage_factory._storage_engines[StorageFactory.TRIGGERS] = engine
        storage_factory._store_to_engine_map[StorageFactory.TRIGGERS] = engine

        mgr.load_triggers(storage_factory)

        self.assertTrue(mgr.trigger("SYSTEM_STARTUP", additional={}))

    def test_local_trigger_mgr_with_additionals_with_event(self):
        config = TriggerConfiguration()
        config._manager = TriggerConfiguration.LOCAL_MANAGER

        mgr = TriggerManager.load_trigger_manager(config)

        trigger_file = os.path.dirname(__file__)  + os.sep + "triggers.txt"
        self.assertTrue(os.path.exists(trigger_file))

        config = FileStorageConfiguration()
        config._triggers_storage = FileStoreConfiguration(file=trigger_file, fileformat="text", encoding="utf-8", delete_on_start=False)
        engine = FileStorageEngine(config)
        engine.initialise()

        storage_factory = StorageFactory()

        storage_factory._storage_engines[StorageFactory.TRIGGERS] = engine
        storage_factory._store_to_engine_map[StorageFactory.TRIGGERS] = engine

        mgr.load_triggers(storage_factory)

        self.assertTrue(mgr.trigger("SYSTEM_STARTUP", additional={'event': "SYSTEM_STARTUP"}))
