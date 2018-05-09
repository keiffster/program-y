import os
import re
import unittest.mock

from programy.extensions.admin.hotreload import HotReloadAdminExtension

from programytest.aiml_tests.client import TestClient


class ReloadTestClient(TestClient):

    denormal = None
    normal = None
    gender = None
    person = None
    person2 = None
    properties = None
    variables = None

    preprocessors = None
    postprocessors = None

    regex_templates = None

    pattern_nodes = None
    template_nodes = None

    aiml_files = None
    set_files = None
    set_file = None
    map_files = None
    map_file = None
    rdf_files = None
    rdf_file = None

    def __init__(self):
        TestClient.__init__(self)

    def load_configuration(self, arguments):
        super(ReloadTestClient, self).load_configuration(arguments)

        if ReloadTestClient.denormal is not None:
            self.configuration.client_configuration.configurations[0].configurations[0].files._denormal = ReloadTestClient.denormal

        if ReloadTestClient.normal is not None:
            self.configuration.client_configuration.configurations[0].configurations[0].files._normal = ReloadTestClient.normal

        if ReloadTestClient.gender is not None:
            self.configuration.client_configuration.configurations[0].configurations[0].files._gender = ReloadTestClient.gender

        if ReloadTestClient.person is not None:
            self.configuration.client_configuration.configurations[0].configurations[0].files._person = ReloadTestClient.person

        if ReloadTestClient.person2 is not None:
            self.configuration.client_configuration.configurations[0].configurations[0].files._person2 = ReloadTestClient.person2

        if ReloadTestClient.properties is not None:
            self.configuration.client_configuration.configurations[0].configurations[0].files._properties = ReloadTestClient.properties

        if ReloadTestClient.variables is not None:
            self.configuration.client_configuration.configurations[0].configurations[0].files._variables = ReloadTestClient.variables

        if ReloadTestClient.regex_templates is not None:
            self.configuration.client_configuration.configurations[0].configurations[0].files._regex_templates = ReloadTestClient.regex_templates

        if ReloadTestClient.pattern_nodes is not None:
            self.configuration.client_configuration.configurations[0].configurations[0].nodes._pattern_nodes = ReloadTestClient.pattern_nodes

        if ReloadTestClient.template_nodes is not None:
            self.configuration.client_configuration.configurations[0].configurations[0].nodes._template_nodes = ReloadTestClient.template_nodes

        if ReloadTestClient.aiml_files is not None:
            self.configuration.client_configuration.configurations[0].configurations[0].files._aiml_files._files =[ReloadTestClient.aiml_files]
            self.configuration.client_configuration.configurations[0].configurations[0].files._aiml_files._extension = ".aiml"
            self.configuration.client_configuration.configurations[0].configurations[0].files._aiml_files._directories = False

        if ReloadTestClient.set_files is not None:
            self.configuration.client_configuration.configurations[0].configurations[0].files._set_files._files = [ReloadTestClient.set_files]
            self.configuration.client_configuration.configurations[0].configurations[0].files._set_files._extension = ".txt"
            self.configuration.client_configuration.configurations[0].configurations[0].files._set_files._directories = False

        if ReloadTestClient.set_file is not None:
            self.configuration.client_configuration.configurations[0].configurations[0].files.set_files._file = ReloadTestClient.set_file

        if ReloadTestClient.map_files is not None:
            self.configuration.client_configuration.configurations[0].configurations[0].files._map_files._files = [ReloadTestClient.map_files]
            self.configuration.client_configuration.configurations[0].configurations[0].files._map_files._extension = ".txt"
            self.configuration.client_configuration.configurations[0].configurations[0].files._map_files._directories = False

        if ReloadTestClient.map_file is not None:
            self.configuration.client_configuration.configurations[0].configurations[0].files.map_files._file = ReloadTestClient.map_file

        if ReloadTestClient.rdf_files is not None:
            self.configuration.client_configuration.configurations[0].configurations[0].files._rdf_files._files = [ReloadTestClient.rdf_files]
            self.configuration.client_configuration.configurations[0].configurations[0].files._rdf_files._extension = ".txt"
            self.configuration.client_configuration.configurations[0].configurations[0].files._rdf_files._directories = False

        if ReloadTestClient.rdf_files is not None:
            self.configuration.client_configuration.configurations[0].configurations[0].files.rdf_files._file = ReloadTestClient.rdf_file


