import unittest

from programy.storage.stores.nosql.mongo.dao.usergroups import UserGroups

class UserGroupsTests(unittest.TestCase):

    def test_init_no_id(self):
        usergroups = UserGroups(usergroups={})

        self.assertIsNotNone(usergroups)
        self.assertIsNone(usergroups.id)
        self.assertEqual({'usergroups': {}}, usergroups.to_document())

    def test_init_with_id(self):
        usergroups = UserGroups(usergroups={})
        usergroups.id = '666'

        self.assertIsNotNone(usergroups)
        self.assertEqual('666', usergroups.id)
        self.assertEqual({'_id': '666', 'usergroups': {}}, usergroups.to_document())

    def test_from_document(self):
        usergroups1 = UserGroups.from_document({'usergroups': {}})
        self.assertIsNotNone(usergroups1)
        self.assertIsNone(usergroups1.id)
        self.assertEqual({}, usergroups1.usergroups)

        usergroups2 = UserGroups.from_document({'_id': '666', 'usergroups': {}})
        self.assertIsNotNone(usergroups2)
        self.assertEqual('666', usergroups2.id)
        self.assertEqual({}, usergroups2.usergroups)

