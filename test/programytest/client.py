import logging
import os
import os.path
from programy.clients.client import BotClient
from programy.config.programy import ProgramyConfiguration
from programy.clients.events.console.config import ConsoleConfiguration
from programy.storage.stores.file.config import FileStorageConfiguration
from programy.storage.stores.file.store.config import FileStoreConfiguration
from programy.storage.stores.file.engine import FileStorageEngine
from programy.storage.factory import StorageFactory
from programytest.clients.arguments import MockArguments


class TestClient(BotClient):

    def __init__(self, debug=False, level=logging.ERROR):
        if debug is True:
            logging.getLogger().setLevel(level)

        self._file_store_config = FileStorageConfiguration()
        self._storage_engine = FileStorageEngine(self._file_store_config)

        BotClient.__init__(self, "testclient")

    def add_license_keys_store(self):
        self._file_store_config._license_storage = FileStoreConfiguration(file=os.path.dirname(__file__) + os.sep + "testdata" + os.sep + "test_licenses.keys", format="text",
                                                       encoding="utf-8", delete_on_start=False)
        self.storage_factory._storage_engines[StorageFactory.LICENSE_KEYS] = self._storage_engine
        self.storage_factory._store_to_engine_map[StorageFactory.LICENSE_KEYS] = self._storage_engine
        self.load_license_keys()

    def add_spelling_store(self):
        self._file_store_config._spelling_storage = FileStoreConfiguration(file=os.path.dirname(__file__) + os.sep + "testdata" + os.sep + "test_corpus.txt", format="text",
                                                       encoding="utf-8", delete_on_start=False)
        self.storage_factory._storage_engines[StorageFactory.SPELLING_CORPUS] = self._storage_engine
        self.storage_factory._store_to_engine_map[StorageFactory.SPELLING_CORPUS] = self._storage_engine

    def add_usergroups_store(self):
        self._file_store_config._usergroups_storage = FileStoreConfiguration(file=os.path.dirname(__file__) + os.sep + "testdata" + os.sep + "test_usergroups.yaml", format="yaml",
                                                       encoding="utf-8", delete_on_start=False)
        self.storage_factory._storage_engines[StorageFactory.USERGROUPS] = self._storage_engine
        self.storage_factory._store_to_engine_map[StorageFactory.USERGROUPS] = self._storage_engine

    def add_categories_store(self, dirs):
        self._file_store_config._categories_storage = FileStoreConfiguration(dirs=dirs, format="xml", extension="aiml", encoding="utf-8", delete_on_start=False)
        self.storage_factory._storage_engines[StorageFactory.CATEGORIES] = self._storage_engine
        self.storage_factory._store_to_engine_map[StorageFactory.CATEGORIES] =  self._storage_engine

    def add_single_categories_store(self, file):
        self._file_store_config._categories_storage = FileStoreConfiguration(file=file, format="xml", extension="aiml", encoding="utf-8", delete_on_start=False)
        self.storage_factory._storage_engines[StorageFactory.CATEGORIES] = self._storage_engine
        self.storage_factory._store_to_engine_map[StorageFactory.CATEGORIES] =  self._storage_engine

    def add_learnf_store(self, dirs):
        self._file_store_config._learnf_storage = FileStoreConfiguration(dirs=dirs, format="xml", extension="aiml", encoding="utf-8", delete_on_start=False)
        self.storage_factory._storage_engines[StorageFactory.LEARNF] = self._storage_engine
        self.storage_factory._store_to_engine_map[StorageFactory.LEARNF] =  self._storage_engine

    def add_sets_store(self, dirs):
        self._file_store_config._sets_storage = FileStoreConfiguration(dirs=dirs, format="text", extension="txt", encoding="utf-8", delete_on_start=False)
        self.storage_factory._storage_engines[StorageFactory.SETS] = self._storage_engine
        self.storage_factory._store_to_engine_map[StorageFactory.SETS] = self._storage_engine

    def add_set_store(self, file):
        self._file_store_config._sets_storage = FileStoreConfiguration(file=file, format="text", extension="txt", encoding="utf-8", delete_on_start=False)
        self.storage_factory._storage_engines[StorageFactory.SETS] = self._storage_engine
        self.storage_factory._store_to_engine_map[StorageFactory.SETS] = self._storage_engine

    def add_maps_store(self, dirs):
        self._file_store_config._maps_storage = FileStoreConfiguration(dirs=dirs, format="text", extension="txt", encoding="utf-8", delete_on_start=False)
        self.storage_factory._storage_engines[StorageFactory.MAPS] = self._storage_engine
        self.storage_factory._store_to_engine_map[StorageFactory.MAPS] = self._storage_engine

    def add_map_store(self, file):
        self._file_store_config._maps_storage = FileStoreConfiguration(file=file, format="text", extension="txt", encoding="utf-8", delete_on_start=False)
        self.storage_factory._storage_engines[StorageFactory.MAPS] = self._storage_engine
        self.storage_factory._store_to_engine_map[StorageFactory.MAPS] = self._storage_engine

    def add_denormal_store(self, file):
        self._file_store_config._denormal_storage = FileStoreConfiguration(dirs=file, format="text", extension="txt", encoding="utf-8", delete_on_start=False)
        self.storage_factory._storage_engines[StorageFactory.DENORMAL] = self._storage_engine
        self.storage_factory._store_to_engine_map[StorageFactory.DENORMAL] = self._storage_engine

    def add_normal_store(self, file):
        self._file_store_config._normal_storage = FileStoreConfiguration(dirs=file, format="text", extension="txt", encoding="utf-8", delete_on_start=False)
        self.storage_factory._storage_engines[StorageFactory.NORMAL] = self._storage_engine
        self.storage_factory._store_to_engine_map[StorageFactory.NORMAL] = self._storage_engine

    def add_person_store(self, file):
        self._file_store_config._person_storage = FileStoreConfiguration(dirs=file, format="text", extension="txt", encoding="utf-8", delete_on_start=False)
        self.storage_factory._storage_engines[StorageFactory.PERSON] = self._storage_engine
        self.storage_factory._store_to_engine_map[StorageFactory.PERSON] = self._storage_engine

    def add_person2_store(self, file):
        self._file_store_config._person2_storage = FileStoreConfiguration(dirs=file, format="text", extension="txt", encoding="utf-8", delete_on_start=False)
        self.storage_factory._storage_engines[StorageFactory.PERSON2] = self._storage_engine
        self.storage_factory._store_to_engine_map[StorageFactory.PERSON2] = self._storage_engine

    def add_gender_store(self, file):
        self._file_store_config._gender_storage = FileStoreConfiguration(file=file, format="text", extension="txt", encoding="utf-8", delete_on_start=False)
        self.storage_factory._storage_engines[StorageFactory.GENDER] = self._storage_engine
        self.storage_factory._store_to_engine_map[StorageFactory.GENDER] = self._storage_engine

    def add_pattern_nodes_store(self, file=None):
        if file is None:
            file = os.path.dirname(__file__) + os.sep + "testdata" + os.sep + "nodes" + os.sep + "test_pattern_nodes.txt"
        self._file_store_config._pattern_nodes_storage = FileStoreConfiguration(file=file, format="text",
                                                       encoding="utf-8", delete_on_start=False)
        self.storage_factory._storage_engines[StorageFactory.PATTERN_NODES] = self._storage_engine
        self.storage_factory._store_to_engine_map[StorageFactory.PATTERN_NODES] = self._storage_engine

    def add_template_nodes_store(self, file=None):
        if file is None:
            file = os.path.dirname(__file__) + os.sep + "testdata" + os.sep + "nodes" + os.sep + "test_template_nodes.txt"
        self._file_store_config._template_nodes_storage = FileStoreConfiguration(file=file, format="text",
                                                       encoding="utf-8", delete_on_start=False)
        self.storage_factory._storage_engines[StorageFactory.TEMPLATE_NODES] = self._storage_engine
        self.storage_factory._store_to_engine_map[StorageFactory.TEMPLATE_NODES] = self._storage_engine

    def add_twitter_store(self):
        self._file_store_config._twitter_storage = FileStoreConfiguration(dirs=os.path.dirname(__file__) + os.sep + "testdata", format="text", encoding="utf-8", delete_on_start=False)
        self.storage_factory._storage_engines[StorageFactory.TWITTER] = self._storage_engine
        self.storage_factory._store_to_engine_map[StorageFactory.TWITTER] = self._storage_engine

    def add_properties_store(self, file):
        self._file_store_config._properties_storage = FileStoreConfiguration(file=file, format="text", encoding="utf-8", delete_on_start=False)
        self.storage_factory._storage_engines[StorageFactory.PROPERTIES] = self._storage_engine
        self.storage_factory._store_to_engine_map[StorageFactory.PROPERTIES] = self._storage_engine

    def add_defaults_store(self, file):
        self._file_store_config._defaults_storage = FileStoreConfiguration(file=file, format="text", encoding="utf-8", delete_on_start=False)
        self.storage_factory._storage_engines[StorageFactory.DEFAULTS] = self._storage_engine
        self.storage_factory._store_to_engine_map[StorageFactory.DEFAULTS] = self._storage_engine

    def add_regex_templates_store(self, file):
        self._file_store_config._regex_storage = FileStoreConfiguration(file=file, format="text", encoding="utf-8", delete_on_start=False)
        self.storage_factory._storage_engines[StorageFactory.REGEX_TEMPLATES] = self._storage_engine
        self.storage_factory._store_to_engine_map[StorageFactory.REGEX_TEMPLATES] = self._storage_engine

    def add_rdfs_store(self, dirs):
        self._file_store_config._rdf_storage = FileStoreConfiguration(dirs=dirs, format="text", extension="txt", encoding="utf-8", delete_on_start=False)
        self.storage_factory._storage_engines[StorageFactory.RDF] = self._storage_engine
        self.storage_factory._store_to_engine_map[StorageFactory.RDF] = self._storage_engine

    def add_rdf_store(self, file):
        self._file_store_config._rdf_storage = FileStoreConfiguration(file=file, format="text", extension="txt", encoding="utf-8", delete_on_start=False)
        self.storage_factory._storage_engines[StorageFactory.RDF] = self._storage_engine
        self.storage_factory._store_to_engine_map[StorageFactory.RDF] = self._storage_engine

    def add_conversation_store(self, dir):
        self._file_store_config._conversation_storage = FileStoreConfiguration(dirs=dir, format="text", extension="txt", encoding="utf-8", delete_on_start=False)
        self.storage_factory._storage_engines[StorageFactory.CONVERSATIONS] = self._storage_engine
        self.storage_factory._store_to_engine_map[StorageFactory.CONVERSATIONS] = self._storage_engine

    def add_default_stores(self):
        self.add_license_keys_store()
        self.add_spelling_store()
        self.add_usergroups_store()
        self.add_pattern_nodes_store()
        self.add_template_nodes_store()

    def parse_arguments(self, argument_parser):
        return MockArguments()

    def initiate_logging(self, arguments):
        pass

    def get_client_configuration(self):
        return ConsoleConfiguration()

    def load_configuration(self, arguments):
        config = ConsoleConfiguration()
        self._configuration = ProgramyConfiguration(config)

    def set_environment(self):
        """For testing purposes we do nothing"""
        return

    def run(self):
        """For testing purposes we do nothing"""
        return

    def dump_graph(self, client_context):
        client_context.brain.aiml_parser.pattern_parser.root.dump("", output_func=print)
