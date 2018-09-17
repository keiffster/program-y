import unittest

from programy.security.authorise.usergroups import User
from programy.security.authorise.usergroups import Group
from programy.security.authorise.usergroups import Authorisable


class UserGroupTests(unittest.TestCase):

    def test_users(self):
        user = User("keith")
        self.assertEqual("keith", user.userid)
        user.roles.append("admin1")
        self.assertTrue(user.has_role("admin1"))
        self.assertFalse(user.has_role("adminx"))

        group = Group("sysadmin")
        self.assertFalse(group.has_user("keith"))
        self.assertEqual([], user.groups)
        user.add_to_group(group)
        self.assertTrue(group.has_user("keith"))
        self.assertEqual([group], user.groups)
        user.add_to_group(group)
        self.assertTrue(group.has_user("keith"))
        self.assertEqual([group], user.groups)

    def test_groups(self):
        group = Group("sysadmin")
        self.assertEqual("sysadmin", group.groupid)

        self.assertFalse(group.has_role("admin2"))
        group.roles.append("admin2")
        self.assertTrue(group.has_role("admin2"))

        self.assertEqual([], group.users)
        self.assertFalse(group.has_user("keith"))
        self.assertFalse(group.has_user("fred"))
        user = User("keith")
        group.add_user(user)
        self.assertEqual([user], group.users)
        self.assertTrue(group.has_user("keith"))
        self.assertFalse(group.has_user("fred"))

        group.add_user(user)
        self.assertEqual([user], group.users)

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

    def test_authorisable(self):
        authorisable = Authorisable("testid")
        self.assertEqual("testid", authorisable._id)
        self.assertEqual([], authorisable.roles)
        self.assertEqual([], authorisable.groups)

        self.assertEqual([], authorisable.available_roles())

        self.assertFalse(authorisable.has_role("user"))
        self.assertFalse(authorisable.has_role("admin"))
        self.assertFalse(authorisable.has_group("sysadmin"))

        self.assertEqual([], authorisable.roles)
        authorisable.add_role("user")
        self.assertEqual(['user'], authorisable.roles)
        authorisable.add_role("user")
        self.assertEqual(['user'], authorisable.roles)
        self.assertTrue(authorisable.has_role("user"))

        group = Group("sysadmin")

        group.roles.append("admin")
        self.assertEqual([], authorisable.groups)
        authorisable.add_group(group)
        self.assertEqual([group], authorisable.groups)
        authorisable.add_group(group)
        self.assertEqual([group], authorisable.groups)

        self.assertTrue(authorisable.has_group("sysadmin"))
        self.assertTrue(authorisable.has_role("admin"))

        self.assertEqual(['user', 'admin'], authorisable.available_roles())

        group2 = Group("root")
        self.assertFalse(authorisable.has_group("root"))
        group.add_group(group2)
        self.assertTrue(authorisable.has_group("root"))