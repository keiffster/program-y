import unittest
import re
import os
import os.path

from programy.mappings.normal import NormalCollection


class NormalsStoreAsserts(unittest.TestCase):

    def assert_upload_from_file(self, store):
        normal_collection = NormalCollection()

        store.upload_from_file(os.path.dirname(__file__) + os.sep + "data" + os.sep + "lookups" + os.sep + "text" + os.sep + "normal.txt")

        store.load(normal_collection)

        self.assertEqual(normal_collection.normalise(".COM"),
                         [re.compile('(^\\.COM|\\.COM|\\.COM$)', re.IGNORECASE), ' DOT COM '])
        self.assertEqual(normal_collection.normalise_string("keith.com"), "keith dot com")
