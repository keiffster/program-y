import unittest.mock
import os
import os.path

from programy.storage.stores.file.store.usergroups import FileUserGroupStore
from programy.storage.stores.file.engine import FileStorageEngine
from programy.storage.stores.file.config import FileStorageConfiguration
from programy.security.authorise.usergroupsauthorisor import BasicUserGroupAuthorisationService
from programy.storage.stores.file.config import FileStoreConfiguration

class FileSpellingStoreTests(unittest.TestCase):

    def test_initialise(self):
        config = FileStorageConfiguration()
        engine = FileStorageEngine(config)
        engine.initialise()
        store = FileUserGroupStore(engine)
        self.assertEqual(store.storage_engine, engine)

    def test_load_users_and_groups(self):
        config = FileStorageConfiguration()
        config._usergroups_storage =  FileStoreConfiguration(file=os.path.dirname(__file__) + os.sep + "data" + os.sep + "security" + os.sep + "roles.yaml", format="yaml", encoding="utf-8", delete_on_start=False)
        engine = FileStorageEngine(config)
        engine.initialise()
        store = FileUserGroupStore(engine)

        store.empty()

        config = unittest.mock.Mock()
        config.usergroups = "Test"
        usersgroupsauthorisor = BasicUserGroupAuthorisationService(config)
        store.load_usergroups(usersgroupsauthorisor)

        self.assertTrue(usersgroupsauthorisor.authorise("console", "admin"))
        with self.assertRaises(Exception):
            self.assertFalse(usersgroupsauthorisor.authorise("offred", "admin"))
