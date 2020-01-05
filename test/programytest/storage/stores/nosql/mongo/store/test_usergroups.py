import unittest
from unittest.mock import patch
import programytest.storage.engines as Engines
from programy.storage.stores.nosql.mongo.config import MongoStorageConfiguration
from programy.storage.stores.nosql.mongo.engine import MongoStorageEngine
from programy.storage.stores.nosql.mongo.store.usergroups import MongoUserGroupsStore
from programytest.storage.asserts.store.assert_usergroups import UserGroupsStoreAsserts


class MongoUserGroupsStoreTests(UserGroupsStoreAsserts):

    @unittest.skipIf(Engines.mongo is False, Engines.mongo_disabled)
    def test_initialise(self):
        config = MongoStorageConfiguration()
        engine = MongoStorageEngine(config)
        engine.initialise()
        store = MongoUserGroupsStore(engine)
        self.assertEqual(store.storage_engine, engine)
        
    @unittest.skipIf(Engines.mongo is False, Engines.mongo_disabled)
    def test_upload_from_file(self):
        config = MongoStorageConfiguration()
        engine = MongoStorageEngine(config)
        engine.initialise()
        store = MongoUserGroupsStore(engine)

        self.assert_upload_from_file(store)

    def patch_read_yaml_from_file(self, filename):
        raise Exception("Mock Exception")

    @unittest.skipIf(Engines.mongo is False, Engines.mongo_disabled)
    @patch("programy.storage.stores.nosql.mongo.store.usergroups.MongoUserGroupsStore._read_yaml_from_file",patch_read_yaml_from_file)
    def test_upload_from_file_exception(self):
        config = MongoStorageConfiguration()
        engine = MongoStorageEngine(config)
        engine.initialise()
        store = MongoUserGroupsStore(engine)

        self.assert_upload_from_file_exception(store)

    @unittest.skipIf(Engines.mongo is False, Engines.mongo_disabled)
    def test_upload_from_file_no_collection(self):
        config = MongoStorageConfiguration()
        engine = MongoStorageEngine(config)
        engine.initialise()
        store = MongoUserGroupsStore(engine)

        self.assert_upload_from_file_no_collection(store)

    def patch_add_document(self, document):
        return False

    @unittest.skipIf(Engines.mongo is False, Engines.mongo_disabled)
    @patch("programy.storage.stores.nosql.mongo.store.mongostore.MongoStore.add_document", patch_add_document)
    def test_upload_from_file_add_document_false(self):
        config = MongoStorageConfiguration()
        engine = MongoStorageEngine(config)
        engine.initialise()
        store = MongoUserGroupsStore(engine)

        self.assert_upload_from_file_exception(store)

