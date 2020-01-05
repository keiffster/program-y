import os
import os.path
import re
import unittest
from programy.mappings.person import PersonCollection
from programy.storage.entities.store import Store


class Person2sStoreAsserts(unittest.TestCase):

    def assert_lookup_storage(self, store):

        store.empty()

        store.add_to_lookup(" I was "," he or she was ")
        store.add_to_lookup(" he was "," I was ")
        store.commit()

        lookups = store.get_lookup()
        self.assertIsNotNone(lookups)
        self.assertEqual(2, len(lookups))

        store.remove_lookup_key(" I was ")
        store.commit()

        lookups = store.get_lookup()
        self.assertIsNotNone(lookups)
        self.assertEqual(1, len(lookups))

        store.remove_lookup()
        store.commit()

        lookup = store.get_lookup()
        self.assertEqual({}, lookup)

    def assert_upload_from_text(self, store):

        store.empty()

        store.upload_from_text(None, """
                        " I was "," he or she was "
                        " he was "," I was "
                        " she was "," I was " 
                        " I am "," he or she is "
                        " I "," he or she " 
                        " me "," him or her "
                        " my "," his or her " 
                        " myself "," him or herself "
                        " mine "," his or hers "
                                """)

        collection = PersonCollection()
        store.load(collection)

        self.assertEqual(collection.person(" I WAS "), [re.compile('(^I WAS | I WAS | I WAS$)', re.IGNORECASE), ' HE OR SHE WAS '])
        self.assertEqual(collection.personalise_string("I was with him"), "he or she was with him")

    def assert_upload_from_text_file(self, store):

        store.empty()

        store.upload_from_file(os.path.dirname(__file__) + os.sep + "data" + os.sep + "lookups" + os.sep + "text" + os.sep + "person2.txt")

        collection = PersonCollection()
        store.load(collection)

        self.assertEqual(collection.person(" I WAS "), [re.compile('(^I WAS | I WAS | I WAS$)', re.IGNORECASE), ' HE OR SHE WAS '])
        self.assertEqual(collection.personalise_string("I was with him"), "he or she was with him")

    def assert_upload_csv_file(self, store):

        store.empty()

        store.upload_from_file(os.path.dirname(__file__) + os.sep + "data" + os.sep + "lookups" + os.sep + "csv" + os.sep + "person2.csv", fileformat=Store.CSV_FORMAT)

        collection = PersonCollection()
        store.load(collection)

        self.assertEqual(collection.person(" I WAS "), [re.compile('(^I WAS | I WAS | I WAS$)', re.IGNORECASE), ' HE OR SHE WAS '])
        self.assertEqual(collection.personalise_string("I was with him"), "he or she was with him")
