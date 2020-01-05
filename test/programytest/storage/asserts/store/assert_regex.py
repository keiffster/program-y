import os
import os.path
import re
import unittest

from programy.mappings.properties import RegexTemplatesCollection


class RegexStoreAsserts(unittest.TestCase):

    def assert_regexes_storage(self, store):
        store.empty()

        defaults = {"anything": "^.*$",
                    "anytext": "^.+$",
                    "anyinteger": "^\d+$",
                    "anydecimal": "^\d+\.\d+$",
                    "anynumber": "^[\d+\.\d+$]|[\d+]$"
                    }
        store.add_regexes(defaults)
        store.commit()

        new_regexes = store.get_regexes()
        self.assertTrue("anything" in new_regexes)
        self.assertEqual("^.*$", new_regexes["anything"])
        self.assertTrue("anytext" in new_regexes)
        self.assertEqual("^.+$", new_regexes["anytext"])

        store.empty()
        new_regexes = store.get_regexes()
        self.assertEqual(0, len(new_regexes.keys()))

    def assert_regex_storage(self, store):
        store.empty()

        store.add_regex("anything", "^.*$")

        new_regexes = store.get_regexes()

        self.assertTrue("anything" in new_regexes)
        self.assertEqual("^.*$", new_regexes["anything"])
        self.assertFalse("anytext" in new_regexes)

        store.add_regex("anytext", "^.+$")
        store.commit()

        new_regexes = store.get_regexes()
        self.assertTrue("anything" in new_regexes)
        self.assertEqual("^.*$", new_regexes["anything"])
        self.assertTrue("anytext" in new_regexes)
        self.assertEqual("^.+$", new_regexes["anytext"])
        self.assertFalse("anyinteger" in new_regexes)

    def assert_empty_regexes(self, store):
        store.empty()

        store.add_regex("anything", "^.*$")
        store.commit()

        store.add_regex("anytext", "^.+$")
        store.commit()

        new_regexes = store.get_regexes()
        self.assertTrue("anything" in new_regexes)
        self.assertEqual("^.*$", new_regexes["anything"])
        new_regexes = store.get_regexes()
        self.assertTrue("anytext" in new_regexes)
        self.assertEqual("^.+$", new_regexes["anytext"])

        store.empty()

        new_regexes = store.get_regexes()
        self.assertFalse("name1" in new_regexes)

    def assert_upload_from_file(self, store):
        store.empty()

        store.upload_from_file(os.path.dirname(__file__) + os.sep + "data" + os.sep + "lookups" + os.sep + "text" + os.sep + "regex-templates.txt")
        store.commit()

        collection = RegexTemplatesCollection()
        store.load(collection)

        self.assertTrue(collection.has_regex("anything"))
        self.assertEqual(re.compile('^.*$', re.IGNORECASE), collection.regex("anything"))
        self.assertTrue(collection.has_regex("legion"))
        self.assertFalse(collection.has_regex("XXXXX"))

    def assert_add_to_collection(self, store):
        store.empty()

        collection = RegexTemplatesCollection()

        store.add_to_collection(collection, "anything", '^.*$')

        self.assertTrue(collection.has_regex("anything"))
        self.assertEqual(re.compile('^.*$', re.IGNORECASE), collection.regex("anything"))

    def assert_add_to_collection_collection(self, store):
        store.empty()

        collection = RegexTemplatesCollection()

        store.add_to_collection(collection, "anything", '^.*$')
