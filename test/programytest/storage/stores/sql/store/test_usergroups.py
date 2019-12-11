import yaml
import unittest.mock
from unittest.mock import patch
import programytest.storage.engines as Engines
from programy.storage.stores.sql.config import SQLStorageConfiguration
from programy.storage.stores.sql.engine import SQLStorageEngine
from programy.storage.stores.sql.store.usergroups import SQLUserGroupStore
from programytest.storage.asserts.store.assert_usergroups import UserGroupsStoreAsserts
from programy.security.authorise.usergroupsauthorisor import BasicUserGroupAuthorisationService
from programy.config.brain.security import BrainSecurityAuthorisationConfiguration
from programy.security.authorise.usergroups import User
from programy.security.authorise.authorisor import AuthorisationException


class SQLUserGroupStoreTests(UserGroupsStoreAsserts):

    @unittest.skipIf(Engines.sql is False, Engines.sql_disabled)
    def test_initialise(self):
        config = SQLStorageConfiguration()
        engine = SQLStorageEngine(config)
        engine.initialise()
        store = SQLUserGroupStore(engine)
        self.assertEqual(store.storage_engine, engine)

    @unittest.skipIf(Engines.sql is False, Engines.sql_disabled)
    def test_get_all(self):
        config = SQLStorageConfiguration()
        engine = SQLStorageEngine(config)
        engine.initialise()
        store = SQLUserGroupStore(engine)

        with self.assertRaises(Exception):
            store._get_all()

    @unittest.skipIf(Engines.sql is False, Engines.sql_disabled)
    def test_upload_from_file(self):
        config = SQLStorageConfiguration()
        engine = SQLStorageEngine(config)
        engine.initialise()
        store = SQLUserGroupStore(engine)

        self.assert_upload_from_file(store)

    def patch_read_yaml_from_file(self, filename):
        raise Exception("Mock Exception")

    @unittest.skipIf(Engines.sql is False, Engines.sql_disabled)
    @patch("programy.storage.stores.sql.store.usergroups.SQLUserGroupStore._read_yaml_from_file",
           patch_read_yaml_from_file)
    def test_upload_from_file_exception(self):
        config = SQLStorageConfiguration()
        engine = SQLStorageEngine(config)
        engine.initialise()
        store = SQLUserGroupStore(engine)

        self.assert_upload_from_file_exception(store)

    @unittest.skipIf(Engines.sql is False, Engines.sql_disabled)
    def test_upload_from_file_no_collection(self):
        config = SQLStorageConfiguration()
        engine = SQLStorageEngine(config)
        engine.initialise()
        store = SQLUserGroupStore(engine)

        self.assert_upload_from_file_no_collection(store)

    @unittest.skipIf(Engines.sql is False, Engines.sql_disabled)
    def test_load_users_user_groups(self):
        user = User("console")

        config = SQLStorageConfiguration()
        engine = SQLStorageEngine(config)
        engine.initialise()
        store = SQLUserGroupStore(engine)

        yaml_data = yaml.load("""
            groups:
              sysadmin, localuser
        """, Loader=yaml.FullLoader)

        store._load_users_user_groups(yaml_data, user, "console")

        self.assertTrue("sysadmin" in user.groups)
        self.assertTrue("localuser" in user.groups)
        self.assertFalse("other" in user.groups)

    @unittest.skipIf(Engines.sql is False, Engines.sql_disabled)
    def test_load_users_user_groups_duplicates(self):
        user = User("console")

        config = SQLStorageConfiguration()
        engine = SQLStorageEngine(config)
        engine.initialise()
        store = SQLUserGroupStore(engine)

        yaml_data = yaml.load("""
            groups:
              sysadmin, localuser, localuser
        """, Loader=yaml.FullLoader)

        store._load_users_user_groups(yaml_data, user, "console")

        self.assertTrue("sysadmin" in user.groups)
        self.assertTrue("localuser" in user.groups)
        self.assertFalse("other" in user.groups)

    @unittest.skipIf(Engines.sql is False, Engines.sql_disabled)
    def test_load_users_user_roles(self):
        user = User("console")

        config = SQLStorageConfiguration()
        engine = SQLStorageEngine(config)
        engine.initialise()
        store = SQLUserGroupStore(engine)

        yaml_data = yaml.load("""
            roles:
              su, local
        """, Loader=yaml.FullLoader)

        store._load_users_user_roles(yaml_data, user, "console")

        self.assertTrue("su" in user.roles)
        self.assertTrue("local" in user.roles)
        self.assertFalse("other" in user.roles)

    @unittest.skipIf(Engines.sql is False, Engines.sql_disabled)
    def test_load_users_user_roles_duplicates(self):
        user = User("console")

        config = SQLStorageConfiguration()
        engine = SQLStorageEngine(config)
        engine.initialise()
        store = SQLUserGroupStore(engine)

        yaml_data = yaml.load("""
            roles:
              su, local, su
        """, Loader=yaml.FullLoader)

        store._load_users_user_roles(yaml_data, user, "console")

        self.assertTrue("su" in user.roles)
        self.assertTrue("local" in user.roles)
        self.assertFalse("other" in user.roles)

    @unittest.skipIf(Engines.sql is False, Engines.sql_disabled)
    def test_load_users(self):
        config = SQLStorageConfiguration()
        engine = SQLStorageEngine(config)
        engine.initialise()
        store = SQLUserGroupStore(engine)

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

        store._upload_users(yaml_data, verbose=False)

        authorisor = BasicUserGroupAuthorisationService(BrainSecurityAuthorisationConfiguration())
        store.load_usergroups(authorisor)

        self.assertTrue("console" in authorisor.users)
        self.assertTrue("viewer" in authorisor.users)
        self.assertFalse("sysadmin" in authorisor.groups)
        self.assertFalse("local" in authorisor.groups)
        self.assertTrue(authorisor.authorise("console", "user"))
        self.assertTrue(authorisor.authorise("viewer", "user"))

    @unittest.skipIf(Engines.sql is False, Engines.sql_disabled)
    def test_load_users_verbose(self):
        config = SQLStorageConfiguration()
        engine = SQLStorageEngine(config)
        engine.initialise()
        store = SQLUserGroupStore(engine)

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

        store.load_from_yaml(yaml_data, verbose=True)

        authorisor = BasicUserGroupAuthorisationService(BrainSecurityAuthorisationConfiguration())
        store.load_usergroups(authorisor)

        self.assertTrue("console" in authorisor.users)
        self.assertTrue("viewer" in authorisor.users)
        self.assertFalse("sysadmin" in authorisor.groups)
        self.assertFalse("local" in authorisor.groups)
        self.assertTrue(authorisor.authorise("console", "user"))
        self.assertTrue(authorisor.authorise("viewer", "user"))

    @unittest.skipIf(Engines.sql is False, Engines.sql_disabled)
    def test_load_users_no_users(self):
        config = SQLStorageConfiguration()
        engine = SQLStorageEngine(config)
        engine.initialise()
        store = SQLUserGroupStore(engine)

        yaml_data = yaml.load("""
            other:
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

        store._upload_users(yaml_data, verbose=True)

        authorisor = BasicUserGroupAuthorisationService(BrainSecurityAuthorisationConfiguration())
        store.load_usergroups(authorisor)

        self.assertFalse("console" in authorisor.users)
        self.assertFalse("viewer" in authorisor.users)
        self.assertFalse("sysadmin" in authorisor.groups)
        self.assertFalse("local" in authorisor.groups)
        with self.assertRaises(AuthorisationException):
            authorisor.authorise("console", "user")
        with self.assertRaises(AuthorisationException):
            authorisor.authorise("viewer", "user")

    @unittest.skipIf(Engines.sql is False, Engines.sql_disabled)
    def test_load_users_no_roles(self):
        config = SQLStorageConfiguration()
        engine = SQLStorageEngine(config)
        engine.initialise()
        store = SQLUserGroupStore(engine)

        yaml_data = yaml.load("""
            users:
              console:
                groups:
                  sysadmin, local
              viewer:
                groups:
                  local
        """, Loader=yaml.FullLoader)

        store._upload_users(yaml_data, verbose=True)

        authorisor = BasicUserGroupAuthorisationService(BrainSecurityAuthorisationConfiguration())
        store.load_usergroups(authorisor)

        self.assertTrue("console" in authorisor.users)
        self.assertTrue("viewer" in authorisor.users)
        self.assertFalse("sysadmin" in authorisor.groups)
        self.assertFalse("local" in authorisor.groups)
        self.assertFalse(authorisor.authorise("console", "user"))
        self.assertFalse(authorisor.authorise("viewer", "user"))

    @unittest.skipIf(Engines.sql is False, Engines.sql_disabled)
    def test_load_users_no_groups(self):
        config = SQLStorageConfiguration()
        engine = SQLStorageEngine(config)
        engine.initialise()
        store = SQLUserGroupStore(engine)

        yaml_data = yaml.load("""
             users:
               console:
                 roles:
                   user
               viewer:
                 roles:
                   user
         """, Loader=yaml.FullLoader)

        store._upload_users(yaml_data, verbose=True)

        authorisor = BasicUserGroupAuthorisationService(BrainSecurityAuthorisationConfiguration())
        store.load_usergroups(authorisor)

        self.assertTrue("console" in authorisor.users)
        self.assertTrue("viewer" in authorisor.users)
        self.assertFalse("sysadmin" in authorisor.groups)
        self.assertFalse("local" in authorisor.groups)
        self.assertTrue(authorisor.authorise("console", "user"))
        self.assertTrue(authorisor.authorise("viewer", "user"))

    @unittest.skipIf(Engines.sql is False, Engines.sql_disabled)
    def test_load_groups(self):
        config = SQLStorageConfiguration()
        engine = SQLStorageEngine(config)
        engine.initialise()
        store = SQLUserGroupStore(engine)

        store.empty()

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

        store._upload_groups(yaml_data, verbose=False)

        authorisor = BasicUserGroupAuthorisationService(BrainSecurityAuthorisationConfiguration())
        store.load_usergroups(authorisor)

        self.assertTrue("group1" in authorisor.groups)
        self.assertTrue("group2" in authorisor.groups)

        self.assertTrue(authorisor.groups)

    @unittest.skipIf(Engines.sql is False, Engines.sql_disabled)
    def test_load_groups_verbose(self):
        config = SQLStorageConfiguration()
        engine = SQLStorageEngine(config)
        engine.initialise()
        store = SQLUserGroupStore(engine)

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

        store._upload_groups(yaml_data, verbose=True)

        authorisor = BasicUserGroupAuthorisationService(BrainSecurityAuthorisationConfiguration())
        store.load_usergroups(authorisor)

    @unittest.skipIf(Engines.sql is False, Engines.sql_disabled)
    def test_load_groups_no_groups(self):
        config = SQLStorageConfiguration()
        engine = SQLStorageEngine(config)
        engine.initialise()
        store = SQLUserGroupStore(engine)

        yaml_data = yaml.load("""
        other:
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

        store._upload_groups(yaml_data, verbose=False)

        authorisor = BasicUserGroupAuthorisationService(BrainSecurityAuthorisationConfiguration())
        store.load_usergroups(authorisor)

    @unittest.skipIf(Engines.sql is False, Engines.sql_disabled)
    def test_load_groups_no_group_roles(self):
        config = SQLStorageConfiguration()
        engine = SQLStorageEngine(config)
        engine.initialise()
        store = SQLUserGroupStore(engine)

        yaml_data = yaml.load("""
        groups:
          group1:
            groups:
              group1, group2
            users:
              user1, user2

          group2:
            groups:
              group3
            users:
              user3
         """, Loader=yaml.FullLoader)

        store._upload_groups(yaml_data, verbose=False)

        authorisor = BasicUserGroupAuthorisationService(BrainSecurityAuthorisationConfiguration())
        store.load_usergroups(authorisor)

    @unittest.skipIf(Engines.sql is False, Engines.sql_disabled)
    def test_load_groups_no_group_groups(self):
        config = SQLStorageConfiguration()
        engine = SQLStorageEngine(config)
        engine.initialise()
        store = SQLUserGroupStore(engine)

        yaml_data = yaml.load("""
        groups:
          group1:
            roles:
              role1, role2, role3  
            users:
              user1, user2

          group2:
            roles:
              role4, role5  
            users:
              user3
         """, Loader=yaml.FullLoader)

        store._upload_groups(yaml_data, verbose=False)

        authorisor = BasicUserGroupAuthorisationService(BrainSecurityAuthorisationConfiguration())
        store.load_usergroups(authorisor)

    @unittest.skipIf(Engines.sql is False, Engines.sql_disabled)
    def test_load_groups_no_group_users(self):
        config = SQLStorageConfiguration()
        engine = SQLStorageEngine(config)
        engine.initialise()
        store = SQLUserGroupStore(engine)

        yaml_data = yaml.load("""
        groups:
          group1:
            roles:
              role1, role2, role3  
            groups:
              group1, group2

          group2:
            roles:
              role4, role5  
            groups:
              group3
         """, Loader=yaml.FullLoader)

        store._upload_groups(yaml_data, verbose=False)

        authorisor = BasicUserGroupAuthorisationService(BrainSecurityAuthorisationConfiguration())
        store.load_usergroups(authorisor)

    @unittest.skipIf(Engines.sql is False, Engines.sql_disabled)
    def test_load_usergroups(self):
        config = SQLStorageConfiguration()
        engine = SQLStorageEngine(config)
        engine.initialise()
        store = SQLUserGroupStore(engine)

        yaml_data = yaml.load("""
         users:
           user1:
             groups:
               group1
           user2:
             groups:
               group4
           user3:
             groups:
               group1
                
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
               role6
               """, Loader=yaml.FullLoader)

        store.load_from_yaml(yaml_data, verbose=False)

        store.commit()

        authorisor = BasicUserGroupAuthorisationService(BrainSecurityAuthorisationConfiguration())
        store.load_usergroups(authorisor)

        self.assertTrue("user1" in authorisor.users)
        self.assertTrue("user2" in authorisor.users)
        self.assertTrue("user3" in authorisor.users)

        self.assertTrue("group1" in authorisor.groups)
        self.assertTrue("group2" in authorisor.groups)
        self.assertTrue("group3" in authorisor.groups)

        self.assertTrue(authorisor.authorise("user3", "role3"))