import unittest.mock

import programytest.storage.engines as Engines
from programy.storage.stores.nosql.mongo.config import MongoStorageConfiguration
from programy.storage.stores.nosql.mongo.engine import MongoStorageEngine
from programy.storage.stores.nosql.mongo.store.categories import MongoCategoryStore
from programy.storage.stores.nosql.mongo.store.conversations import MongoConversationStore
from programy.storage.stores.nosql.mongo.store.duplicates import MongoDuplicatesStore
from programy.storage.stores.nosql.mongo.store.errors import MongoErrorsStore
from programy.storage.stores.nosql.mongo.store.learnf import MongoLearnfStore
from programy.storage.stores.nosql.mongo.store.licensekeys import MongoLicenseKeysStore
from programy.storage.stores.nosql.mongo.store.linkedaccounts import MongoLinkedAccountStore
from programy.storage.stores.nosql.mongo.store.links import MongoLinkStore
from programy.storage.stores.nosql.mongo.store.lookups import MongoDenormalStore
from programy.storage.stores.nosql.mongo.store.lookups import MongoGenderStore
from programy.storage.stores.nosql.mongo.store.lookups import MongoNormalStore
from programy.storage.stores.nosql.mongo.store.lookups import MongoPerson2Store
from programy.storage.stores.nosql.mongo.store.lookups import MongoPersonStore
from programy.storage.stores.nosql.mongo.store.maps import MongoMapsStore
from programy.storage.stores.nosql.mongo.store.nodes import MongoPatternNodeStore
from programy.storage.stores.nosql.mongo.store.nodes import MongoTemplateNodeStore
from programy.storage.stores.nosql.mongo.store.processors import MongoPostProcessorStore
from programy.storage.stores.nosql.mongo.store.processors import MongoPostQuestionProcessorStore
from programy.storage.stores.nosql.mongo.store.processors import MongoPreProcessorStore
from programy.storage.stores.nosql.mongo.store.properties import MongoDefaultVariablesStore
from programy.storage.stores.nosql.mongo.store.properties import MongoPropertyStore
from programy.storage.stores.nosql.mongo.store.properties import MongoRegexesStore
from programy.storage.stores.nosql.mongo.store.rdfs import MongoRDFsStore
from programy.storage.stores.nosql.mongo.store.sets import MongoSetsStore
from programy.storage.stores.nosql.mongo.store.spelling import MongoSpellingStore
from programy.storage.stores.nosql.mongo.store.twitter import MongoTwitterStore
from programy.storage.stores.nosql.mongo.store.usergroups import MongoUserGroupsStore
from programy.storage.stores.nosql.mongo.store.users import MongoUserStore
from programy.storage.stores.nosql.mongo.store.triggers import MongoTriggerStore
from programy.storage.stores.nosql.mongo.store.oobs import MongoOOBStore
from programytest.storage.test_utils import StorageEngineTestUtils


