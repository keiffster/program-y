import unittest
import re
import os
import os.path

from programy.mappings.person import PersonCollection


class Person2sStoreAsserts(unittest.TestCase):

    def assert_upload_from_file(self, store):
        person2_collection = PersonCollection()

        store.upload_from_file(os.path.dirname(__file__) + os.sep + "data" + os.sep + "lookups" + os.sep + "text" + os.sep + "person2.txt")

        store.load(person2_collection)

        self.assertEqual(person2_collection.person(" I WAS "),
                         [re.compile('(^I WAS | I WAS | I WAS$)', re.IGNORECASE), ' HE OR SHE WAS '])
        self.assertEqual(person2_collection.personalise_string("I was there"), "he or she was there")
