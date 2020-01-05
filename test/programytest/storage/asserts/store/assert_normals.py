import os
import os.path
import re
import unittest
from programy.mappings.normal import NormalCollection
from programy.storage.entities.store import Store


class NormalsStoreAsserts(unittest.TestCase):

    def assert_lookup_storage(self, store):

        store.empty()

        store.add_to_lookup(".uk"," dot uk " )
        store.add_to_lookup(".net"," dot net ")
        store.commit()

        lookups = store.get_lookup()
        self.assertIsNotNone(lookups)
        self.assertEqual(2, len(lookups))

        store.remove_lookup_key(".uk")
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
                                ".uk"," dot uk " 	
                                ".net"," dot net " 	
                                ".ca"," dot ca "	
                                ".de"," dot de "
                                ".jp"," dot jp "
                                ".fr"," dot fr " 
                                ".au"," dot au "
                                ".us"," dot us "
                                ".ru"," dot ru "
                                ".ch"," dot ch "
                                ".it"," dot it "
                                ".nl"," dot nl "
                                ".se"," dot se "
                                ".no"," dot no "
                                ".es"," dot es "                                
                                """)

        collection = NormalCollection()
        store.load(collection)

        self.assertEqual(collection.normalise(".UK"), [re.compile('(^\\.UK|\\.UK|\\.UK$)', re.IGNORECASE), ' DOT UK '])
        self.assertEqual(collection.normalise_string("keiffster.uk"), "keiffster dot uk")

    def assert_upload_from_text_file(self, store):

        store.empty()

        store.upload_from_file(os.path.dirname(__file__) + os.sep + "data" + os.sep + "lookups" + os.sep + "text" + os.sep + "normal.txt")

        collection = NormalCollection()
        store.load(collection)

        self.assertEqual(collection.normalise(".UK"), [re.compile('(^\\.UK|\\.UK|\\.UK$)', re.IGNORECASE), ' DOT UK '])
        self.assertEqual(collection.normalise_string("keiffster.uk"), "keiffster dot uk")

    def assert_upload_csv_file(self, store):

        store.empty()

        store.upload_from_file(os.path.dirname(__file__) + os.sep + "data" + os.sep + "lookups" + os.sep + "csv" + os.sep + "normal.csv", fileformat=Store.CSV_FORMAT)

        collection = NormalCollection()
        store.load(collection)

        self.assertEqual(collection.normalise(".UK"), [re.compile('(^\\.UK|\\.UK|\\.UK$)', re.IGNORECASE), ' DOT UK '])
        self.assertEqual(collection.normalise_string("keiffster.uk"), "keiffster dot uk")
