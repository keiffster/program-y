import unittest


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

        store.empty()
        new_properties = store.get_properties()
        self.assertEqual(0, len(new_properties.keys()))

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

