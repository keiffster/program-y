import unittest

class VariablesStoreAsserts(unittest.TestCase):

    def assert_variables_storage(self, store):

        store.empty()

        variables = {"name1": "val1", "name2": "val2", "name3": "val3"}
        store.add_variables("client1", "user1", variables)
        store.commit()

        new_variables = store.get_variables("client1", "user1")
        self.assertTrue("name1" in new_variables)
        self.assertEqual("val1", new_variables["name1"])
        self.assertTrue("name2" in new_variables)
        self.assertEqual("val2", new_variables["name2"])
        self.assertTrue("name3" in new_variables)
        self.assertEqual("val3", new_variables["name3"])
        self.assertFalse("name4" in new_variables)

        store.empty()
        new_variables = store.get_variables("client1", "user1")
        self.assertEqual(0, len(new_variables.keys()))

    def assert_variable_storage(self, store):

        store.empty()

        store.add_variable("client1", "user1", "name1", "val1")

        new_variables = store.get_variables("client1", "user1")

        self.assertTrue("name1" in new_variables)
        self.assertEqual("val1", new_variables["name1"])
        self.assertFalse("name2" in new_variables)

        store.add_variable("client1", "user1", "name2", "val2")
        store.commit()
        new_variables = store.get_variables("client1", "user1")
        self.assertTrue("name1" in new_variables)
        self.assertEqual("val1", new_variables["name1"])
        self.assertTrue("name2" in new_variables)
        self.assertEqual("val2", new_variables["name2"])
        self.assertFalse("name3" in new_variables)

    def assert_empty_variables(self, store):

        store.empty()

        store.add_variable("client1", "user1", "name1", "val1")
        store.commit()

        store.add_variable("client1", "user2", "name2", "val2")
        store.commit()

        new_variables = store.get_variables("client1", "user1")
        self.assertTrue("name1" in new_variables)
        self.assertEqual("val1", new_variables["name1"])
        new_variables = store.get_variables("client1", "user2")
        self.assertTrue("name2" in new_variables)
        self.assertEqual("val2", new_variables["name2"])

        store.empty_variables("client1", "user1")

        new_variables = store.get_variables("client1", "user1")
        self.assertFalse("name1" in new_variables)
        new_variables = store.get_variables("client1", "user2")
        self.assertTrue("name2" in new_variables)
        self.assertEqual("val2", new_variables["name2"])
