import unittest

class UserStoreAsserts(unittest.TestCase):

    def assert_user_storage(self, store):
        
        store.empty()

        store.add_user('1', "console")
        store.add_user('1', "facebook")
        store.add_user('2', "console")
        store.add_user('3', "twitter")
        store.add_user('4', "facebook")
        store.add_user('5', "console")
        store.commit()

        self.assertTrue(store.exists('1', "console"))
        self.assertFalse(store.exists('2', "facebook"))

        links = store.get_links('1')
        self.assertEquals(['console', "facebook"], links)

        links = store.get_links('999')
        self.assertEquals([], links)

        store.remove_user('1', "console")
        self.assertFalse(store.exists('1', "console"))

        store.add_user('1', "console")
        self.assertTrue(store.exists('1', "console"))
        self.assertTrue(store.exists('1', "facebook"))

        store.remove_user_from_all_clients('1')
        self.assertFalse(store.exists('1', "console"))
        self.assertFalse(store.exists('1', "facebook"))
