import unittest
from programy.mappings.properties import DefaultVariablesCollection


class DefaultVariablesTests(unittest.TestCase):

    def test_initialise_collection(self):
        collection = DefaultVariablesCollection()
        self.assertIsNotNone(collection)

    def test_properties_operations(self):
        collection = DefaultVariablesCollection()
        self.assertIsNotNone(collection)

        collection.add_variable("name", "KeiffBot 1.0")
        collection.add_variable("firstname", "Keiff")
        collection.add_variable("middlename", "AIML")
        collection.add_variable("lastname", "BoT")
        collection.add_variable("fullname", "KeiffBot")

        self.assertTrue(collection.has_property("name"))
        self.assertFalse(collection.has_property("age"))

        self.assertEqual("KeiffBot 1.0", collection.variable("name"))
        self.assertIsNone(collection.variable("age"))