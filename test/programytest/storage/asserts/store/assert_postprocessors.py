import os
import os.path
import unittest

from programy.processors.processing import PostProcessorCollection


class PostProcessorsStoreAsserts(unittest.TestCase):

    def assert_load(self, store):
        store.empty()

        store.upload_from_file(os.path.dirname(__file__) + os.sep + "data" + os.sep + "processors" + os.sep + "postprocessors.conf")

        collection = PostProcessorCollection()
        store.load(collection)

        self.assertEqual(5, len(collection.processors))

    def assert_load_exception(self, store):
        store.empty()

        store.upload_from_file(os.path.dirname(__file__) + os.sep + "data" + os.sep + "processors" + os.sep + "postprocessors.conf")

        collection = PostProcessorCollection()
        store.load(collection)

        self.assertEqual(0, len(collection.processors))

    def assert_upload_from_file(self, store, verbose=False):
        store.empty()

        count, success = store.upload_from_file(os.path.dirname(__file__) + os.sep + "data" + os.sep + "processors" + os.sep + "postprocessors.conf", verbose=verbose)
        self.assertEquals(6, count)
        self.assertEquals(5, success)

    def assert_upload_from_file_exception(self, store):
        store.empty()

        count, success = store.upload_from_file(os.path.dirname(__file__) + os.sep + "data" + os.sep + "processors" + os.sep + "postprocessors.conf")
        self.assertEquals(0, count)
        self.assertEquals(0, success)
