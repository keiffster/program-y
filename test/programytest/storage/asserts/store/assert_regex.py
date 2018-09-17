import unittest
import re
import os
import os.path

from programy.mappings.properties import RegexTemplatesCollection


class RegexStoreAsserts(unittest.TestCase):

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
