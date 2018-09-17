import unittest
import os
import os.path

from programy.processors.processing import ProcessorCollection


class PreProcessorsStoreAsserts(unittest.TestCase):

    def assert_upload_from_file(self, store):

        store.upload_from_file(os.path.dirname(__file__) + os.sep + "data" + os.sep + "processors" + os.sep + "preprocessors.conf")

        collection = ProcessorCollection()
        store.load(collection)

        self.assertEqual(2, len(collection.processors))
