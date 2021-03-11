import os
import os.path
import unittest
from programy.services.handler import ServiceHandler


class ServicesStoreAsserts(unittest.TestCase):

    def assert_load(self, store):
        store.empty()

        store.upload_from_file(os.path.dirname(__file__) + os.sep + "data" + os.sep + "services" + os.sep + "wikipedia.yaml")

        handler = ServiceHandler()
        store.load(handler)

        self.assertEqual(1, len(handler.services))
        self.assertTrue(handler.services.get("wikipedia"))

    def assert_load_exception(self, store):
        store.empty()

        store.upload_from_file(os.path.dirname(__file__) + os.sep + "data" + os.sep + "services" + os.sep + "wikipedia.yaml")

        handler = ServiceHandler()
        store.load(handler)

        self.assertEqual(0, len(handler.services))
        self.assertFalse(handler.services.get("wikipedia"))

    def assert_upload_from_file(self, store, verbose=False):
        store.empty()

        count, success = store.upload_from_file(os.path.dirname(__file__) + os.sep + "data" + os.sep + "services" + os.sep + "wikipedia.yaml", verbose=verbose)
        self.assertEquals(1, count)
        self.assertEquals(1, success)

    def assert_upload_from_file_exception(self, store):
        store.empty()

        count, success = store.upload_from_file(os.path.dirname(__file__) + os.sep + "data" + os.sep + "services"  + os.sep + "wikipedia.yaml")
        self.assertEquals(0, count)
        self.assertEquals(0, success)
