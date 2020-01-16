import unittest.mock

from programy.storage.stores.sql.config import SQLStorageConfiguration
from programy.storage.stores.sql.engine import SQLStorageEngine
from programy.storage.stores.sql.store.categories import SQLCategoryStore
from programy.storage.stores.sql.store.conversations import SQLConversationStore
from programy.storage.stores.sql.store.duplicates import SQLDuplicatesStore
from programy.storage.stores.sql.store.errors import SQLErrorsStore
from programy.storage.stores.sql.store.learnf import SQLLearnfStore
from programy.storage.stores.sql.store.licensekeys import SQLLicenseKeysStore
from programy.storage.stores.sql.store.linkedaccounts import SQLLinkedAccountStore
from programy.storage.stores.sql.store.links import SQLLinkStore
from programy.storage.stores.sql.store.lookups import SQLDenormalStore
from programy.storage.stores.sql.store.lookups import SQLGenderStore
from programy.storage.stores.sql.store.lookups import SQLNormalStore
from programy.storage.stores.sql.store.lookups import SQLPerson2Store
from programy.storage.stores.sql.store.lookups import SQLPersonStore
from programy.storage.stores.sql.store.maps import SQLMapsStore
from programy.storage.stores.sql.store.nodes import SQLPatternNodesStore
from programy.storage.stores.sql.store.nodes import SQLTemplateNodesStore
from programy.storage.stores.sql.store.processors import SQLPostProcessorsStore
from programy.storage.stores.sql.store.processors import SQLPostQuestionProcessorsStore
from programy.storage.stores.sql.store.processors import SQLPreProcessorsStore
from programy.storage.stores.sql.store.properties import SQLDefaultVariableStore
from programy.storage.stores.sql.store.properties import SQLPropertyStore
from programy.storage.stores.sql.store.properties import SQLRegexStore
from programy.storage.stores.sql.store.rdfs import SQLRDFsStore
from programy.storage.stores.sql.store.sets import SQLSetsStore
from programy.storage.stores.sql.store.spelling import SQLSpellingStore
from programy.storage.stores.sql.store.twitter import SQLTwitterStore
from programy.storage.stores.sql.store.usergroups import SQLUserGroupStore
from programy.storage.stores.sql.store.users import SQLUserStore
from programy.storage.stores.sql.store.triggers import SQLTriggersStore
from programy.storage.stores.sql.store.oobs import SQLOOBsStore
from programytest.storage.test_utils import StorageEngineTestUtils


class MockSQLStorageEngine(SQLStorageEngine):

    def __init__(self, configuration):
        SQLStorageEngine.__init__(self, configuration)
        self.drop_all = False
        self.create_all = False

    def _drop_all(self):
        self.drop_all = True

    def _create_all(self):
        self.create_all = True

    def _create_session(self):
        pass


class SQLStorageEngineTests(StorageEngineTestUtils):

    def test_init_with_configuration(self):
        config = SQLStorageConfiguration()
        engine = SQLStorageEngine(config)
        self.assertIsNotNone(engine)
        self.assertIsNotNone(engine.configuration)
        self.assertIsNone(engine._session)

    def test_drop_all_false(self):
        config = SQLStorageConfiguration()
        config._drop_all_first = False
        engine = MockSQLStorageEngine(config)
        engine.initialise()
        self.assertFalse(engine.drop_all)

    def test_drop_all_true(self):
        config = SQLStorageConfiguration()
        config._drop_all_first = True
        engine = MockSQLStorageEngine(config)
        engine.initialise()
        self.assertTrue(engine.drop_all)

    def test_create_all_false(self):
        config = SQLStorageConfiguration()
        config._create_db = False
        engine = MockSQLStorageEngine(config)
        engine.initialise()
        self.assertFalse(engine.create_all)

    def test_create_all_true(self):
        config = SQLStorageConfiguration()
        config._create_db = True
        engine = MockSQLStorageEngine(config)
        engine.initialise()
        self.assertTrue(engine.create_all)

    def test_stores(self):
        config = unittest.mock.Mock
        engine = SQLStorageEngine(config)

        self.assertIsInstance(engine.category_store(), SQLCategoryStore)
        self.assertIsInstance(engine.errors_store(), SQLErrorsStore)
        self.assertIsInstance(engine.duplicates_store(), SQLDuplicatesStore)
        self.assertIsInstance(engine.learnf_store(), SQLLearnfStore)
        self.assertIsInstance(engine.conversation_store(), SQLConversationStore)
        self.assertIsInstance(engine.sets_store(), SQLSetsStore)
        self.assertIsInstance(engine.maps_store(), SQLMapsStore)
        self.assertIsInstance(engine.rdf_store(), SQLRDFsStore)
        self.assertIsInstance(engine.denormal_store(), SQLDenormalStore)
        self.assertIsInstance(engine.normal_store(), SQLNormalStore)
        self.assertIsInstance(engine.gender_store(), SQLGenderStore)
        self.assertIsInstance(engine.person_store(), SQLPersonStore)
        self.assertIsInstance(engine.person2_store(), SQLPerson2Store)
        self.assertIsInstance(engine.regex_store(), SQLRegexStore)
        self.assertIsInstance(engine.property_store(), SQLPropertyStore)
        self.assertIsInstance(engine.defaults_store(), SQLDefaultVariableStore)
        self.assertIsInstance(engine.twitter_store(), SQLTwitterStore)
        self.assertIsInstance(engine.spelling_store(), SQLSpellingStore)
        self.assertIsInstance(engine.license_store(), SQLLicenseKeysStore)
        self.assertIsInstance(engine.pattern_nodes_store(), SQLPatternNodesStore)
        self.assertIsInstance(engine.template_nodes_store(), SQLTemplateNodesStore)
        self.assertIsInstance(engine.preprocessors_store(), SQLPreProcessorsStore)
        self.assertIsInstance(engine.postprocessors_store(), SQLPostProcessorsStore)
        self.assertIsInstance(engine.postquestionprocessors_store(), SQLPostQuestionProcessorsStore)
        self.assertIsInstance(engine.usergroups_store(), SQLUserGroupStore)
        self.assertIsInstance(engine.user_store(), SQLUserStore)
        self.assertIsInstance(engine.linked_account_store(), SQLLinkedAccountStore)
        self.assertIsInstance(engine.link_store(), SQLLinkStore)
        self.assertIsInstance(engine.triggers_store(), SQLTriggersStore)
        self.assertIsInstance(engine.oobs_store(), SQLOOBsStore)

    def test_users(self):
        config = SQLStorageConfiguration()
        engine = SQLStorageEngine(config)
        engine.initialise()
        self.user_asserts(engine)

    def test_linked_accounts(self):
        config = SQLStorageConfiguration()
        engine = SQLStorageEngine(config)
        engine.initialise()
        self.linked_account_asserts(engine)

    def test_links(self):
        config = SQLStorageConfiguration()
        engine = SQLStorageEngine(config)
        engine.initialise()
        self.link_asserts(engine)

    def test_properties(self):
        config = SQLStorageConfiguration()
        engine = SQLStorageEngine(config)
        engine.initialise()
        self.property_asserts(engine)

    def test_conversations(self):
        config = SQLStorageConfiguration()
        engine = SQLStorageEngine(config)
        engine.initialise()
        self.conversation_asserts(engine)

    def test_categories(self):
        config = SQLStorageConfiguration()
        engine = SQLStorageEngine(config)
        engine.initialise()
        self.category_asserts(engine)
