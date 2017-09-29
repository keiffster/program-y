import unittest
import os
import yaml

from programy.security.authorise.usergrouploader import UserGroupLoader

class UserGroupLoaderTests(unittest.TestCase):

    def test_load_from_file(self):

        loader = UserGroupLoader()
        users_dict, groups_dict = loader.load_users_and_groups_from_file(os.path.dirname(__file__) + os.sep + "test_usergroups.yaml")

        users = list(users_dict.values())
        self.assertIsNotNone(users)
        groups = list(groups_dict.values())
        self.assertIsNotNone(groups)

        self.assertEqual(1, len(users))
        self.assertEqual("console", users[0].userid)
        self.assertEqual(1, len(users[0].groups))
        self.assertEqual("sysadmin", users[0].groups[0].groupid)
        self.assertEqual(1, len(users[0].roles))
        self.assertEqual("user", users[0].roles[0])

        self.assertEqual(2, len(groups))
        self.assertEqual("sysadmin", groups[0].groupid)
        self.assertEqual(3, len(groups[0].roles))
        self.assertEqual(1, len(groups[0].groups))
        self.assertEqual(0, len(groups[0].users))
        self.assertEqual("user", groups[1].groupid)
        self.assertEqual(1, len(groups[1].roles))
        self.assertEqual(0, len(groups[1].groups))
        self.assertEqual(0, len(groups[1].users))

    def test_load_no_data(self):
        loader = UserGroupLoader()
        with self.assertRaises(Exception):
            loader.load_users_and_groups_from_text("")

    def test_load_from_text_no_users(self):
        loader = UserGroupLoader()
        yaml_data = yaml.load("""
        groups:
           sysadmin:
             roles:
               root, admin, system
             groups:
               user

           user:
             roles:
               ask
         """)
        users = loader.load_users(yaml_data)
        self.assertIsNotNone(users)
        self.assertEqual({}, users)

        loader.dump_users_and_groups(users, None)

    def test_load_from_text_no_groups(self):
        loader = UserGroupLoader()
        yaml_data = yaml.load("""
        users:
          console:
            roles:
              user
            groups:
              sysadmin

        user:
          roles:
            ask
         """)
        groups = loader.load_groups(yaml_data)
        self.assertIsNotNone(groups)
        self.assertEqual({}, groups)

        loader.dump_users_and_groups(None, groups)

    def test_load_from_text(self):

        loader = UserGroupLoader()
        users_dict, groups_dict = loader.load_users_and_groups_from_text("""
        users:
          console:
            roles:
              user
            groups:
              sysadmin
        
        groups:
          sysadmin:
            roles:
              root, admin, system
            groups:
              user
              
          user:
            roles:
              ask
        """)

        loader.dump_users_and_groups(users_dict, groups_dict)

        users = list(users_dict.values())
        self.assertIsNotNone(users)
        groups = list(groups_dict.values())
        self.assertIsNotNone(groups)

        self.assertEqual(1, len(users))
        self.assertEqual("console", users[0].userid)
        self.assertEqual(1, len(users[0].groups))
        self.assertEqual("sysadmin", users[0].groups[0].groupid)
        self.assertEqual(1, len(users[0].roles))
        self.assertEqual("user", users[0].roles[0])

        self.assertEqual(2, len(groups))
        self.assertEqual("sysadmin", groups[0].groupid)
        self.assertEqual(3, len(groups[0].roles))
        self.assertEqual(1, len(groups[0].groups))
        self.assertEqual(0, len(groups[0].users))
        self.assertEqual("user", groups[1].groupid)
        self.assertEqual(1, len(groups[1].roles))
        self.assertEqual(0, len(groups[1].groups))
        self.assertEqual(0, len(groups[1].users))



    def test_load_from_text_multiples(self):

        loader = UserGroupLoader()
        users_dict, groups_dict = loader.load_users_and_groups_from_text("""
        users:
          user1:
            roles:
              role1, role2
            groups:
              group1, group2
              
        groups:
            group1:
                roles:
                    role4, role5, role6
                groups:
                    group2, group3
            group2:
                roles:
                    role7, role8, rol8
            group3:
                roles:
                    role10
        """)

        loader.dump_users_and_groups(users_dict, groups_dict)

        users = list(users_dict.values())
        self.assertIsNotNone(users)
        groups = list(groups_dict.values())
        self.assertIsNotNone(groups)

        self.assertEqual(1, len(users))
        self.assertEqual(2, len(users[0].roles))
        self.assertEqual(2, len(users[0].groups))


        self.assertEqual(3, len(groups))
        self.assertEqual(3, len(groups[0].roles))
        self.assertEqual(2, len(groups[0].groups))
        self.assertEqual(0, len(groups[0].users))
        self.assertEqual(3, len(groups[1].roles))
        self.assertEqual(0, len(groups[1].groups))
        self.assertEqual(0, len(groups[1].users))
        self.assertEqual(1, len(groups[2].roles))
        self.assertEqual(0, len(groups[2].groups))
        self.assertEqual(0, len(groups[2].users))

    def test_load_from_text_duplicates(self):
        loader = UserGroupLoader()
        users_dict, groups_dict = loader.load_users_and_groups_from_text("""
        users:
          user1:
            roles:
              role1, role1
            groups:
              group1, group1

        groups:
            group1:
                role:
                    role2
        """)


        loader.dump_users_and_groups(users_dict, groups_dict)

        users = list(users_dict.values())
        self.assertIsNotNone(users)

        self.assertEqual(1, len(users))
        self.assertEqual(1, len(users[0].roles))
        self.assertEqual(1, len(users[0].groups))

    def test_load_from_text_missing(self):
        loader = UserGroupLoader()
        users_dict, groups_dict = loader.load_users_and_groups_from_text("""
        users:
          user1:
            roles:
              role1
            groups:
              group1, group2

        groups:
            group1:
                role:
                    role2
        """)


        loader.dump_users_and_groups(users_dict, groups_dict)

        users = list(users_dict.values())
        self.assertIsNotNone(users)

        self.assertEqual(1, len(users))
        self.assertEqual(1, len(users[0].roles))
        self.assertEqual(1, len(users[0].groups))
