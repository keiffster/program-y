import unittest
import re

from programy.mappings.gender import GenderCollection
from programy.storage.entities.store import Store


class LookupStoreAsserts(unittest.TestCase):

    def assert_lookup_storage(self, store):

        store.empty()

        store.add_to_lookup("GENDER", " with him ", " with her ")
        store.add_to_lookup("GENDER", " with her ", " with him ")
        store.commit()

        lookups = store.get_lookup("GENDER")
        self.assertIsNotNone(lookups)
        self.assertEquals(2, len(lookups))

        store.remove_lookup_key("GENDER", " with him ")
        store.commit()

        lookups = store.get_lookup("GENDER")
        self.assertIsNotNone(lookups)
        self.assertEquals(1, len(lookups))

        store.remove_lookup("GENDER")
        store.commit()

        lookup = store.get_lookup("GENDER")
        self.assertIsNone(lookup)

    def assert_upload_from_text(self, store):

        store.empty()

        store.upload_from_text("GENDER", """
                                " with him "," with her "
                                " with her "," with him "
                                " to him "," to her "
                                " to her "," to him "
                                " on him "," on her "
                                " on her "," on him "
                                " in him "," in her "
                                " in her "," in him "
                                " for him "," for her "
                                " for her "," for him "
                                " he "," she "
                                " his "," her "
                                " him "," her "
                                " her "," his "
                                " she "," he "
                                """)

        collection = GenderCollection()
        store.load(collection, 'GENDER')

        self.assertEquals(collection.gender(" WITH HIM "), [re.compile('(^WITH HIM | WITH HIM | WITH HIM$)', re.IGNORECASE), ' WITH HER '])
        self.assertEqual(collection.genderise_string("This is with him "), "This is WITH HER")

    def assert_upload_from_text_file(self, store, filename):

        store.empty()

        store.upload_from_file(filename)

        collection = GenderCollection()
        store.load(collection, 'GENDER')

        self.assertEquals(collection.gender(" WITH HIM "), [re.compile('(^WITH HIM | WITH HIM | WITH HIM$)', re.IGNORECASE), ' WITH HER '])
        self.assertEqual(collection.genderise_string("This is with him "), "This is WITH HER")

    def assert_upload_csv_file(self, store, filename):

        store.empty()

        store.upload_from_file(filename, format=Store.CSV_FORMAT)

        collection = GenderCollection()
        store.load(collection, 'GENDER')

        self.assertEquals(collection.gender(" WITH HIM "), [re.compile('(^WITH HIM | WITH HIM | WITH HIM$)', re.IGNORECASE), ' WITH HER '])
        self.assertEqual(collection.genderise_string("This is with him "), "This is WITH HER")
