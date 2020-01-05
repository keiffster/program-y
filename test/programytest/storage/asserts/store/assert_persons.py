import os
import os.path
import re
import unittest
from programy.mappings.person import PersonCollection
from programy.storage.entities.store import Store


class PersonsStoreAsserts(unittest.TestCase):

    def assert_lookup_storage(self, store):

        store.empty()

        store.add_to_lookup(" with you "," with me2 ")
        store.add_to_lookup(" with me "," with you2 ")
        store.commit()

        lookups = store.get_lookup()
        self.assertIsNotNone(lookups)
        self.assertEqual(2, len(lookups.keys()))

        store.remove_lookup_key(" with me ")
        store.commit()

        lookups = store.get_lookup()
        self.assertIsNotNone(lookups)
        self.assertEqual(1, len(lookups.keys()))

        store.remove_lookup()
        store.commit()

        lookup = store.get_lookup()
        self.assertEqual({}, lookup)

    def assert_upload_from_text(self, store):

        store.empty()

        store.upload_from_text(None, """
                            " with you "," with me2 " 
                            " with me "," with you2 "
                            " to you "," to me2 " 
                            " to me "," to you2 "
                            " of you "," of me2 " 
                            " of me "," of you2 "
                            " for you "," for me2 " 
                            " for me "," for you2 "
                            " give you "," give me2 " 
                            " give me "," give you2 "
                                """)

        collection = PersonCollection()
        store.load(collection)

        self.assertEqual(collection.person(" WITH YOU "), [re.compile('(^WITH YOU | WITH YOU | WITH YOU$)', re.IGNORECASE), ' WITH ME2 '])
        self.assertEqual(collection.personalise_string("This is with you "), "This is with me2")

    def assert_upload_from_text_file(self, store):

        store.empty()

        store.upload_from_file(os.path.dirname(__file__) + os.sep + "data" + os.sep + "lookups" + os.sep + "text" + os.sep + "person.txt")

        collection = PersonCollection()
        store.load(collection)

        self.assertEqual(collection.person(" WITH YOU "), [re.compile('(^WITH YOU | WITH YOU | WITH YOU$)', re.IGNORECASE), ' WITH ME2 '])
        self.assertEqual(collection.personalise_string("This is with you "), "This is with me2")

    def assert_upload_csv_file(self, store):

        store.empty()

        store.upload_from_file(os.path.dirname(__file__) + os.sep + "data" + os.sep + "lookups" + os.sep + "csv" + os.sep + "person.csv", fileformat=Store.CSV_FORMAT)

        collection = PersonCollection()
        store.load(collection)

        self.assertEqual(collection.person(" WITH YOU "), [re.compile('(^WITH YOU | WITH YOU | WITH YOU$)', re.IGNORECASE), ' WITH ME2 '])
        self.assertEqual(collection.personalise_string("This is with you "), "This is with me2")