class MongoStorageEngineTests(StorageEngineTestUtils):

    @unittest.skipIf(Engines.mongo is False, Engines.mongo_disabled)
    def test_init_with_configuration(self):
        config = MongoStorageConfiguration()
        engine = MongoStorageEngine(config)
        self.assertIsNotNone(engine)
        self.assertIsNotNone(engine.configuration)

    def test_stores(self):
        config = unittest.mock.Mock
        engine = MongoStorageEngine(config)

        self.assertIsInstance(engine.category_store(), MongoCategoryStore)
        self.assertIsInstance(engine.errors_store(), MongoErrorsStore)
        self.assertIsInstance(engine.duplicates_store(), MongoDuplicatesStore)
        self.assertIsInstance(engine.learnf_store(), MongoLearnfStore)
        self.assertIsInstance(engine.conversation_store(), MongoConversationStore)
        self.assertIsInstance(engine.sets_store(), MongoSetsStore)
        self.assertIsInstance(engine.maps_store(), MongoMapsStore)
        self.assertIsInstance(engine.rdf_store(), MongoRDFsStore)
        self.assertIsInstance(engine.denormal_store(), MongoDenormalStore)
        self.assertIsInstance(engine.normal_store(), MongoNormalStore)
        self.assertIsInstance(engine.gender_store(), MongoGenderStore)
        self.assertIsInstance(engine.person_store(), MongoPersonStore)
        self.assertIsInstance(engine.person2_store(), MongoPerson2Store)
        self.assertIsInstance(engine.regex_store(), MongoRegexesStore)
        self.assertIsInstance(engine.property_store(), MongoPropertyStore)
        self.assertIsInstance(engine.defaults_store(), MongoDefaultVariablesStore)
        self.assertIsInstance(engine.twitter_store(), MongoTwitterStore)
        self.assertIsInstance(engine.spelling_store(), MongoSpellingStore)
        self.assertIsInstance(engine.license_store(), MongoLicenseKeysStore)
        self.assertIsInstance(engine.pattern_nodes_store(), MongoPatternNodeStore)
        self.assertIsInstance(engine.template_nodes_store(), MongoTemplateNodeStore)
        self.assertIsInstance(engine.preprocessors_store(), MongoPreProcessorStore)
        self.assertIsInstance(engine.postprocessors_store(), MongoPostProcessorStore)
        self.assertIsInstance(engine.postquestionprocessors_store(), MongoPostQuestionProcessorStore)
        self.assertIsInstance(engine.usergroups_store(), MongoUserGroupsStore)
        self.assertIsInstance(engine.user_store(), MongoUserStore)
        self.assertIsInstance(engine.linked_account_store(), MongoLinkedAccountStore)
        self.assertIsInstance(engine.link_store(), MongoLinkStore)
        self.assertIsInstance(engine.triggers_store(), MongoTriggerStore)
        self.assertIsInstance(engine.oobs_store(), MongoOOBStore)

    @unittest.skipIf(Engines.mongo is False, Engines.mongo_disabled)
    def test_initialise_drop_all_first_false(self):
        config = MongoStorageConfiguration()
        config.drop_all_first = False
        engine = MongoStorageEngine(config)
        engine.initialise()
        self.user_asserts(storage_engine=engine)

    @unittest.skipIf(Engines.mongo is False, Engines.mongo_disabled)
    def test_users(self):
        config = MongoStorageConfiguration()
        engine = MongoStorageEngine(config)
        engine.initialise()
        self.user_asserts(storage_engine=engine)

    @unittest.skipIf(Engines.mongo is False, Engines.mongo_disabled)
    def test_linked_accounts(self):
        config = MongoStorageConfiguration()
        engine = MongoStorageEngine(config)
        engine.initialise()
        self.linked_account_asserts(storage_engine=engine)

    @unittest.skipIf(Engines.mongo is False, Engines.mongo_disabled)
    def test_links(self):
        config = MongoStorageConfiguration()
        engine = MongoStorageEngine(config)
        engine.initialise()
        self.link_asserts(storage_engine=engine)

    @unittest.skipIf(Engines.mongo is False, Engines.mongo_disabled)
    def test_properties(self):
        config = MongoStorageConfiguration()
        engine = MongoStorageEngine(config)
        engine.initialise()
        self.property_asserts(storage_engine=engine)

    @unittest.skipIf(Engines.mongo is False, Engines.mongo_disabled)
    def test_conversations(self):
        config = MongoStorageConfiguration()
        engine = MongoStorageEngine(config)
        engine.initialise()
        self.conversation_asserts(storage_engine=engine)

    @unittest.skipIf(Engines.mongo is False, Engines.mongo_disabled)
    def test_categories(self):
        config = MongoStorageConfiguration()
        engine = MongoStorageEngine(config)
        engine.initialise()
        self.category_asserts(storage_engine=engine)
