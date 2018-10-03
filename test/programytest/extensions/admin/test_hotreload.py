import os
import re
import unittest.mock

from programy.extensions.admin.hotreload import HotReloadAdminExtension
from programy.storage.factory import StorageFactory

from programytest.client import TestClient


class ReloadTestClient(TestClient):

    denormal = None
    normal = None
    gender = None
    person = None
    person2 = None
    properties = None
    defaults = None

    preprocessors = None
    postprocessors = None

    regex_templates = None

    pattern_nodes = None
    template_nodes = None

    aiml_files = None
    set_files = None
    map_files = None
    rdf_files = None

    def __init__(self):
        TestClient.__init__(self)

    def load_storage(self):
        super(ReloadTestClient, self).load_storage()

        self.add_default_stores()

        if ReloadTestClient.denormal is not None:
            self.add_denormal_store(ReloadTestClient.denormal)

        if ReloadTestClient.normal is not None:
            self.add_normal_store(ReloadTestClient.normal)

        if ReloadTestClient.gender is not None:
            self.add_gender_store(ReloadTestClient.gender)

        if ReloadTestClient.person is not None:
            self.add_person_store(ReloadTestClient.person)

        if ReloadTestClient.person2 is not None:
            self.add_person2_store(ReloadTestClient.person2)

        if ReloadTestClient.properties is not None:
            self.add_properties_store(ReloadTestClient.properties)

        if ReloadTestClient.defaults is not None:
            self.add_defaults_store(ReloadTestClient.defaults)

        if ReloadTestClient.regex_templates is not None:
            self.add_regex_templates_store(ReloadTestClient.regex_templates)

        if ReloadTestClient.pattern_nodes is not None:
            self.add_pattern_nodes_store(ReloadTestClient.pattern_nodes)

        if ReloadTestClient.template_nodes is not None:
            self.add_template_nodes_store(ReloadTestClient.template_nodes)

        if ReloadTestClient.aiml_files is not None:
            self.add_categories_store([ReloadTestClient.aiml_files])

        if ReloadTestClient.set_files is not None:
            self.add_sets_store([ReloadTestClient.set_files])

        if ReloadTestClient.map_files is not None:
            self.add_maps_store([ReloadTestClient.map_files])

        if ReloadTestClient.rdf_files is not None:
            self.add_rdfs_store([ReloadTestClient.rdf_files])


