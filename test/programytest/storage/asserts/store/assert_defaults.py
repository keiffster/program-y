import unittest
import os
import os.path

from programy.mappings.properties import DefaultVariablesCollection


class DefaultStoreAsserts(unittest.TestCase):

    def assert_defaults_storage(self, store):

        store.empty()

        defaults = {"name1": "val1", "name2": "val2", "name3": "val3"}
        store.add_defaults(defaults)
        store.commit()

        new_defaults = store.get_default_values()
        self.assertTrue("name1" in new_defaults)
        self.assertEqual("val1", new_defaults["name1"])
        self.assertTrue("name2" in new_defaults)
        self.assertEqual("val2", new_defaults["name2"])
        self.assertTrue("name3" in new_defaults)
        self.assertEqual("val3", new_defaults["name3"])
        self.assertFalse("name4" in new_defaults)

        store.empty()
        new_defaults = store.get_default_values()
        self.assertEqual(0, len(new_defaults.keys()))

    def assert_default_storage(self, store):

        store.empty()

        store.add_default("name1", "val1")

        new_defaults = store.get_default_values()

        self.assertTrue("name1" in new_defaults)
        self.assertEqual("val1", new_defaults["name1"])
        self.assertFalse("name2" in new_defaults)

        store.add_default("name2", "val2")
        store.commit()

        new_defaults = store.get_default_values()
        self.assertTrue("name1" in new_defaults)
        self.assertEqual("val1", new_defaults["name1"])
        self.assertTrue("name2" in new_defaults)
        self.assertEqual("val2", new_defaults["name2"])
        self.assertFalse("name3" in new_defaults)

    def assert_empty_defaults(self, store):

        store.empty()

        store.add_default("name1", "val1")
        store.commit()

        store.add_default("name2", "val2")
        store.commit()

        new_defaults = store.get_default_values()
        self.assertTrue("name1" in new_defaults)
        self.assertEqual("val1", new_defaults["name1"])
        new_defaults = store.get_default_values()
        self.assertTrue("name2" in new_defaults)
        self.assertEqual("val2", new_defaults["name2"])

        store.empty()

        new_defaults = store.get_default_values()
        self.assertFalse("name1" in new_defaults)

    def assert_upload_from_file(self, store):
        
        store.empty()
        
        default_collection = DefaultVariablesCollection()

        store.upload_from_file(os.path.dirname(__file__) + os.sep + "data" + os.sep + "lookups" + os.sep + "text" + os.sep + "defaults.txt")

        store.load(default_collection)

