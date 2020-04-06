import unittest
import unittest.mock

from programy.storage.stores.file.config import FileStorageConfiguration
from programy.storage.stores.file.engine import FileStorageEngine
from programy.storage.stores.file.store.binaries import FileBinariesStore
from programy.storage.stores.file.store.braintree import FileBraintreeStore
from programy.storage.stores.file.store.categories import FileCategoryStore
from programy.storage.stores.file.store.conversations import FileConversationStore
from programy.storage.stores.file.store.duplicates import FileDuplicatesStore
from programy.storage.stores.file.store.errors import FileErrorsStore
from programy.storage.stores.file.store.learnf import FileLearnfStore
from programy.storage.stores.file.store.licensekeys import FileLicenseStore
from programy.storage.stores.file.store.lookups import FileDenormalStore
from programy.storage.stores.file.store.lookups import FileGenderStore
from programy.storage.stores.file.store.lookups import FileNormalStore
from programy.storage.stores.file.store.lookups import FilePerson2Store
from programy.storage.stores.file.store.lookups import FilePersonStore
from programy.storage.stores.file.store.maps import FileMapsStore
from programy.storage.stores.file.store.nodes import FilePatternNodeStore
from programy.storage.stores.file.store.nodes import FileTemplateNodeStore
from programy.storage.stores.file.store.processors import FilePostProcessorsStore
from programy.storage.stores.file.store.processors import FilePostQuestionProcessorsStore
from programy.storage.stores.file.store.processors import FilePreProcessorsStore
from programy.storage.stores.file.store.properties import FileDefaultVariablesStore
from programy.storage.stores.file.store.properties import FilePropertyStore
from programy.storage.stores.file.store.properties import FileRegexStore
from programy.storage.stores.file.store.rdfs import FileRDFStore
from programy.storage.stores.file.store.sets import FileSetsStore
from programy.storage.stores.file.store.spelling import FileSpellingStore
from programy.storage.stores.file.store.twitter import FileTwitterStore
from programy.storage.stores.file.store.usergroups import FileUserGroupStore
from programytest.storage.test_utils import StorageEngineTestUtils
from programy.storage.stores.file.store.triggers import FileTriggersStore
from programy.storage.stores.file.store.oobs import FileOOBStore
from programy.storage.stores.file.store.services import FileServiceStore


class FileStorageEngineTests(StorageEngineTestUtils):

    def test_init_with_configuration(self):
        config = unittest.mock.Mock
        engine = FileStorageEngine(config)
        self.assertIsNotNone(engine)
        self.assertIsNotNone(engine.configuration)

    def test_stores(self):
        config = unittest.mock.Mock
        engine = FileStorageEngine(config)

        self.assertIsInstance(engine.category_store(), FileCategoryStore)
        self.assertIsInstance(engine.errors_store(), FileErrorsStore)
        self.assertIsInstance(engine.duplicates_store(), FileDuplicatesStore)
        self.assertIsInstance(engine.learnf_store(), FileLearnfStore)
        self.assertIsInstance(engine.conversation_store(), FileConversationStore)
        self.assertIsInstance(engine.sets_store(), FileSetsStore)
        self.assertIsInstance(engine.maps_store(), FileMapsStore)
        self.assertIsInstance(engine.rdf_store(), FileRDFStore)
        self.assertIsInstance(engine.denormal_store(), FileDenormalStore)
        self.assertIsInstance(engine.normal_store(), FileNormalStore)
        self.assertIsInstance(engine.gender_store(), FileGenderStore)
        self.assertIsInstance(engine.person_store(), FilePersonStore)
        self.assertIsInstance(engine.person2_store(), FilePerson2Store)
        self.assertIsInstance(engine.regex_store(), FileRegexStore)
        self.assertIsInstance(engine.property_store(), FilePropertyStore)
        self.assertIsInstance(engine.defaults_store(), FileDefaultVariablesStore)
        self.assertIsInstance(engine.twitter_store(), FileTwitterStore)
        self.assertIsInstance(engine.spelling_store(), FileSpellingStore)
        self.assertIsInstance(engine.license_store(), FileLicenseStore)
        self.assertIsInstance(engine.pattern_nodes_store(), FilePatternNodeStore)
        self.assertIsInstance(engine.template_nodes_store(), FileTemplateNodeStore)
        self.assertIsInstance(engine.binaries_store(), FileBinariesStore)
        self.assertIsInstance(engine.braintree_store(), FileBraintreeStore)
        self.assertIsInstance(engine.preprocessors_store(), FilePreProcessorsStore)
        self.assertIsInstance(engine.postprocessors_store(), FilePostProcessorsStore)
        self.assertIsInstance(engine.postquestionprocessors_store(), FilePostQuestionProcessorsStore)
        self.assertIsInstance(engine.usergroups_store(), FileUserGroupStore)
        self.assertIsInstance(engine.triggers_store(), FileTriggersStore)
        self.assertIsInstance(engine.oobs_store(), FileOOBStore)
        self.assertIsInstance(engine.services_store(), FileServiceStore)

    def test_properties(self):
        config = FileStorageConfiguration()
        engine = FileStorageEngine(config)
        engine.initialise()
        self.property_asserts(storage_engine=engine)

    def test_conversations(self):
        config = FileStorageConfiguration()
        engine = FileStorageEngine(config)
        engine.initialise()
        self.conversation_asserts(storage_engine=engine)

    def test_twitter(self):
        config = FileStorageConfiguration()
        engine = FileStorageEngine(config)
        engine.initialise()
        self.twitter_asserts(storage_engine=engine)