class HotReloadAdminExtensionTests(unittest.TestCase):

    def test_hotreload_commands(self):
        extension = HotReloadAdminExtension()
        client = ReloadTestClient()
        client_context = client.create_client_context("testid")
        self.assertEqual("RELOAD [DENORMAL|NORMAL|GENDER|PERSON|PERSON2|PROPERTIES|DEFAULTS|REGEX|PATTERNS|TEMPLATES] | [SET|MAP|RDF] NAME | ALL [AIML|MAPS|SETS|RDFS]", extension.execute(client_context, "COMMANDS"))

    def test_reload_all(self):
        extension = HotReloadAdminExtension()

        client = ReloadTestClient()
        client_context = client.create_client_context("testid")

        result = extension.execute(client_context, "RELOAD ALL")
        self.assertEqual("HOTRELOAD OK", result)

    def test_reload_denormal(self):
        extension = HotReloadAdminExtension()

        ReloadTestClient.denormal = os.path.dirname(__file__) + os.sep + "test_config" + os.sep + "denormal1.txt"

        client = ReloadTestClient()
        client_context = client.create_client_context("testid")

        self.assertIsNotNone(client_context.brain.denormals)
        self.assertTrue(client_context.brain.denormals.has_key(" DOT COM "))
        self.assertFalse(client_context.brain.denormals.has_key(" DOT EDU "))

        lookups_engine = client.storage_factory.entity_storage_engine(StorageFactory.DENORMAL)
        lookups_store = lookups_engine.denormal_store()
        lookups_store.get_storage()._dirs = [os.path.dirname(__file__) + os.sep + "test_config" + os.sep + "denormal2.txt"]

        result = extension.execute(client_context, "RELOAD DENORMAL")
        self.assertEqual("HOTRELOAD OK", result)

        self.assertIsNotNone(client_context.brain.denormals)
        self.assertTrue(client_context.brain.denormals.has_key(" DOT EDU "))
        self.assertFalse(client_context.brain.denormals.has_key(" DOT COM "))

    def test_reload_normal(self):
        extension = HotReloadAdminExtension()

        ReloadTestClient.normal = os.path.dirname(__file__) + os.sep + "test_config" + os.sep + "normal1.txt"

        client = ReloadTestClient()
        client_context = client.create_client_context("testid")

        self.assertIsNotNone(client_context.brain.normals)
        self.assertTrue(client_context.brain.normals.has_key("%20"))
        self.assertFalse(client_context.brain.normals.has_key("%2C"))

        lookups_engine = client.storage_factory.entity_storage_engine(StorageFactory.NORMAL)
        lookups_store = lookups_engine.normal_store()
        lookups_store.get_storage()._dirs = [os.path.dirname(__file__) + os.sep + "test_config" + os.sep + "normal2.txt"]

        result = extension.execute(client_context, "RELOAD NORMAL")
        self.assertEqual("HOTRELOAD OK", result)

        self.assertIsNotNone(client_context.brain.normals)
        self.assertTrue(client_context.brain.normals.has_key("%2C"))
        self.assertFalse(client_context.brain.normals.has_key("%20"))

    def test_reload_gender(self):
        extension = HotReloadAdminExtension()

        ReloadTestClient.gender = os.path.dirname(__file__) + os.sep + "test_config" + os.sep + "gender1.txt"

        client = ReloadTestClient()
        client_context = client.create_client_context("testid")

        self.assertIsNotNone(client_context.brain.genders)
        self.assertTrue(client_context.brain.genders.has_key(" WITH HIM "))
        self.assertFalse(client_context.brain.genders.has_key(" TO HIM "))

        lookups_engine = client.storage_factory.entity_storage_engine(StorageFactory.GENDER)
        lookups_store = lookups_engine.gender_store()
        lookups_store.get_storage()._dirs = [os.path.dirname(__file__) + os.sep + "test_config" + os.sep + "gender2.txt"]

        result = extension.execute(client_context, "RELOAD GENDER")
        self.assertEqual("HOTRELOAD OK", result)

        self.assertIsNotNone(client_context.brain.genders)
        self.assertTrue(client_context.brain.genders.has_key(" TO HIM "))
        self.assertFalse(client_context.brain.genders.has_key(" TO YOU "))

    def test_reload_person(self):
        extension = HotReloadAdminExtension()

        ReloadTestClient.person = os.path.dirname(__file__) + os.sep + "test_config" + os.sep + "person1.txt"

        client = ReloadTestClient()
        client_context = client.create_client_context("testid")

        self.assertIsNotNone(client_context.brain.persons)
        self.assertTrue(client_context.brain.persons.has_key(" WITH YOU "))
        self.assertFalse(client_context.brain.persons.has_key(" TO YOU "))

        lookups_engine = client.storage_factory.entity_storage_engine(StorageFactory.PERSON)
        lookups_store = lookups_engine.person_store()
        lookups_store.get_storage()._dirs = [os.path.dirname(__file__) + os.sep + "test_config" + os.sep + "person2.txt"]

        result = extension.execute(client_context, "RELOAD PERSON")
        self.assertEqual("HOTRELOAD OK", result)

        self.assertIsNotNone(client_context.brain.persons)
        self.assertTrue(client_context.brain.persons.has_key(" TO YOU "))
        self.assertFalse(client_context.brain.persons.has_key(" WITH YOU "))

    def test_reload_person2(self):
        extension = HotReloadAdminExtension()

        ReloadTestClient.person2 = os.path.dirname(__file__) + os.sep + "test_config" + os.sep + "person2_1.txt"

        client = ReloadTestClient()
        client_context = client.create_client_context("testid")

        self.assertIsNotNone(client_context.brain.person2s)
        self.assertTrue(client_context.brain.person2s.has_key(" I WAS "))
        self.assertFalse(client_context.brain.person2s.has_key(" SHE WAS "))

        lookups_engine = client.storage_factory.entity_storage_engine(StorageFactory.PERSON2)
        lookups_store = lookups_engine.person2_store()
        lookups_store.get_storage()._dirs = [os.path.dirname(__file__) + os.sep + "test_config" + os.sep + "person2_2.txt"]

        result = extension.execute(client_context, "RELOAD PERSON2")
        self.assertEqual("HOTRELOAD OK", result)

        self.assertIsNotNone(client_context.brain.person2s)
        self.assertTrue(client_context.brain.person2s.has_key(" SHE WAS "))
        self.assertFalse(client_context.brain.person2s.has_key(" I WAS "))

    def test_reload_properties(self):
        extension = HotReloadAdminExtension()

        ReloadTestClient.properties = os.path.dirname(__file__) + os.sep + "test_config" + os.sep + "properties1.txt"

        client = ReloadTestClient()
        client_context = client.create_client_context("testid")

        self.assertIsNotNone(client_context.brain.properties)
        self.assertTrue(client_context.brain.properties.has_property("name"))
        self.assertEqual("Y-Bot", client_context.brain.properties.property("name"))

        lookups_engine = client.storage_factory.entity_storage_engine(StorageFactory.PROPERTIES)
        lookups_store = lookups_engine.property_store()
        lookups_store.get_storage()._dirs = [os.path.dirname(__file__) + os.sep + "test_config" + os.sep + "properties2.txt"]

        result = extension.execute(client_context, "RELOAD PROPERTIES")
        self.assertEqual("HOTRELOAD OK", result)

        self.assertIsNotNone(client_context.brain.properties)
        self.assertTrue(client_context.brain.properties.has_property("name"))
        self.assertEqual("Y-Bot2", client_context.brain.properties.property("name"))

    def test_reload_defaults(self):
        extension = HotReloadAdminExtension()

        ReloadTestClient.defaults = os.path.dirname(__file__) + os.sep + "test_config" + os.sep + "defaults1.txt"

        client = ReloadTestClient()
        client_context = client.create_client_context("testid")

        self.assertIsNotNone(client_context.brain.default_variables)
        self.assertTrue(client_context.brain.default_variables.has_property("name"))
        self.assertEqual("Y-Bot", client_context.brain.default_variables.property("name"))

        default_variables_engine = client.storage_factory.entity_storage_engine(StorageFactory.DEFAULTS)
        default_variables_store = default_variables_engine.defaults_store()
        default_variables_store.get_storage()._dirs = [os.path.dirname(__file__) + os.sep + "test_config" + os.sep + "defaults2.txt"]

        result = extension.execute(client_context, "RELOAD DEFAULTS")
        self.assertEqual("HOTRELOAD OK", result)

        self.assertIsNotNone(client_context.brain.default_variables)
        self.assertTrue(client_context.brain.default_variables.has_property("name"))
        self.assertEqual("Y-Bot2", client_context.brain.default_variables.property("name"))

    def test_reload_regex(self):
        extension = HotReloadAdminExtension()

        ReloadTestClient.regex_templates = os.path.dirname(__file__) + os.sep + "test_config" + os.sep + "regex-templates1.txt"

        client = ReloadTestClient()
        client_context = client.create_client_context("testid")

        self.assertIsNotNone(client_context.brain.regex_templates)
        self.assertIsNotNone(client_context.brain.regex_templates.has_regex("anything"))
        self.assertEqual(re.compile('^.*$', re.IGNORECASE), client_context.brain.regex_templates.regex("anything"))

        regex_engine = client.storage_factory.entity_storage_engine(StorageFactory.REGEX_TEMPLATES)
        regex_store = regex_engine.regex_store()
        regex_store.get_storage()._dirs = [os.path.dirname(__file__) + os.sep + "test_config" + os.sep + "regex-templates2.txt"]

        result = extension.execute(client_context, "RELOAD REGEX")
        self.assertEqual("HOTRELOAD OK", result)

        self.assertIsNotNone(client_context.brain.regex_templates)
        self.assertIsNotNone(client_context.brain.regex_templates.has_regex("anything"))
        self.assertEqual(re.compile('^.2*$', re.IGNORECASE), client_context.brain.regex_templates.regex("anything"))

    def test_reload_patterns(self):
        extension = HotReloadAdminExtension()

        ReloadTestClient.pattern_nodes = os.path.dirname(__file__) + os.sep + "test_config" + os.sep + "pattern_nodes1.conf"

        client = ReloadTestClient()
        client_context = client.create_client_context("testid")

        self.assertTrue(client_context.brain.aiml_parser.pattern_parser._pattern_factory.exists("word"))

        lookups_engine = client.storage_factory.entity_storage_engine(StorageFactory.PATTERN_NODES)
        lookups_store = lookups_engine.pattern_nodes_store()
        lookups_store.get_storage()._dirs = [os.path.dirname(__file__) + os.sep + "test_config" + os.sep + "pattern_nodes2.conf"]

        result = extension.execute(client_context, "RELOAD PATTERNS")
        self.assertEqual("HOTRELOAD OK", result)

        self.assertFalse(client_context.brain.aiml_parser.pattern_parser._pattern_factory.exists("word"))
        self.assertTrue(client_context.brain.aiml_parser.pattern_parser._pattern_factory.exists("word2"))

    def test_reload_templates(self):
        extension = HotReloadAdminExtension()

        ReloadTestClient.template_nodes = os.path.dirname(__file__) + os.sep + "test_config" + os.sep + "template_nodes1.conf"

        client = ReloadTestClient()
        client_context = client.create_client_context("testid")

        self.assertTrue(client_context.brain.aiml_parser.pattern_parser._pattern_factory.exists("word"))

        lookups_engine = client.storage_factory.entity_storage_engine(StorageFactory.PATTERN_NODES)
        lookups_store = lookups_engine.pattern_nodes_store()
        lookups_store.get_storage()._dirs = [os.path.dirname(__file__) + os.sep + "test_config" + os.sep + "template_nodes2.conf"]

        result = extension.execute(client_context, "RELOAD PATTERNS")
        self.assertEqual("HOTRELOAD OK", result)

        self.assertFalse(client_context.brain.aiml_parser.pattern_parser._pattern_factory.exists("word"))
        self.assertTrue(client_context.brain.aiml_parser.pattern_parser._pattern_factory.exists("word2"))

    def test_reload_maps(self):
        extension = HotReloadAdminExtension()

        ReloadTestClient.map_files = os.path.dirname(__file__) + os.sep + "test_config" + os.sep + "maps1"

        client = ReloadTestClient()
        client_context = client.create_client_context("testid")

        self.assertIsNotNone(client_context.brain.maps)
        self.assertTrue(client_context.brain.maps.contains("animallegs"))
        self.assertTrue(client_context.brain.maps.contains("animalsounds"))
        self.assertFalse(client_context.brain.maps.contains("state2captial"))
        self.assertFalse(client_context.brain.maps.contains("state2largestcity"))

        lookups_engine = client.storage_factory.entity_storage_engine(StorageFactory.MAPS)
        lookups_store = lookups_engine.maps_store()
        lookups_store.get_storage()._dirs = [os.path.dirname(__file__) + os.sep + "test_config" + os.sep + "maps2"]

        result = extension.execute(client_context, "RELOAD ALL MAPS")
        self.assertEqual("HOTRELOAD OK", result)

        self.assertIsNotNone(client_context.brain.maps)
        self.assertFalse(client_context.brain.maps.contains("animallegs"))
        self.assertFalse(client_context.brain.maps.contains("animalsounds"))
        self.assertTrue(client_context.brain.maps.contains("state2capital"))
        self.assertTrue(client_context.brain.maps.contains("state2largestcity"))

    def test_reload_map(self):
        extension = HotReloadAdminExtension()

        ReloadTestClient.map_files = os.path.dirname(__file__) + os.sep + "test_config" + os.sep + "maps1"

        client = ReloadTestClient()
        client_context = client.create_client_context("testid")

        self.assertIsNotNone(client_context.brain.maps)
        self.assertTrue(client_context.brain.maps.contains("animallegs"))
        al_map = client_context.brain.maps.map("animallegs")
        self.assertIsNotNone(al_map)
        self.assertEqual('4', al_map['BUFFALO'])
        al_map['BUFFALO'] = '6'
        self.assertEqual('6', al_map['BUFFALO'])

        result = extension.execute(client_context, "RELOAD MAP ANIMALLEGS")
        self.assertEqual("HOTRELOAD OK", result)

        self.assertIsNotNone(client_context.brain.maps)

        self.assertTrue(client_context.brain.maps.contains("animallegs"))
        al_map = client_context.brain.maps.map("animallegs")
        self.assertIsNotNone(al_map)
        self.assertEqual('4', al_map['BUFFALO'])

    def test_reload_sets(self):
        extension = HotReloadAdminExtension()

        ReloadTestClient.set_files = os.path.dirname(__file__) + os.sep + "test_config" + os.sep + "sets1"

        client = ReloadTestClient()
        client_context = client.create_client_context("testid")

        self.assertIsNotNone(client_context.brain.sets)
        self.assertTrue(client_context.brain.sets.contains("animal"))
        self.assertTrue(client_context.brain.sets.contains("animals"))
        self.assertFalse(client_context.brain.sets.contains("fastfood"))
        self.assertFalse(client_context.brain.sets.contains("food"))

        lookups_engine = client.storage_factory.entity_storage_engine(StorageFactory.SETS)
        lookups_store = lookups_engine.sets_store()
        lookups_store.get_storage()._dirs = [os.path.dirname(__file__) + os.sep + "test_config" + os.sep + "sets2"]

        result = extension.execute(client_context, "RELOAD ALL SETS")
        self.assertEqual("HOTRELOAD OK", result)

        self.assertIsNotNone(client_context.brain.sets)
        self.assertFalse(client_context.brain.sets.contains("animal"))
        self.assertFalse(client_context.brain.sets.contains("animals"))
        self.assertTrue(client_context.brain.sets.contains("fastfood"))
        self.assertTrue(client_context.brain.sets.contains("food"))

    def test_reload_set(self):
        extension = HotReloadAdminExtension()

        ReloadTestClient.set_files = os.path.dirname(__file__) + os.sep + "test_config" + os.sep + "sets1"

        client = ReloadTestClient()
        client_context = client.create_client_context("testid")

        self.assertIsNotNone(client_context.brain.sets)
        self.assertTrue(client_context.brain.sets.contains("animal"))
        set = client_context.brain.sets.set("animal")
        self.assertTrue('BUFFALO' in set)
        del set['BUFFALO']
        self.assertFalse('BUFFALO' in set)

        result = extension.execute(client_context, "RELOAD SET ANIMAL")
        self.assertEqual("HOTRELOAD OK", result)

        self.assertIsNotNone(client_context.brain.sets)
        self.assertTrue(client_context.brain.sets.contains("animal"))
        set = client_context.brain.sets.set("animal")
        self.assertTrue('BUFFALO' in set)

    def test_reload_rdfs(self):
        extension = HotReloadAdminExtension()

        ReloadTestClient.rdf_files = os.path.dirname(__file__) + os.sep + "test_config" + os.sep + "rdfs1"

        client = ReloadTestClient()
        client_context = client.create_client_context("testid")

        self.assertIsNotNone(client_context.brain.rdf)
        self.assertTrue(client_context.brain.rdf.has_subject("ANIMAL"))
        self.assertTrue(client_context.brain.rdf.has_subject("JUPITER"))
        self.assertFalse(client_context.brain.rdf.has_subject("SOUTH"))
        self.assertFalse(client_context.brain.rdf.has_subject("IBM"))

        lookups_engine = client.storage_factory.entity_storage_engine(StorageFactory.RDF)
        lookups_store = lookups_engine.rdf_store()
        lookups_store.get_storage()._dirs = [os.path.dirname(__file__) + os.sep + "test_config" + os.sep + "rdfs2"]

        result = extension.execute(client_context, "RELOAD ALL RDFS")
        self.assertEqual("HOTRELOAD OK", result)

        self.assertIsNotNone(client_context.brain.rdf)
        self.assertFalse(client_context.brain.rdf.has_subject("ANIMAL"))
        self.assertFalse(client_context.brain.rdf.has_subject("JUPITER"))
        self.assertTrue(client_context.brain.rdf.has_subject("SOUTH"))
        self.assertTrue(client_context.brain.rdf.has_subject("IBM"))

    def test_reload_rdf(self):
        extension = HotReloadAdminExtension()

        ReloadTestClient.rdf_files = os.path.dirname(__file__) + os.sep + "test_config" + os.sep + "rdfs1"

        client = ReloadTestClient()
        client_context = client.create_client_context("testid")

        self.assertTrue(client_context.brain.rdf.has_subject('ANTEATER'))
        client_context.brain.rdf.delete_entity('ANTEATER')
        self.assertFalse(client_context.brain.rdf.has_subject('ANTEATER'))

        result = extension.execute(client_context, "RELOAD RDF ANIMAL")
        self.assertEqual("HOTRELOAD OK", result)

        self.assertTrue(client_context.brain.rdf.has_subject('ANTEATER'))

    def test_reload_aimls(self):
        extension = HotReloadAdminExtension()

        ReloadTestClient.aiml_files = os.path.dirname(__file__) + os.sep + "test_config" + os.sep + 'aimls1'

        client = ReloadTestClient()
        client_context = client.create_client_context("testid")

        self.assertEqual("That was test 1.", client_context.bot.ask_question(client_context, "TEST1"))
        self.assertEqual("That was test 2.", client_context.bot.ask_question(client_context, "TEST2"))

        category_engine = client.storage_factory.entity_storage_engine(StorageFactory.CATEGORIES)
        category_store = category_engine.category_store()
        category_store.get_storage()._dirs = [os.path.dirname(__file__) + os.sep + "test_config" + os.sep + 'aimls2']

        result = extension.execute(client_context, "RELOAD ALL AIML")
        self.assertEqual("HOTRELOAD OK", result)

        self.assertEqual("That was test 3.", client_context.bot.ask_question(client_context, "TEST3"))
        self.assertEqual("That was test 4.", client_context.bot.ask_question(client_context, "TEST4"))
