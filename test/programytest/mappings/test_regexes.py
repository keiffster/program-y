import unittest
from programy.mappings.properties import RegexTemplatesCollection


class RegexTests(unittest.TestCase):

    def test_initialise_collection(self):
        collection = RegexTemplatesCollection()
        self.assertIsNotNone(collection)

    def test_properties_operations(self):
        collection = RegexTemplatesCollection()
        self.assertIsNotNone(collection)

        collection.add_regex("name", ".*")

        self.assertTrue(collection.has_regex("name"))

        self.assertEqual(".*", collection.regex("name"))
