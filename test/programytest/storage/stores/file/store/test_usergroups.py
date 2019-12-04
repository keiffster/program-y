import os
import os.path
import unittest.mock
from unittest.mock import patch
from programy.security.authorise.usergroupsauthorisor import BasicUserGroupAuthorisationService
from programy.storage.stores.file.config import FileStorageConfiguration
from programy.storage.stores.file.config import FileStoreConfiguration
from programy.storage.stores.file.engine import FileStorageEngine
from programy.storage.stores.file.store.usergroups import FileUserGroupStore


class FileUserGroupsStoreTests(unittest.TestCase):

    def test_initialise(self):
        config = FileStorageConfiguration()
        engine = FileStorageEngine(config)
        engine.initialise()
        store = FileUserGroupStore(engine)
        self.assertEqual(store.storage_engine, engine)

    def test_storage_path(self):
        config = FileStorageConfiguration()
        engine = FileStorageEngine(config)
        engine.initialise()
        store = FileUserGroupStore(engine)

        self.assertEquals('/tmp/security/usergroups.yaml', store._get_storage_path())
        self.assertIsInstance(store.get_storage(), FileStoreConfiguration)

    def test_load_users_and_groups(self):
        config = FileStorageConfiguration()
        config._usergroups_storage =  FileStoreConfiguration(file=os.path.dirname(__file__) + os.sep + "data" + os.sep + "security" + os.sep + "roles.yaml", fileformat="yaml", encoding="utf-8", delete_on_start=False)
        engine = FileStorageEngine(config)
        engine.initialise()
        store = FileUserGroupStore(engine)

        config = unittest.mock.Mock()
        config.usergroups = "Test"
        usersgroupsauthorisor = BasicUserGroupAuthorisationService(config)
        self.assertTrue(store.load_usergroups(usersgroupsauthorisor))

        self.assertTrue(usersgroupsauthorisor.authorise("console", "admin"))
        with self.assertRaises(Exception):
            self.assertFalse(usersgroupsauthorisor.authorise("offred", "admin"))

    def patch_read_usergroups_from_file(self, filename, usersgroupsauthorisor):
        raise Exception ("Mock Exception")

    @patch ("programy.storage.stores.file.store.usergroups.FileUserGroupStore._read_usergroups_from_file", patch_read_usergroups_from_file)
    def test_load_users_groups_with_exception(self):
        config = FileStorageConfiguration()
        engine = FileStorageEngine(config)
        engine.initialise()
        store = FileUserGroupStore(engine)

        usersgroupsauthorisor = BasicUserGroupAuthorisationService(config)
        self.assertFalse(store.load_usergroups(usersgroupsauthorisor))
