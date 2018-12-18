import unittest
import os
import os.path
import re

from programy.mappings.person import PersonCollection


class PersonssStoreAsserts(unittest.TestCase):

    def assert_upload_from_file(self, store):
        person_collection = PersonCollection()

        store.upload_from_file(os.path.dirname(
            __file__) + os.sep + "data" + os.sep + "lookups" + os.sep + "text" + os.sep + "person.txt")

        store.load(person_collection)

        self.assertEqual(person_collection.person(" WITH YOU "),
                         [re.compile('(^WITH YOU | WITH YOU | WITH YOU$)', re.IGNORECASE), ' WITH ME2 '])
        self.assertEqual(person_collection.personalise_string("Is he with you"), "Is he with me2")
