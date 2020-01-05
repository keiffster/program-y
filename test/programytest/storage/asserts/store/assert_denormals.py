import os
import os.path
import re
import unittest
from programy.mappings.denormal import DenormalCollection
from programy.storage.entities.store import Store


class DenormalStoreAsserts(unittest.TestCase):

    def assert_lookup_storage(self, store):

        store.empty()

        store.add_to_lookup(" dot com ",".com")
        store.add_to_lookup(" dot org ",".org")
        store.commit()

        lookups = store.get_lookup()
        self.assertIsNotNone(lookups)
        self.assertEqual(2, len(lookups))

        store.remove_lookup_key(" dot com ")
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
                                " dot uk ",".uk"
                                " dot net ",".net"
                                " dot ca ",".ca"
                                " dot de ",".de"
                                " dot jp ",".jp"
                                " dot fr ",".fr"
                                " dot au ",".au"
                                " dot us ",".us"
                                " dot ru ",".ru"
                                " dot ch ",".ch"
                                " dot it ",".it"
                                " dot nl ",".nl"
                                " dot se ",".se"
                                " dot no ",".no"
                                " dot es ",".es"
                                """)

        collection = DenormalCollection()
        store.load(collection)

        self.assertEqual(collection.denormalise(" DOT UK "), [re.compile('(^DOT UK | DOT UK | DOT UK$)', re.IGNORECASE), '.UK'])
        self.assertEqual(collection.denormalise_string("keiffster DOT UK"), "keiffster.uk")

    def assert_upload_from_text_file(self, store):

        store.empty()

        store.upload_from_file(os.path.dirname(__file__) + os.sep + "data" + os.sep + "lookups" + os.sep + "text" + os.sep + "denormal.txt")

        collection = DenormalCollection()
        store.load(collection)

        self.assertEqual(collection.denormalise(" DOT UK "), [re.compile('(^DOT UK | DOT UK | DOT UK$)', re.IGNORECASE), '.UK'])
        self.assertEqual(collection.denormalise_string("keiffster DOT UK"), "keiffster.uk")

    def assert_upload_csv_file(self, store):

        store.empty()

        store.upload_from_file(os.path.dirname(__file__) + os.sep + "data" + os.sep + "lookups" + os.sep + "csv" + os.sep + "denormal.csv",  fileformat=Store.CSV_FORMAT)

        collection = DenormalCollection()
        store.load(collection)

        self.assertEqual(collection.denormalise(" DOT UK "), [re.compile('(^DOT UK | DOT UK | DOT UK$)', re.IGNORECASE), '.UK'])
        self.assertEqual(collection.denormalise_string("keiffster DOT UK"), "keiffster.uk")
