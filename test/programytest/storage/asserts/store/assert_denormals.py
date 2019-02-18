import unittest
import re
import os
import os.path

from programy.mappings.denormal import DenormalCollection


class DenormalStoreAsserts(unittest.TestCase):

    def assert_upload_from_file(self, store):

        denormal_collection = DenormalCollection()

        store.upload_from_file(os.path.dirname(__file__) + os.sep + "data" + os.sep + "lookups" + os.sep + "text" + os.sep + "denormal.txt")

        store.load(denormal_collection)

        self.assertEqual(denormal_collection.denormalise(" DOT COM "),
                         [re.compile('(^DOT COM | DOT COM | DOT COM$)', re.IGNORECASE), '.COM'])
        self.assertEqual(denormal_collection.denormalise_string("keith dot com"), "keith.com")
