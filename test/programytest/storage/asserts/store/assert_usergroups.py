import unittest
import unittest.mock
import os
import os.path

from programy.security.authorise.usergroupsauthorisor import BasicUserGroupAuthorisationService


class UserGroupsStoreAsserts(unittest.TestCase):

    def assert_upload_from_file(self, store):
        store.empty()

        store.upload_from_file(os.path.dirname(__file__) + os.sep + "data" + os.sep + "security" + os.sep + "roles.yaml")

        config = unittest.mock.Mock()
        config.usergroups = "Test"
        usersgroupsauthorisor = BasicUserGroupAuthorisationService(config)
        store.load_usergroups(usersgroupsauthorisor)

        self.assertTrue(usersgroupsauthorisor.authorise("console", "admin"))
        with self.assertRaises(Exception):
            self.assertFalse(usersgroupsauthorisor.authorise("offred", "admin"))
