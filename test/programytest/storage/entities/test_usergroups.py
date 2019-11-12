import unittest
import unittest.mock
from programy.storage.entities.usergroups import UserGroupsStore


class UserGroupsStoreTests(unittest.TestCase):

    def test_store_category(self):
        store = UserGroupsStore()
        with self.assertRaises(NotImplementedError):
            store.upload_from_file("test.txt")

    def test_load_usergroups(self):
        store = UserGroupsStore()
        with self.assertRaises(NotImplementedError):
            usersgroupsauthorisor = unittest.mock.Mock()
            store.load_usergroups(usersgroupsauthorisor)

    def test_load_users(self):
        pass

    def test_load_groups(self):
        pass

    def test_combine_users_and_groups(self):
        pass

