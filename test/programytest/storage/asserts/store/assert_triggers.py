import os
import os.path
import unittest
from programy.triggers.local import LocalTriggerManager
from programy.triggers.config import TriggerConfiguration


class TriggersStoreAsserts(unittest.TestCase):

    def assert_load(self, store):
        store.empty()

        store.upload_from_file(os.path.dirname(__file__) + os.sep + "data" + os.sep + "triggers" + os.sep + "triggers.txt")

        handler = LocalTriggerManager(TriggerConfiguration())
        store.load(handler)

        self.assertEqual(3, len(handler.triggers))
        self.assertTrue(handler.triggers.get("CONVERSATION_START"))

    def assert_load_exception(self, store):
        store.empty()

        store.upload_from_file(os.path.dirname(__file__) + os.sep + "data" + os.sep + "triggers" + os.sep + "triggers.txt")

        handler = LocalTriggerManager(TriggerConfiguration())
        store.load(handler)

        self.assertEqual(0, len(handler.triggers))
        self.assertFalse(handler.triggers.get("CONVERSATION_START"))

    def assert_upload_from_file(self, store, verbose=False):
        store.empty()

        count, success = store.upload_from_file(os.path.dirname(__file__) + os.sep + "data" + os.sep + "triggers" + os.sep + "triggers.txt", verbose=verbose)
        self.assertEquals(4, count)
        self.assertEquals(4, success)

    def assert_upload_from_file_exception(self, store):
        store.empty()

        count, success = store.upload_from_file(os.path.dirname(__file__) + os.sep + "data" + os.sep + "triggers" + os.sep + "triggers.txt")
        self.assertEquals(0, count)
        self.assertEquals(0, success)
