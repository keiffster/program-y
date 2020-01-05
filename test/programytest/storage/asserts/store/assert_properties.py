import unittest
import os


class PropertyStoreAsserts(unittest.TestCase):

    def assert_properties_storage(self, store):
        store.empty()

        properties = {"name1": "val1", "name2": "val2", "name3": "val3"}
        store.add_properties(properties)
        store.commit()

        new_properties = store.get_properties()
        self.assertTrue("name1" in new_properties)
        self.assertEqual("val1", new_properties["name1"])
        self.assertTrue("name2" in new_properties)
        self.assertEqual("val2", new_properties["name2"])
        self.assertTrue("name3" in new_properties)
        self.assertEqual("val3", new_properties["name3"])
        self.assertFalse("name4" in new_properties)

    def assert_property_storage(self, store):
        store.empty()

        store.add_property("name1", "val1")

        new_properties = store.get_properties()

        self.assertTrue("name1" in new_properties)
        self.assertEqual("val1", new_properties["name1"])
        self.assertFalse("name2" in new_properties)

        store.add_property("name2", "val2")
        store.commit()

        new_properties = store.get_properties()
        self.assertTrue("name1" in new_properties)
        self.assertEqual("val1", new_properties["name1"])
        self.assertTrue("name2" in new_properties)
        self.assertEqual("val2", new_properties["name2"])
        self.assertFalse("name3" in new_properties)

    def assert_duplicate_property_storage(self, store):
        store.empty()

        store.add_property("name1", "val1")

        new_properties = store.get_properties()

        self.assertTrue("name1" in new_properties)
        self.assertEqual("val1", new_properties["name1"])
        self.assertFalse("name2" in new_properties)

        store.add_property("name1", "val2")

        new_properties2 = store.get_properties()
        self.assertTrue("name1" in new_properties2)
        self.assertEqual("val2", new_properties2["name1"])

    def assert_empty_properties(self, store):
        store.empty()

        store.add_property("name1", "val1")
        store.commit()

        store.add_property("name2", "val2")
        store.commit()

        new_properties = store.get_properties()
        self.assertTrue("name1" in new_properties)
        self.assertEqual("val1", new_properties["name1"])
        new_properties = store.get_properties()
        self.assertTrue("name2" in new_properties)
        self.assertEqual("val2", new_properties["name2"])

        store.empty_properties()

        new_properties = store.get_properties()
        self.assertFalse("name1" in new_properties)

    def assert_upload_from_file(self, store):
        store.empty()

        count, success = store.upload_from_file(os.path.dirname(
            __file__) + os.sep + "data" + os.sep + "lookups" + os.sep + "text" + os.sep + "properties.txt", verbose=False)

        self.assertEquals(93, count)
        self.assertEquals(80, success)

    def assert_upload_from_file_verbose(self, store):
        store.empty()

        count, success = store.upload_from_file(os.path.dirname(
            __file__) + os.sep + "data" + os.sep + "lookups" + os.sep + "text" + os.sep + "properties.txt", verbose=True)

        self.assertEquals(93, count)
        self.assertEquals(80, success)

    def assert_upload_from_file_exception(self, store):
        store.empty()

        count, success = store.upload_from_file(os.path.dirname(
            __file__) + os.sep + "data" + os.sep + "lookups" + os.sep + "text" + os.sep + "properties.txt")

        self.assertEquals(0, count)
        self.assertEquals(0, success)
