import logging
import os
import os.path

from programy.clients.client import BotClient
from programy.clients.events.console.config import ConsoleConfiguration
from programy.config.programy import ProgramyConfiguration
from programy.storage.factory import StorageFactory
from programy.storage.stores.file.config import FileStorageConfiguration
from programy.storage.stores.file.engine import FileStorageEngine
from programy.storage.stores.file.store.config import FileStoreConfiguration
from programytest.clients.arguments import MockArguments


class TestClient(BotClient):

    def __init__(self, debug=False, level=logging.ERROR):
        if debug is True:
            logging.getLogger().setLevel(level)

        self._file_store_config = FileStorageConfiguration()
        self._storage_engine = FileStorageEngine(self._file_store_config)

        BotClient.__init__(self, "testclient")

    def add_license_keys_store(self, filepath=None):
        if filepath is None:
            filepath = os.path.dirname(__file__) + os.sep + "testdata" + os.sep + "test_licenses.keys"

        self._file_store_config._license_storage = FileStoreConfiguration(file=filepath, fileformat="text",
                                                       encoding="utf-8", delete_on_start=False)
        self.storage_factory._storage_engines[StorageFactory.LICENSE_KEYS] = self._storage_engine
        self.storage_factory._store_to_engine_map[StorageFactory.LICENSE_KEYS] = self._storage_engine

    def add_spelling_store(self):
        self._file_store_config._spelling_storage = FileStoreConfiguration(file=os.path.dirname(__file__) + os.sep + "testdata" + os.sep + "test_corpus.txt", fileformat="text",
                                                       encoding="utf-8", delete_on_start=False)
        self.storage_factory._storage_engines[StorageFactory.SPELLING_CORPUS] = self._storage_engine
        self.storage_factory._store_to_engine_map[StorageFactory.SPELLING_CORPUS] = self._storage_engine

    def add_usergroups_store(self):
        self._file_store_config._usergroups_storage = FileStoreConfiguration(file=os.path.dirname(__file__) + os.sep + "testdata" + os.sep + "test_usergroups.yaml", fileformat="yaml",
                                                       encoding="utf-8", delete_on_start=False)
        self.storage_factory._storage_engines[StorageFactory.USERGROUPS] = self._storage_engine
        self.storage_factory._store_to_engine_map[StorageFactory.USERGROUPS] = self._storage_engine

    def add_categories_store(self, dirs):
        self._file_store_config._categories_storage = FileStoreConfiguration(dirs=dirs, fileformat="xml", extension="aiml", encoding="utf-8", delete_on_start=False)
        self.storage_factory._storage_engines[StorageFactory.CATEGORIES] = self._storage_engine
        self.storage_factory._store_to_engine_map[StorageFactory.CATEGORIES] =  self._storage_engine

    def add_single_categories_store(self, file):
        self._file_store_config._categories_storage = FileStoreConfiguration(file=file, fileformat="xml", extension="aiml", encoding="utf-8", delete_on_start=False)
        self.storage_factory._storage_engines[StorageFactory.CATEGORIES] = self._storage_engine
        self.storage_factory._store_to_engine_map[StorageFactory.CATEGORIES] =  self._storage_engine

    def add_learnf_store(self, dirs):
        self._file_store_config._learnf_storage = FileStoreConfiguration(dirs=dirs, fileformat="xml", extension="aiml", encoding="utf-8", delete_on_start=False)
        self.storage_factory._storage_engines[StorageFactory.LEARNF] = self._storage_engine
        self.storage_factory._store_to_engine_map[StorageFactory.LEARNF] =  self._storage_engine

    def add_sets_store(self, dirs):
        self._file_store_config._sets_storage = FileStoreConfiguration(dirs=dirs, fileformat="text", extension="txt", encoding="utf-8", delete_on_start=False)
        self.storage_factory._storage_engines[StorageFactory.SETS] = self._storage_engine
        self.storage_factory._store_to_engine_map[StorageFactory.SETS] = self._storage_engine

    def add_set_store(self, file):
        self._file_store_config._sets_storage = FileStoreConfiguration(file=file, fileformat="text", extension="txt", encoding="utf-8", delete_on_start=False)
        self.storage_factory._storage_engines[StorageFactory.SETS] = self._storage_engine
        self.storage_factory._store_to_engine_map[StorageFactory.SETS] = self._storage_engine

    def add_maps_store(self, dirs):
        self._file_store_config._maps_storage = FileStoreConfiguration(dirs=dirs, fileformat="text", extension="txt", encoding="utf-8", delete_on_start=False)
        self.storage_factory._storage_engines[StorageFactory.MAPS] = self._storage_engine
        self.storage_factory._store_to_engine_map[StorageFactory.MAPS] = self._storage_engine

    def add_map_store(self, file):
        self._file_store_config._maps_storage = FileStoreConfiguration(file=file, fileformat="text", extension="txt", encoding="utf-8", delete_on_start=False)
        self.storage_factory._storage_engines[StorageFactory.MAPS] = self._storage_engine
        self.storage_factory._store_to_engine_map[StorageFactory.MAPS] = self._storage_engine

    def add_denormal_store(self, file):
        self._file_store_config._denormal_storage = FileStoreConfiguration(dirs=file, fileformat="text", extension="txt", encoding="utf-8", delete_on_start=False)
        self.storage_factory._storage_engines[StorageFactory.DENORMAL] = self._storage_engine
        self.storage_factory._store_to_engine_map[StorageFactory.DENORMAL] = self._storage_engine

    def add_normal_store(self, file):
        self._file_store_config._normal_storage = FileStoreConfiguration(dirs=file, fileformat="text", extension="txt", encoding="utf-8", delete_on_start=False)
        self.storage_factory._storage_engines[StorageFactory.NORMAL] = self._storage_engine
        self.storage_factory._store_to_engine_map[StorageFactory.NORMAL] = self._storage_engine

    def add_person_store(self, file):
        self._file_store_config._person_storage = FileStoreConfiguration(dirs=file, fileformat="text", extension="txt", encoding="utf-8", delete_on_start=False)
        self.storage_factory._storage_engines[StorageFactory.PERSON] = self._storage_engine
        self.storage_factory._store_to_engine_map[StorageFactory.PERSON] = self._storage_engine

    def add_person2_store(self, file):
        self._file_store_config._person2_storage = FileStoreConfiguration(dirs=file, fileformat="text", extension="txt", encoding="utf-8", delete_on_start=False)
        self.storage_factory._storage_engines[StorageFactory.PERSON2] = self._storage_engine
        self.storage_factory._store_to_engine_map[StorageFactory.PERSON2] = self._storage_engine

    def add_gender_store(self, file):
        self._file_store_config._gender_storage = FileStoreConfiguration(file=file, fileformat="text", extension="txt", encoding="utf-8", delete_on_start=False)
        self.storage_factory._storage_engines[StorageFactory.GENDER] = self._storage_engine
        self.storage_factory._store_to_engine_map[StorageFactory.GENDER] = self._storage_engine

    def add_pattern_nodes_store(self, file=None):
        if file is None:
            file = os.path.dirname(__file__) + os.sep + "testdata" + os.sep + "nodes" + os.sep + "test_pattern_nodes.conf"
        self._file_store_config._pattern_nodes_storage = FileStoreConfiguration(file=file, fileformat="text",
                                                       encoding="utf-8", delete_on_start=False)
        self.storage_factory._storage_engines[StorageFactory.PATTERN_NODES] = self._storage_engine
        self.storage_factory._store_to_engine_map[StorageFactory.PATTERN_NODES] = self._storage_engine

    def add_template_nodes_store(self, file=None):
        if file is None:
            file = os.path.dirname(__file__) + os.sep + "testdata" + os.sep + "nodes" + os.sep + "test_template_nodes.conf"
        self._file_store_config._template_nodes_storage = FileStoreConfiguration(file=file, fileformat="text",
                                                       encoding="utf-8", delete_on_start=False)
        self.storage_factory._storage_engines[StorageFactory.TEMPLATE_NODES] = self._storage_engine
        self.storage_factory._store_to_engine_map[StorageFactory.TEMPLATE_NODES] = self._storage_engine

    def add_twitter_store(self):
        self._file_store_config._twitter_storage = FileStoreConfiguration(dirs=os.path.dirname(__file__) + os.sep + "testdata", fileformat="text", encoding="utf-8", delete_on_start=False)
        self.storage_factory._storage_engines[StorageFactory.TWITTER] = self._storage_engine
        self.storage_factory._store_to_engine_map[StorageFactory.TWITTER] = self._storage_engine

    def add_properties_store(self, file):
        self._file_store_config._properties_storage = FileStoreConfiguration(file=file, fileformat="text", encoding="utf-8", delete_on_start=False)
        self.storage_factory._storage_engines[StorageFactory.PROPERTIES] = self._storage_engine
        self.storage_factory._store_to_engine_map[StorageFactory.PROPERTIES] = self._storage_engine

    def add_defaults_store(self, file):
        self._file_store_config._defaults_storage = FileStoreConfiguration(file=file, fileformat="text", encoding="utf-8", delete_on_start=False)
        self.storage_factory._storage_engines[StorageFactory.DEFAULTS] = self._storage_engine
        self.storage_factory._store_to_engine_map[StorageFactory.DEFAULTS] = self._storage_engine

    def add_regex_templates_store(self, file):
        self._file_store_config._regex_storage = FileStoreConfiguration(file=file, fileformat="text", encoding="utf-8", delete_on_start=False)
        self.storage_factory._storage_engines[StorageFactory.REGEX_TEMPLATES] = self._storage_engine
        self.storage_factory._store_to_engine_map[StorageFactory.REGEX_TEMPLATES] = self._storage_engine

    def add_rdfs_store(self, dirs):
        self._file_store_config._rdf_storage = FileStoreConfiguration(dirs=dirs, fileformat="text", extension="txt", encoding="utf-8", delete_on_start=False)
        self.storage_factory._storage_engines[StorageFactory.RDF] = self._storage_engine
        self.storage_factory._store_to_engine_map[StorageFactory.RDF] = self._storage_engine

    def add_rdf_store(self, file):
        self._file_store_config._rdf_storage = FileStoreConfiguration(file=file, fileformat="text", extension="txt", encoding="utf-8", delete_on_start=False)
        self.storage_factory._storage_engines[StorageFactory.RDF] = self._storage_engine
        self.storage_factory._store_to_engine_map[StorageFactory.RDF] = self._storage_engine

    def add_conversation_store(self, dir):
        self._file_store_config._conversation_storage = FileStoreConfiguration(dirs=dir, fileformat="text", extension="txt", encoding="utf-8", delete_on_start=False)
        self.storage_factory._storage_engines[StorageFactory.CONVERSATIONS] = self._storage_engine
        self.storage_factory._store_to_engine_map[StorageFactory.CONVERSATIONS] = self._storage_engine

    def add_debug_stores(self, errors_file, duplicates_file):
        self._file_store_config._errors_storage = FileStoreConfiguration(file=errors_file, fileformat="text",encoding="utf-8", delete_on_start=False)
        self.storage_factory._storage_engines[StorageFactory.ERRORS] = self._storage_engine
        self.storage_factory._store_to_engine_map[StorageFactory.ERRORS] = self._storage_engine

        self._file_store_config._duplicates_storage = FileStoreConfiguration(file=duplicates_file, fileformat="text",encoding="utf-8", delete_on_start=False)
        self.storage_factory._storage_engines[StorageFactory.DUPLICATES] = self._storage_engine
        self.storage_factory._store_to_engine_map[StorageFactory.DUPLICATES] = self._storage_engine

    def add_braintree_store(self, brainfile):
        self._file_store_config._braintree_storage = FileStoreConfiguration(file=brainfile, fileformat="text",encoding="utf-8", delete_on_start=False)
        self.storage_factory._storage_engines[StorageFactory.BRAINTREE] = self._storage_engine
        self.storage_factory._store_to_engine_map[StorageFactory.BRAINTREE] = self._storage_engine

    def add_oobs_store(self, oobsfile):
        self._file_store_config._oobs_storage = FileStoreConfiguration(file=oobsfile, fileformat="text",
                                                       encoding="utf-8", delete_on_start=False)
        self.storage_factory._storage_engines[StorageFactory.OOBS] = self._storage_engine
        self.storage_factory._store_to_engine_map[StorageFactory.OOBS] = self._storage_engine

    def add_services_store(self, dirs):
        self._file_store_config._services_storage = FileStoreConfiguration(dirs=dirs, fileformat="yaml", extension="conf", encoding="utf-8", delete_on_start=False)
        self.storage_factory._storage_engines[StorageFactory.SERVICES] = self._storage_engine
        self.storage_factory._store_to_engine_map[StorageFactory.SERVICES] =  self._storage_engine

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
