import unittest
import os
import os.path

from programy.processors.processing import PostQuestionProcessorCollection


class PostQuestionProcessorsStoreAsserts(unittest.TestCase):

    def assert_upload_from_file(self, store):

        store.upload_from_file(os.path.dirname(__file__) + os.sep + "data" + os.sep + "processors" + os.sep + "postquestionprocessors.conf")

        collection = PostQuestionProcessorCollection()
        store.load(collection)

        self.assertEqual(0, len(collection.processors))