class HotReloadAdminExtensionTests(unittest.TestCase):

    def test_hotreload_commands(self):
        extension = HotReloadAdminExtension()
        client = ReloadTestClient()
        client_context = client.create_client_context("testid")
        self.assertEquals("RELOAD [DENORMAL|NORMAL|GENDER|PERSON|PERSON2|PROPERTIES|DEFAULTS|REGEX|PATTERNS|TEMPLATES] | [SET|MAP|RDF] NAME | ALL [AIML|MAPS|SETS|RDFS]", extension.execute(client_context, "COMMANDS"))

    def test_reload_all(self):
        extension = HotReloadAdminExtension()

        client = ReloadTestClient()
        client_context = client.create_client_context("testid")

        result = extension.execute(client_context, "RELOAD ALL")
        self.assertEquals("HOTRELOAD OK", result)

    def test_reload_denormal(self):
        extension = HotReloadAdminExtension()

        ReloadTestClient.denormal = os.path.dirname(__file__) + os.sep + "test_config" + os.sep + "denormal1.txt"

        client = ReloadTestClient()
        client_context = client.create_client_context("testid")

        self.assertIsNotNone(client_context.brain.denormals)
        self.assertTrue(client_context.brain.denormals.has_key(" dot com "))
        self.assertFalse(client_context.brain.denormals.has_key(" dot edu "))

        client_context.brain.configuration.files._denormal = os.path.dirname(__file__) + os.sep + "test_config" + os.sep + "denormal2.txt"

        result = extension.execute(client_context, "RELOAD DENORMAL")
        self.assertEquals("HOTRELOAD OK", result)

        self.assertIsNotNone(client_context.brain.denormals)
        self.assertTrue(client_context.brain.denormals.has_key(" dot edu "))
        self.assertFalse(client_context.brain.denormals.has_key(" dot com "))

    def test_reload_normal(self):
        extension = HotReloadAdminExtension()

        ReloadTestClient.normal = os.path.dirname(__file__) + os.sep + "test_config" + os.sep + "normal1.txt"

        client = ReloadTestClient()
        client_context = client.create_client_context("testid")

        self.assertIsNotNone(client_context.brain.normals)
        self.assertTrue(client_context.brain.normals.has_key("%20"))
        self.assertFalse(client_context.brain.normals.has_key("%2C"))

        client_context.brain.configuration.files._normal = os.path.dirname(__file__) + os.sep + "test_config" + os.sep + "normal2.txt"

        result = extension.execute(client_context, "RELOAD NORMAL")
        self.assertEquals("HOTRELOAD OK", result)

        self.assertIsNotNone(client_context.brain.normals)
        self.assertTrue(client_context.brain.normals.has_key("%2C"))
        self.assertFalse(client_context.brain.normals.has_key("%20"))

    def test_reload_gender(self):
        extension = HotReloadAdminExtension()

        ReloadTestClient.gender = os.path.dirname(__file__) + os.sep + "test_config" + os.sep + "gender1.txt"

        client = ReloadTestClient()
        client_context = client.create_client_context("testid")

        self.assertIsNotNone(client_context.brain.genders)
        self.assertTrue(client_context.brain.genders.has_key(" with him "))
        self.assertFalse(client_context.brain.genders.has_key(" to him "))

        client_context.brain.configuration.files._gender = os.path.dirname(__file__) + os.sep + "test_config" + os.sep + "gender2.txt"

        result = extension.execute(client_context, "RELOAD GENDER")
        self.assertEquals("HOTRELOAD OK", result)

        self.assertIsNotNone(client_context.brain.genders)
        self.assertTrue(client_context.brain.genders.has_key(" to him "))
        self.assertFalse(client_context.brain.genders.has_key(" to you "))

    def test_reload_person(self):
        extension = HotReloadAdminExtension()

        ReloadTestClient.person = os.path.dirname(__file__) + os.sep + "test_config" + os.sep + "person1.txt"

        client = ReloadTestClient()
        client_context = client.create_client_context("testid")

        self.assertIsNotNone(client_context.brain.persons)
        self.assertTrue(client_context.brain.persons.has_key(" with you "))
        self.assertFalse(client_context.brain.persons.has_key(" to you "))

        client_context.brain.configuration.files._person = os.path.dirname(__file__) + os.sep + "test_config" + os.sep + "person2.txt"

        result = extension.execute(client_context, "RELOAD PERSON")
        self.assertEquals("HOTRELOAD OK", result)

        self.assertIsNotNone(client_context.brain.persons)
        self.assertTrue(client_context.brain.persons.has_key(" to you "))
        self.assertFalse(client_context.brain.persons.has_key(" with you "))

    def test_reload_person2(self):
        extension = HotReloadAdminExtension()

        ReloadTestClient.person2 = os.path.dirname(__file__) + os.sep + "test_config" + os.sep + "person2_1.txt"

        client = ReloadTestClient()
        client_context = client.create_client_context("testid")

        self.assertIsNotNone(client_context.brain.person2s)
        self.assertTrue(client_context.brain.person2s.has_key(" I was "))
        self.assertFalse(client_context.brain.person2s.has_key(" she was "))

        client_context.brain.configuration.files._person2 = os.path.dirname(__file__) + os.sep + "test_config" + os.sep + "person2_2.txt"

        result = extension.execute(client_context, "RELOAD PERSON2")
        self.assertEquals("HOTRELOAD OK", result)

        self.assertIsNotNone(client_context.brain.person2s)
        self.assertTrue(client_context.brain.person2s.has_key(" she was "))
        self.assertFalse(client_context.brain.person2s.has_key(" I was "))

    def test_reload_properties(self):
        extension = HotReloadAdminExtension()

        ReloadTestClient.properties = os.path.dirname(__file__) + os.sep + "test_config" + os.sep + "properties1.txt"

        client = ReloadTestClient()
        client_context = client.create_client_context("testid")

        self.assertIsNotNone(client_context.brain.properties)
        self.assertTrue(client_context.brain.properties.has_property("name"))
        self.assertEquals("Y-Bot", client_context.brain.properties.property("name"))

        client_context.brain.configuration.files._properties = os.path.dirname(__file__) + os.sep + "test_config" + os.sep + "properties2.txt"

        result = extension.execute(client_context, "RELOAD PROPERTIES")
        self.assertEquals("HOTRELOAD OK", result)

        self.assertIsNotNone(client_context.brain.properties)
        self.assertTrue(client_context.brain.properties.has_property("name"))
        self.assertEquals("Y-Bot2", client_context.brain.properties.property("name"))

    def test_reload_defaults(self):
        extension = HotReloadAdminExtension()

        ReloadTestClient.variables = os.path.dirname(__file__) + os.sep + "test_config" + os.sep + "variables1.txt"

        client = ReloadTestClient()
        client_context = client.create_client_context("testid")

        self.assertIsNotNone(client_context.brain.variables)
        self.assertTrue(client_context.brain.variables.has_property("name"))
        self.assertEquals("Y-Bot", client_context.brain.variables.property("name"))

        client_context.brain.configuration.files._variables = os.path.dirname(__file__) + os.sep + "test_config" + os.sep + "variables2.txt"

        result = extension.execute(client_context, "RELOAD DEFAULTS")
        self.assertEquals("HOTRELOAD OK", result)

        self.assertIsNotNone(client_context.brain.variables)
        self.assertTrue(client_context.brain.variables.has_property("name"))
        self.assertEquals("Y-Bot2", client_context.brain.variables.property("name"))

    def test_reload_regex(self):
        extension = HotReloadAdminExtension()

        ReloadTestClient.regex_templates = os.path.dirname(__file__) + os.sep + "test_config" + os.sep + "regex-templates1.txt"

        client = ReloadTestClient()
        client_context = client.create_client_context("testid")

        self.assertIsNotNone(client_context.brain.regex_templates)
        self.assertIsNotNone(client_context.brain.regex_templates["anything"])
        self.assertEquals(re.compile('^.*$', re.IGNORECASE), client_context.brain.regex_templates["anything"])

        client_context.brain.configuration.files._regex_templates = os.path.dirname(__file__) + os.sep + "test_config" + os.sep +  "regex-templates2.txt"

        result = extension.execute(client_context, "RELOAD REGEX")
        self.assertEquals("HOTRELOAD OK", result)

        self.assertIsNotNone(client_context.brain.regex_templates)
        self.assertIsNotNone(client_context.brain.regex_templates["anything"])
        self.assertEquals(re.compile('^.2*$', re.IGNORECASE), client_context.brain.regex_templates["anything"])

    def test_reload_patterns(self):
        extension = HotReloadAdminExtension()

        ReloadTestClient.pattern_nodes = os.path.dirname(__file__) + os.sep + "test_config" + os.sep + "pattern_nodes1.conf"

        client = ReloadTestClient()
        client_context = client.create_client_context("testid")

        self.assertTrue(client_context.brain.aiml_parser.pattern_parser._pattern_factory.exists("word"))

        client_context.brain.aiml_parser.brain.configuration.nodes._pattern_nodes = os.path.dirname(__file__) + os.sep + "test_config" + os.sep + "pattern_nodes2.conf"

        result = extension.execute(client_context, "RELOAD PATTERNS")
        self.assertEquals("HOTRELOAD OK", result)

        self.assertFalse(client_context.brain.aiml_parser.pattern_parser._pattern_factory.exists("word"))
        self.assertTrue(client_context.brain.aiml_parser.pattern_parser._pattern_factory.exists("word2"))

    def test_reload_templates(self):
        extension = HotReloadAdminExtension()

        ReloadTestClient.template_nodes = os.path.dirname(__file__) + os.sep + "test_config" + os.sep + "pattern_nodes1.conf"

        client = ReloadTestClient()
        client_context = client.create_client_context("testid")

        self.assertTrue(client_context.brain.aiml_parser.pattern_parser._pattern_factory.exists("word"))

        client_context.brain.aiml_parser.brain.configuration.nodes._pattern_nodes = os.path.dirname(__file__) + os.sep + "test_config" + os.sep + "pattern_nodes2.conf"

        result = extension.execute(client_context, "RELOAD PATTERNS")
        self.assertEquals("HOTRELOAD OK", result)

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

        client_context.client.configuration.client_configuration.configurations[0].configurations[0].files._map_files._files = [os.path.dirname(__file__) + os.sep + "test_config" + os.sep + "maps2"]

        result = extension.execute(client_context, "RELOAD ALL MAPS")
        self.assertEquals("HOTRELOAD OK", result)

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
        self.assertEquals('4', al_map['BUFFALO'])
        al_map['BUFFALO'] = '6'
        self.assertEquals('6', al_map['BUFFALO'])

        result = extension.execute(client_context, "RELOAD MAP ANIMALLEGS")
        self.assertEquals("HOTRELOAD OK", result)

        self.assertIsNotNone(client_context.brain.maps)
        self.assertTrue(client_context.brain.maps.contains("animallegs"))
        al_map = client_context.brain.maps.map("animallegs")
        self.assertIsNotNone(al_map)
        self.assertEquals('4', al_map['BUFFALO'])

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

        client_context.client.configuration.client_configuration.configurations[0].configurations[0].files._set_files._files = [os.path.dirname(__file__) + os.sep + "test_config" + os.sep + "sets2"]

        result = extension.execute(client_context, "RELOAD ALL SETS")
        self.assertEquals("HOTRELOAD OK", result)

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
        self.assertEquals("HOTRELOAD OK", result)

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

        client_context.client.configuration.client_configuration.configurations[0].configurations[0].files._rdf_files._files = [os.path.dirname(__file__) + os.sep + "test_config" + os.sep + "rdfs2"]

        result = extension.execute(client_context, "RELOAD ALL RDFS")
        self.assertEquals("HOTRELOAD OK", result)

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
        self.assertEquals("HOTRELOAD OK", result)

        self.assertTrue(client_context.brain.rdf.has_subject('ANTEATER'))

    def test_reload_aimls(self):
        extension = HotReloadAdminExtension()

        ReloadTestClient.aiml_files = os.path.dirname(__file__) + os.sep + "test_config" + os.sep + 'aimls1'

        client = ReloadTestClient()
        client_context = client.create_client_context("testid")

        self.assertEquals("That was test 1", client_context.bot.ask_question(client_context, "TEST1"))
        self.assertEquals("That was test 2", client_context.bot.ask_question(client_context, "TEST2"))

        client_context.client.configuration.client_configuration.configurations[0].configurations[0].files._aiml_files._files = [os.path.dirname(__file__) + os.sep + "test_config" + os.sep + 'aimls2']

        result = extension.execute(client_context, "RELOAD ALL AIML")
        self.assertEquals("HOTRELOAD OK", result)

        self.assertEquals("That was test 3", client_context.bot.ask_question(client_context, "TEST3"))
        self.assertEquals("That was test 4", client_context.bot.ask_question(client_context, "TEST4"))
