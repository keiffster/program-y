import unittest
import unittest.mock
import yaml
from programy.storage.entities.usergroups import UserGroupsStore
from programy.security.authorise.usergroupsauthorisor import BasicUserGroupAuthorisationService
from programy.config.brain.security import BrainSecurityAuthorisationConfiguration


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
        authorisor = BasicUserGroupAuthorisationService(BrainSecurityAuthorisationConfiguration())
        store = UserGroupsStore()
        yaml_data =  yaml.load("""users:
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
      ask""", Loader=yaml.FullLoader)

        store.load_users(yaml_data, authorisor)

    def test_load_groups(self):
        authorisor = BasicUserGroupAuthorisationService(BrainSecurityAuthorisationConfiguration())
        store = UserGroupsStore()
        yaml_data = yaml.load("""users:
  console:
    roles:
      user
    groups:
      sysadmin
      
  user:
    roles:
      ask""", Loader=yaml.FullLoader)

        store.load_groups(yaml_data, authorisor)

    def test_combine_users_and_groups(self):
        authorisor = BasicUserGroupAuthorisationService(BrainSecurityAuthorisationConfiguration())
        store = UserGroupsStore()
        yaml_data = yaml.load("""groups:
          sysadmin:
            roles:
              root, admin, system
            groups:
              user

          user:
            roles:
              ask""", Loader=yaml.FullLoader)

        store.load_users(yaml_data, authorisor)
        store.load_groups(yaml_data, authorisor)
        store.combine_users_and_groups(authorisor)
