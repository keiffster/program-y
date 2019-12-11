import os
import os.path
import unittest

from programy.processors.processing import PostQuestionProcessorCollection


class PostQuestionProcessorsStoreAsserts(unittest.TestCase):

    def assert_load(self, store):
        store.empty()

        store.upload_from_file(os.path.dirname(__file__) + os.sep + "data" + os.sep + "processors" + os.sep + "postquestionprocessors.conf")

        collection = PostQuestionProcessorCollection()
        store.load(collection)

        self.assertEqual(1, len(collection.processors))

    def assert_load_exception(self, store):
        store.empty()

        store.upload_from_file(os.path.dirname(__file__) + os.sep + "data" + os.sep + "processors" + os.sep + "postquestionprocessors.conf")

        collection = PostQuestionProcessorCollection()
        store.load(collection)

        self.assertEqual(0, len(collection.processors))

    def assert_upload_from_file(self, store, verbose=False):
        store.empty()

        count, success = store.upload_from_file(os.path.dirname(__file__) + os.sep + "data" + os.sep + "processors" + os.sep + "postquestionprocessors.conf", verbose=verbose)
        self.assertEquals(1, count)
        self.assertEquals(1, success)

    def assert_upload_from_file_exception(self, store):
        store.empty()

        count, success = store.upload_from_file(os.path.dirname(__file__) + os.sep + "data" + os.sep + "processors" + os.sep + "postquestionprocessors.conf")
        self.assertEquals(0, count)
        self.assertEquals(0, success)
