import os
import os.path
import unittest
from programy.oob.handler import OOBHandler


class OOBsStoreAsserts(unittest.TestCase):

    def assert_load(self, store):
        store.empty()

        store.upload_from_file(os.path.dirname(__file__) + os.sep + "data" + os.sep + "oobs" + os.sep + "callmom.conf")

        handler = OOBHandler()
        store.load(handler)

        self.assertEqual(12, len(handler.oobs))
        self.assertTrue(handler.oobs.get("dial"))

    def assert_load_exception(self, store):
        store.empty()

        store.upload_from_file(os.path.dirname(__file__) + os.sep + "data" + os.sep + "oobs" + os.sep + "callmom.conf")

        handler = OOBHandler()
        store.load(handler)

        self.assertEqual(0, len(handler.oobs))
        self.assertFalse(handler.oobs.get("dial"))

    def assert_upload_from_file(self, store, verbose=False):
        store.empty()

        count, success = store.upload_from_file(os.path.dirname(__file__) + os.sep + "data" + os.sep + "oobs" + os.sep + "callmom.conf", verbose=verbose)
        self.assertEquals(13, count)
        self.assertEquals(13, success)

    def assert_upload_from_file_exception(self, store):
        store.empty()

        count, success = store.upload_from_file(os.path.dirname(__file__) + os.sep + "data" + os.sep + "oobs" + os.sep + "callmom.conf")
        self.assertEquals(0, count)
        self.assertEquals(0, success)
