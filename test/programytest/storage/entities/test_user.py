import unittest

from programy.storage.entities.user import UserStore

class UserStoreTests(unittest.TestCase):

    def test_add_user(self):
        user_store = UserStore()
        with self.assertRaises(NotImplementedError):
            user_store.add_user("userid", "testclient")
