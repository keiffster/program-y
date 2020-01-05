import unittest
import unittest.mock
import yaml
from programy.storage.entities.usergroups import UserGroupsStore
from programy.security.authorise.usergroupsauthorisor import BasicUserGroupAuthorisationService
from programy.config.brain.security import BrainSecurityAuthorisationConfiguration
from programy.security.authorise.usergroups import User
from programy.security.authorise.usergroups import Group


class UserGroupsStoreTests(unittest.TestCase):

    def test_upload_from_file_no_implemented(self):
        store = UserGroupsStore()
        with self.assertRaises(NotImplementedError):
            store.upload_from_file("test.txt")

    def test_load_usergroups(self):
        store = UserGroupsStore()
        with self.assertRaises(NotImplementedError):
            usersgroupsauthorisor = unittest.mock.Mock()
            store.load_usergroups(usersgroupsauthorisor)

    def test_load_users_user_groups(self):
        user = User("console")
        store = UserGroupsStore()

        yaml_data =  yaml.load("""
            groups:
              sysadmin, localuser
        """, Loader=yaml.FullLoader)

        store._load_users_user_groups(yaml_data, user, "console")

        self.assertTrue("sysadmin" in user.groups)
        self.assertTrue("localuser" in user.groups)
        self.assertFalse("other" in user.groups)

    def test_load_users_user_groups_duplicates(self):
        user = User("console")
        store = UserGroupsStore()

        yaml_data = yaml.load("""
            groups:
              sysadmin, localuser, localuser
        """, Loader=yaml.FullLoader)

        store._load_users_user_groups(yaml_data, user, "console")

        self.assertTrue("sysadmin" in user.groups)
        self.assertTrue("localuser" in user.groups)
        self.assertFalse("other" in user.groups)

    def test_load_users_user_roles(self):
        user = User("console")
        store = UserGroupsStore()

        yaml_data = yaml.load("""
            roles:
              su, local
        """, Loader=yaml.FullLoader)

        store._load_users_user_roles(yaml_data, user, "console")

        self.assertTrue("su" in user.roles)
        self.assertTrue("local" in user.roles)
        self.assertFalse("other" in user.roles)

    def test_load_users_user_roles_duplicates(self):
        user = User("console")
        store = UserGroupsStore()

        yaml_data = yaml.load("""
            roles:
              su, local, su
        """, Loader=yaml.FullLoader)

        store._load_users_user_roles(yaml_data, user, "console")

        self.assertTrue("su" in user.roles)
        self.assertTrue("local" in user.roles)
        self.assertFalse("other" in user.roles)

    def test_load_users_user(self):
        authorisor = BasicUserGroupAuthorisationService(BrainSecurityAuthorisationConfiguration())
        store = UserGroupsStore()

        yaml_data = yaml.load("""
            users:
              console:
                roles:
                  user
                groups:
                  sysadmin
        """, Loader=yaml.FullLoader)

        store._load_users_user(yaml_data, "console", authorisor)

        self.assertTrue("console" in authorisor.users.keys())
        self.assertIsInstance(authorisor.users['console'], User)
        self.assertTrue("user" in authorisor.users['console'].roles)
        self.assertTrue("sysadmin" in authorisor.users['console'].groups)

    def test_load_users(self):
        authorisor = BasicUserGroupAuthorisationService(BrainSecurityAuthorisationConfiguration())
        store = UserGroupsStore()

        yaml_data = yaml.load("""
            users:
              console:
                roles:
                  user
                groups:
                  sysadmin, local
              viewer:
                roles:
                  user
                groups:
                  local
        """, Loader=yaml.FullLoader)

        store._load_users(yaml_data,authorisor)

        self.assertTrue("console" in authorisor.users.keys())
        self.assertIsInstance(authorisor.users['console'], User)
        self.assertTrue("user" in authorisor.users['console'].roles)
        self.assertTrue("sysadmin" in authorisor.users['console'].groups)
        self.assertTrue("local" in authorisor.users['console'].groups)

        self.assertTrue("viewer" in authorisor.users.keys())
        self.assertIsInstance(authorisor.users['viewer'], User)
        self.assertTrue("user" in authorisor.users['viewer'].roles)
        self.assertTrue("local" in authorisor.users['viewer'].groups)

    def test_load_users_no_users(self):
        authorisor = BasicUserGroupAuthorisationService(BrainSecurityAuthorisationConfiguration())
        store = UserGroupsStore()

        yaml_data = yaml.load("""
            others:
              console:
                roles:
                  user
                groups:
                  sysadmin, local
              viewer:
                roles:
                  user
                groups:
                  local
        """, Loader=yaml.FullLoader)

        store._load_users(yaml_data,authorisor)

        self.assertFalse("console" in authorisor.users.keys())
        self.assertFalse("viewer" in authorisor.users.keys())

    def test_load_groups_group_groups(self):
        group = Group("sysadmin")
        store = UserGroupsStore()

        yaml_data = yaml.load("""
         groups:
            su  
         """, Loader=yaml.FullLoader)

        store._load_groups_group_groups(yaml_data, group, "sysadmin")

        self.assertTrue("su" in group.groups)

    def test_load_groups_group_groups_duplicates(self):
        group = Group("sysadmin")
        store = UserGroupsStore()

        yaml_data = yaml.load("""
         groups:
            su, su
         """, Loader=yaml.FullLoader)

        store._load_groups_group_groups(yaml_data, group, "sysadmin")

        self.assertTrue("su" in group.groups)

    def test_load_groups_group_users(self):
        group = Group("sysadmin")
        store = UserGroupsStore()

        yaml_data = yaml.load("""
         users:
            user1, user2  
         """, Loader=yaml.FullLoader)

        store._load_groups_group_users(yaml_data, group, "sysadmin")

        self.assertTrue("user1" in group.users)
        self.assertTrue("user2" in group.users)

    def test_load_groups_group_users_duplicates(self):
        group = Group("sysadmin")
        store = UserGroupsStore()

        yaml_data = yaml.load("""
         users:
            user1, user2, user1
         """, Loader=yaml.FullLoader)

        store._load_groups_group_users(yaml_data, group, "sysadmin")

        self.assertTrue("user1" in group.users)
        self.assertTrue("user2" in group.users)

    def test_load_groups_group_roles(self):
        group = Group("sysadmin")
        store = UserGroupsStore()

        yaml_data = yaml.load("""
         roles:
            role1, role2, role3  
         """, Loader=yaml.FullLoader)

        store._load_groups_group_roles(yaml_data, group, "sysadmin")

        self.assertTrue("role1" in group.roles)
        self.assertTrue("role2" in group.roles)
        self.assertTrue("role3" in group.roles)

    def test_load_groups_group_roles_duplicates(self):
        group = Group("sysadmin")
        store = UserGroupsStore()

        yaml_data = yaml.load("""
         roles:
            role1, role2, role3, role1, role3
         """, Loader=yaml.FullLoader)

        store._load_groups_group_roles(yaml_data, group, "sysadmin")

        self.assertTrue("role1" in group.roles)
        self.assertTrue("role2" in group.roles)
        self.assertTrue("role3" in group.roles)

    def test_load_groups_group(self):
        authorisor = BasicUserGroupAuthorisationService(BrainSecurityAuthorisationConfiguration())
        store = UserGroupsStore()

        yaml_data = yaml.load("""
        groups:
          group1:
            roles:
              role1, role2, role3  
            groups:
              group1, group2
            users:
              user1, user2
         """, Loader=yaml.FullLoader)

        store._load_groups_group(yaml_data, "group1", authorisor)

        self.assertTrue("group1" in authorisor.groups)
        self.assertTrue("role1" in authorisor.groups['group1'].roles)
        self.assertTrue("role2" in authorisor.groups['group1'].roles)
        self.assertTrue("role2" in authorisor.groups['group1'].roles)
        self.assertTrue("group1" in authorisor.groups['group1'].groups)
        self.assertTrue("group2" in authorisor.groups['group1'].groups)
        self.assertTrue("user1" in authorisor.groups['group1'].users)
        self.assertTrue("user2" in authorisor.groups['group1'].users)

    def test_load_groups_group_no_roles(self):
        authorisor = BasicUserGroupAuthorisationService(BrainSecurityAuthorisationConfiguration())
        store = UserGroupsStore()

        yaml_data = yaml.load("""
        groups:
          group1:
            groups:
              group1, group2
            users:
              user1, user2
         """, Loader=yaml.FullLoader)

        store._load_groups_group(yaml_data, "group1", authorisor)

        self.assertTrue("group1" in authorisor.groups)
        self.assertTrue("group1" in authorisor.groups['group1'].groups)
        self.assertTrue("group2" in authorisor.groups['group1'].groups)
        self.assertTrue("user1" in authorisor.groups['group1'].users)
        self.assertTrue("user2" in authorisor.groups['group1'].users)

    def test_load_groups(self):

        authorisor = BasicUserGroupAuthorisationService(BrainSecurityAuthorisationConfiguration())
        store = UserGroupsStore()

        yaml_data = yaml.load("""
        groups:
          group1:
            roles:
              role1, role2, role3  
            groups:
              group1, group2
            users:
              user1, user2

          group2:
            roles:
              role4, role5  
            groups:
              group3
            users:
              user3
         """, Loader=yaml.FullLoader)

        store._load_groups(yaml_data,authorisor)

        self.assertTrue("group1" in authorisor.groups)
        self.assertTrue("role1" in authorisor.groups['group1'].roles)
        self.assertTrue("role2" in authorisor.groups['group1'].roles)
        self.assertTrue("role2" in authorisor.groups['group1'].roles)
        self.assertTrue("group1" in authorisor.groups['group1'].groups)
        self.assertTrue("group2" in authorisor.groups['group1'].groups)
        self.assertTrue("user1" in authorisor.groups['group1'].users)
        self.assertTrue("user2" in authorisor.groups['group1'].users)

        self.assertTrue("group2" in authorisor.groups)
        self.assertTrue("role4" in authorisor.groups['group2'].roles)
        self.assertTrue("role5" in authorisor.groups['group2'].roles)
        self.assertTrue("group3" in authorisor.groups['group2'].groups)
        self.assertTrue("user3" in authorisor.groups['group2'].users)

    def test_load_groups_no_groups(self):

        authorisor = BasicUserGroupAuthorisationService(BrainSecurityAuthorisationConfiguration())
        store = UserGroupsStore()

        yaml_data = yaml.load("""
        others:
          group1:
            roles:
              role1, role2, role3  
            groups:
              group1, group2
            users:
              user1, user2

          group2:
            roles:
              role4, role5  
            groups:
              group3
            users:
              user3
         """, Loader=yaml.FullLoader)

        store._load_groups(yaml_data,authorisor)

        self.assertFalse("group1" in authorisor.groups)
        self.assertFalse("group2" in authorisor.groups)

    def test_overall_load(self):

        authorisor = BasicUserGroupAuthorisationService(BrainSecurityAuthorisationConfiguration())
        store = UserGroupsStore()

        yaml_data = yaml.load("""
        users:
          user1:
            groups:
              group1
          user2:
            groups:
              group2

        groups:
          group1:
            roles:
              role1, role2, role3  
            groups:
              group1, group2
            users:
              user1, user2

          group2:
            roles:
              role4, role5  
            groups:
              group3
            users:
              user3
              
          group3:
            roles:
              role6
         """, Loader=yaml.FullLoader)

        store.load_users_and_groups_from_yaml(yaml_data,authorisor)

    def test_overall_load_missing_groups(self):
        authorisor = BasicUserGroupAuthorisationService(BrainSecurityAuthorisationConfiguration())
        store = UserGroupsStore()

        yaml_data = yaml.load("""
        users:
          user1:
            groups:
              group1
          user2:
            groups:
              group4

        groups:
          group1:
            roles:
              role1, role2, role3  
            groups:
              group1, group2
            users:
              user1, user2

          group2:
            roles:
              role4, role5  
            groups:
              group5
            users:
              user3
              
          group3:
            roles:
              role6         """, Loader=yaml.FullLoader)

        store.load_users_and_groups_from_yaml(yaml_data, authorisor)
