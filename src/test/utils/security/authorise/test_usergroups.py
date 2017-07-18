import unittest

from programy.utils.security.authorise.usergroups import User
from programy.utils.security.authorise.usergroups import Group

class UserGroupTests(unittest.TestCase):

    def test_users(self):
        user1 = User("keith")
        user1.roles.append("admin1")
        self.assertTrue(user1.has_role("admin1"))
        self.assertFalse(user1.has_role("adminx"))

    def test_groups(self):
        group1 = Group("sysadmin")
        group1.roles.append("admin2")
        self.assertTrue(group1.has_role("admin2"))

    def test_users_and_groups(self):
        user1 = User("keith")
        user1.roles.append("admin1")
        self.assertTrue(user1.has_role("admin1"))
        self.assertFalse(user1.has_role("adminx"))

        group1 = Group("sysadmin")
        group1.roles.append("admin2")
        self.assertTrue(group1.has_role("admin2"))

        group2 = Group("operations")
        group2.roles.append("audit")
        group1.groups.append(group2)

        user2 = User("fred")
        user2.groups.append(group1)
        user2.roles.append("admin3")
        self.assertTrue(user2.has_group("sysadmin"))
        self.assertTrue(user2.has_role("admin2"))
        self.assertTrue(user2.has_role("admin3"))
        self.assertFalse(user2.has_role("adminx"))

