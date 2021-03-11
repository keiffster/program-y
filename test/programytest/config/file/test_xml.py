import os

from programy.clients.events.console.config import ConsoleConfiguration
from programy.config.file.xml_file import XMLConfigurationFile
from programy.utils.substitutions.substitues import Substitutions
from programytest.config.file.base_file_tests import ConfigurationBaseFileTests


class XMLConfigurationFileTests(ConfigurationBaseFileTests):

    def test_invalid_file(self):
        config = XMLConfigurationFile()
        self.assertIsNotNone(config.load_from_file("unknown.xml", ConsoleConfiguration(), "."))

    def test_get_methods(self):
        config_data = XMLConfigurationFile()
        self.assertIsNotNone(config_data)
        configuration = config_data.load_from_text("""<?xml version="1.0" encoding="UTF-8" ?>
<root>
	<brain>
		<overrides>
			<allow_system_aiml>true</allow_system_aiml>
			<allow_learn_aiml>true</allow_learn_aiml>
			<allow_learnf_aiml>true</allow_learnf_aiml>
		</overrides>
    </brain>
</root>""", ConsoleConfiguration(), ".")
        self.assertIsNotNone(configuration)

        section = config_data.get_section("brainx")
        self.assertIsNone(section)

        section = config_data.get_section("brain")
        self.assertIsNotNone(section)

        child_section = config_data.get_section("overrides", section)
        self.assertIsNotNone(child_section)

        keys = list(config_data.get_child_section_keys("overrides", section))
        self.assertIsNotNone(keys)
        self.assertEqual(3, len(keys))
        self.assertTrue("allow_system_aiml" in keys)
        self.assertTrue("allow_learn_aiml" in keys)
        self.assertTrue("allow_learnf_aiml" in keys)
        self.assertIsNone(config_data.get_child_section_keys("missing", section))
        self.assertEqual(True, config_data.get_option(child_section, "allow_system_aiml"))
        self.assertEqual(True, config_data.get_option(child_section, "missing", missing_value=True))
        self.assertEqual(True, config_data.get_bool_option(child_section, "allow_system_aiml"))
        self.assertEqual(False, config_data.get_bool_option(child_section, "other_value"))
        self.assertEqual(0, config_data.get_int_option(child_section, "other_value"))

    def test_load_from_file(self):
        xml = XMLConfigurationFile()
        self.assertIsNotNone(xml)

        text_file = os.path.dirname(__file__) + os.sep + "test_xml.xml"

        configuration = xml.load_from_file(text_file,ConsoleConfiguration(), ".")
        self.assertIsNotNone(configuration)
        self.assert_configuration(configuration)

    def test_load_from_text(self):
        xml = XMLConfigurationFile()
        self.assertIsNotNone(xml)

        text_file = os.path.dirname(__file__) + os.sep + "test_xml.xml"

        text = ""
        with open(text_file, "r+") as textfile:
            lines = textfile.readlines()
            for line in lines:
                text += line
                text += "\n"

        configuration = xml.load_from_text(text, ConsoleConfiguration(), ".")

        self.assertIsNotNone(configuration)
        self.assert_configuration(configuration)

    def test_load_from_text_multis_one_value(self):
        xml = XMLConfigurationFile()
        self.assertIsNotNone(xml)
        configuration = xml.load_from_text("""<?xml version="1.0" encoding="UTF-8" ?>
<bot>
    <brain>bot1</brain>
</bot>""", ConsoleConfiguration(), ".")
        self.assertIsNotNone(configuration)

        self.assertEqual(1, len(configuration.client_configuration.configurations[0].configurations))

    def test_load_from_text_multis_multiple_values(self):
        xml = XMLConfigurationFile()
        self.assertIsNotNone(xml)
        configuration = xml.load_from_text("""<?xml version="1.0" encoding="UTF-8" ?>
<root>
	<console>
		<bot>bot1</bot>
		<bot>bot2</bot>
	</console>
	<bot1>
		<brain>brain1</brain>
		<brain>brain2</brain>
	</bot1>
	<bot2>
		<brain>brain1</brain>
		<brain>brain2</brain>
	</bot2>
</root>""", ConsoleConfiguration(), ".")
        self.assertIsNotNone(configuration)

        self.assertEqual(1, len(configuration.client_configuration.configurations[0].configurations))

    def test_load_with_subs(self):
        subs = Substitutions()
        subs.add_substitute("$ALLOW_SYSTEM", True)

        config_data = XMLConfigurationFile()
        self.assertIsNotNone(config_data)
        configuration = config_data.load_from_text("""<?xml version="1.0" encoding="UTF-8" ?>
<root>
	<brain>
		<overrides>
			<allow_system_aiml>true</allow_system_aiml>
			<allow_learn_aiml>true</allow_learn_aiml>
			<allow_learnf_aiml>true</allow_learnf_aiml>
		</overrides>
    </brain>
</root>""", ConsoleConfiguration(), ".")
        self.assertIsNotNone(configuration)

        section = config_data.get_section("brainx")
        self.assertIsNone(section)

        section = config_data.get_section("brain")
        self.assertIsNotNone(section)

        child_section = config_data.get_section("overrides", section)
        self.assertIsNotNone(child_section)

        self.assertEqual(True, config_data.get_option(child_section, "allow_system_aiml"))
        self.assertEqual(True, config_data.get_bool_option(child_section, "allow_system_aiml"))
        self.assertEqual(False, config_data.get_bool_option(child_section, "other_value"))

    def test_get_invalid_values(self):
        config_data = XMLConfigurationFile()
        self.assertIsNotNone(config_data)
        configuration = config_data.load_from_text("""
        <console>
            <section1>
                <section2>
                    <boolvalue>true</boolvalue>
                    <intvalue>23</intvalue>
                    <strvalue>hello</strvalue>
                    <multivalue>
                        <dir>one</dir>
                        <dir>two</dir>
                        <dir>three</dir>
                    </multivalue>
                </section2>
            </section1>
        </console>
                  """, ConsoleConfiguration(), ".")
        self.assertIsNotNone(configuration)

        section = config_data.get_section("section1")
        self.assertIsNotNone(section)

        child_section = config_data.get_section("section2", section)
        self.assertIsNotNone(child_section)

        self.assertEquals(0, config_data.get_int_option(child_section, "boolvalue"))
        self.assertEquals(23, config_data.get_int_option(child_section, "intvalue"))
        self.assertEquals(0, config_data.get_int_option(child_section, "strvalue"))

        self.assertTrue(config_data.get_bool_option(child_section, "boolvalue"))
        self.assertFalse(config_data.get_bool_option(child_section, "intvalue"))
        self.assertFalse(config_data.get_bool_option(child_section, "strvalue"))

        self.assertEquals([], config_data.get_multi_option(child_section, "multivalue2"))
        self.assertEquals([], config_data.get_multi_file_option(child_section, "multivalue2", "."))

    def test_get_multi_option(self):
        config_data = XMLConfigurationFile()
        self.assertIsNotNone(config_data)
        configuration = config_data.load_from_text("""
        <console>
            <section1>
                <multivalue>
                    <dir>one</dir>
                    <dir>two</dir>
                    <dir>three</dir>
                    <dir></dir>
                </multivalue>
            </section1>
        </console>
                  """, ConsoleConfiguration(), ".")
        self.assertIsNotNone(configuration)

        section1 = config_data.get_section("section1")
        self.assertIsNotNone(section1)

        multivalue = config_data.get_section("multivalue", section1)
        self.assertIsNotNone(section1)

        self.assertEquals(['one', 'two', 'three'], config_data.get_multi_option(multivalue, "dir"))

    def test_get_multi_option_no_missing_values(self):
        config_data = XMLConfigurationFile()
        self.assertIsNotNone(config_data)
        configuration = config_data.load_from_text("""
        <console>
            <section1>
                <multivalue>
                    <dir>one</dir>
                    <dir>two</dir>
                    <dir>three</dir>
                    <dir></dir>
                    <other>value</other>
                    <other></other>
                </multivalue>
            </section1>
        </console>
                  """, ConsoleConfiguration(), ".")
        self.assertIsNotNone(configuration)

        section1 = config_data.get_section("section1")
        self.assertIsNotNone(section1)

        multivalue = config_data.get_section("multivalue", section1)
        self.assertIsNotNone(section1)

        self.assertEquals([], config_data.get_multi_option(multivalue, "dirX"))

    def test_get_multi_option_with_missing_values(self):
        config_data = XMLConfigurationFile()
        self.assertIsNotNone(config_data)
        configuration = config_data.load_from_text("""
        <console>
            <section1>
                <multivalue>
                    <dir>one</dir>
                    <dir>two</dir>
                    <dir>three</dir>
                </multivalue>
            </section1>
        </console>
                  """, ConsoleConfiguration(), ".")
        self.assertIsNotNone(configuration)

        section1 = config_data.get_section("section1")
        self.assertIsNotNone(section1)

        multivalue = config_data.get_section("multivalue", section1)
        self.assertIsNotNone(section1)

        self.assertEquals(["X", "Y", "Z"], config_data.get_multi_option(multivalue, "dirX", missing_value=["X", "Y", "Z"]))

    def test_get_multi_file_option(self):
        config_data = XMLConfigurationFile()
        self.assertIsNotNone(config_data)
        configuration = config_data.load_from_text("""
        <console>
            <section1>
                <multivalue>
                    <dir>one</dir>
                    <dir>two</dir>
                    <dir>three</dir>
                </multivalue>
            </section1>
        </console>
                  """, ConsoleConfiguration(), ".")
        self.assertIsNotNone(configuration)

        section1 = config_data.get_section("section1")
        self.assertIsNotNone(section1)

        self.assertEquals(['one', 'two', 'three'], config_data.get_multi_file_option(section1, "multivalue", "."))

    def test_get_multi_file_option_no_missing_value(self):
        config_data = XMLConfigurationFile()
        self.assertIsNotNone(config_data)
        configuration = config_data.load_from_text("""
        <console>
            <section1>
                <multivalue>
                    <dir>one</dir>
                    <dir>two</dir>
                    <dir>three</dir>
                </multivalue>
            </section1>
        </console>
                  """, ConsoleConfiguration(), ".")
        self.assertIsNotNone(configuration)

        section1 = config_data.get_section("section1")
        self.assertIsNotNone(section1)

        self.assertEquals([], config_data.get_multi_file_option(section1, "multivalue2", "."))

    def test_get_multi_file_option_with_missing_value(self):
        config_data = XMLConfigurationFile()
        self.assertIsNotNone(config_data)
        configuration = config_data.load_from_text("""
        <console>
            <section1>
                <multivalue>
                    <dir>one</dir>
                    <dir>two</dir>
                    <dir>three</dir>
                </multivalue>
            </section1>
        </console>
                  """, ConsoleConfiguration(), ".")
        self.assertIsNotNone(configuration)

        section1 = config_data.get_section("section1")
        self.assertIsNotNone(section1)

        self.assertEquals(["file1", "file2", "file3"], config_data.get_multi_file_option(section1, "multivalue2", ".", missing_value=["file1", "file2", "file3"]))

    def test_get_multi_file_option_with_missing_value_as_string(self):
        config_data = XMLConfigurationFile()
        self.assertIsNotNone(config_data)
        configuration = config_data.load_from_text("""
        <console>
            <section1>
                <multivalue>
                    <dir>one</dir>
                    <dir>two</dir>
                    <dir>three</dir>
                </multivalue>
            </section1>
        </console>
                  """, ConsoleConfiguration(), ".")
        self.assertIsNotNone(configuration)

        section1 = config_data.get_section("section1")
        self.assertIsNotNone(section1)

        self.assertEquals(["file1"], config_data.get_multi_file_option(section1, "multivalue2", ".", missing_value="file1"))

    def test_get_multi_option_not_dir(self):
        config_data = XMLConfigurationFile()
        self.assertIsNotNone(config_data)
        configuration = config_data.load_from_text("""
        <console>
            <section1>
                <multivalue>
                    <dir>one</dir>
                    <dir>two</dir>
                    <dir>three</dir>
                    <notdir>four</notdir>
                    <dir></dir>
                </multivalue>
            </section1>
        </console>
                  """, ConsoleConfiguration(), ".")
        self.assertIsNotNone(configuration)

        section1 = config_data.get_section("section1")
        self.assertIsNotNone(section1)

        multivalue = config_data.get_section("multivalue", section1)
        self.assertIsNotNone(section1)

        self.assertEquals(['one', 'two', 'three'], config_data.get_multi_option(multivalue, "dir"))

    def test_get_multi_file_option_not_dir(self):
        config_data = XMLConfigurationFile()
        self.assertIsNotNone(config_data)
        configuration = config_data.load_from_text("""
        <console>
            <section1>
                <multivalue>
                    <dir>one</dir>
                    <dir>two</dir>
                    <dir>three</dir>
                    <notdir>four</notdir>
                    <dir></dir>
                </multivalue>
            </section1>
        </console>
                  """, ConsoleConfiguration(), ".")
        self.assertIsNotNone(configuration)

        section1 = config_data.get_section("section1")
        self.assertIsNotNone(section1)

        multivalue = config_data.get_section("multivalue", section1)
        self.assertIsNotNone(section1)

        self.assertEquals(['one', 'two', 'three'], config_data.get_multi_file_option(section1, "multivalue", "."))

