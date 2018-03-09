import os

from programy.config.file.xml_file import XMLConfigurationFile
from programy.clients.events.console.config import ConsoleConfiguration

from programytest.config.file.base_file_tests import ConfigurationBaseFileTests


class XMLConfigurationFileTests(ConfigurationBaseFileTests):

    def test_get_methods(self):
        config_data = XMLConfigurationFile()
        self.assertIsNotNone(config_data)
        configuration = config_data.load_from_text("""
<root>
	<brain>
		<overrides>
			<allow_system_aiml>true</allow_system_aiml>
			<allow_learn_aiml>true</allow_learn_aiml>
			<allow_learnf_aiml>true</allow_learnf_aiml>
			<int_value>999</int_value>
		</overrides>
	</brain>
</root>
          """, ConsoleConfiguration(), ".")
        self.assertIsNotNone(configuration)

        section = config_data.get_section("brainx")
        self.assertIsNone(section)

        section = config_data.get_section("brain")
        self.assertIsNotNone(section)

        child_section = config_data.get_section("overrides", section)
        self.assertIsNotNone(child_section)

        keys = list(config_data.get_child_section_keys("overrides", section))
        self.assertIsNotNone(keys)
        self.assertEqual(4, len(keys))
        self.assertTrue("allow_system_aiml" in keys)
        self.assertTrue("allow_learn_aiml" in keys)
        self.assertTrue("allow_learnf_aiml" in keys)
        self.assertIsNone(config_data.get_child_section_keys("missing", section))
        self.assertEqual(True, config_data.get_option(child_section, "allow_system_aiml"))
        self.assertEqual(True, config_data.get_option(child_section, "missing", missing_value=True))
        self.assertEqual(True, config_data.get_bool_option(child_section, "allow_system_aiml"))
        self.assertEqual(False, config_data.get_bool_option(child_section, "other_value"))
        self.assertEqual(999, config_data.get_int_option(child_section, "int_value"))
        self.assertEqual(0, config_data.get_int_option(child_section, "other_value"))

    def test_load_from_file(self):
        xml = XMLConfigurationFile()
        self.assertIsNotNone(xml)
        configuration = xml.load_from_file(os.path.dirname(__file__)+ os.sep + "test_xml.xml", ConsoleConfiguration(), ".")
        self.assertIsNotNone(configuration)
        self.assert_configuration(configuration)

    def test_load_from_text_single_files(self):
        xml = XMLConfigurationFile()
        self.assertIsNotNone(xml)
        configuration=xml.load_from_text("""<?xml version="1.0" encoding="UTF-8" ?>
<root>
	<brain>
		<files>
			<aiml>
				<files>$BOT_ROOT/test-aiml</files>
				<extension>.test-aiml</extension>
				<directories>true</directories>
				<errors>/tmp/y-bot_errors.txt</errors>
				<duplicates>/tmp/y-bot_duplicates.txt</duplicates>
				<conversation>/tmp/y-bot_conversation.txt</conversation>
			</aiml>
			<sets>
				<files>$BOT_ROOT/test-sets</files>
				<extension>.test-txt</extension>
				<directories>true</directories>
			</sets>
			<maps>
				<files>$BOT_ROOT/test-maps</files>
				<extension>.test-txt</extension>
				<directories>true</directories>
			</maps>
		</files>
	</brain>
</root>
        """, ConsoleConfiguration(), ".")

        self.assertIsNotNone(configuration)

        self.assertTrue(configuration.client_configuration.configurations[0].configurations[0].files.aiml_files.has_multiple_files())
        self.assertFalse(configuration.client_configuration.configurations[0].configurations[0].files.aiml_files.has_single_file())

        self.assertEqual(configuration.client_configuration.configurations[0].configurations[0].files.aiml_files.files, ["./test-aiml"])
        self.assertEqual(configuration.client_configuration.configurations[0].configurations[0].files.set_files.files, ["./test-sets"])
        self.assertEqual(configuration.client_configuration.configurations[0].configurations[0].files.map_files.files, ["./test-maps"])

    def test_load_from_text_multi_files(self):
        xml = XMLConfigurationFile()
        self.assertIsNotNone(xml)
        configuration=xml.load_from_text("""<?xml version="1.0" encoding="UTF-8" ?>
<root>
	<brain>
		<files>
			<aiml>
				<files>
				    <dir>$BOT_ROOT/test-aiml</dir>
				    <dir>$BOT_ROOT/my-aiml</dir>
				</files>
				<extension>.test-aiml</extension>
				<directories>true</directories>
				<errors>/tmp/y-bot_errors.txt</errors>
				<duplicates>/tmp/y-bot_duplicates.txt</duplicates>
				<conversation>/tmp/y-bot_conversation.txt</conversation>
			</aiml>
			<sets>
				<files>$BOT_ROOT/test-sets</files>
				<extension>.test-txt</extension>
				<directories>true</directories>
			</sets>
			<maps>
				<files>$BOT_ROOT/test-maps</files>
				<extension>.test-txt</extension>
				<directories>true</directories>
			</maps>
		</files>
	</brain>
</root>
        """, ConsoleConfiguration(), ".")

        self.assertIsNotNone(configuration)

        self.assertTrue(configuration.client_configuration.configurations[0].configurations[0].files.aiml_files.has_multiple_files())
        self.assertFalse(configuration.client_configuration.configurations[0].configurations[0].files.aiml_files.has_single_file())

        self.assertEqual(configuration.client_configuration.configurations[0].configurations[0].files.aiml_files.files, ["./test-aiml", "./my-aiml"])
        self.assertEqual(configuration.client_configuration.configurations[0].configurations[0].files.set_files.files, ["./test-sets"])
        self.assertEqual(configuration.client_configuration.configurations[0].configurations[0].files.map_files.files, ["./test-maps"])

    def test_load_from_text_single_file(self):
        xml = XMLConfigurationFile()
        self.assertIsNotNone(xml)
        configuration=xml.load_from_text("""<?xml version="1.0" encoding="UTF-8" ?>
<root>
	<brain>
		<files>
			<aiml>
				<file>$BOT_ROOT/test-aiml/test.aiml</file>
				<extension>.test-aiml</extension>
				<directories>true</directories>
				<errors>/tmp/y-bot_errors.txt</errors>
				<duplicates>/tmp/y-bot_duplicates.txt</duplicates>
				<conversation>/tmp/y-bot_conversation.txt</conversation>
			</aiml>
			<sets>
				<files>$BOT_ROOT/test-sets</files>
				<extension>.test-txt</extension>
				<directories>true</directories>
			</sets>
			<maps>
				<files>$BOT_ROOT/test-maps</files>
				<extension>.test-txt</extension>
				<directories>true</directories>
			</maps>
		</files>
	</brain>
</root>
        """, ConsoleConfiguration(), ".")

        self.assertIsNotNone(configuration)

        self.assertFalse(configuration.client_configuration.configurations[0].configurations[0].files.aiml_files.has_multiple_files())
        self.assertTrue(configuration.client_configuration.configurations[0].configurations[0].files.aiml_files.has_single_file())

        self.assertEqual(configuration.client_configuration.configurations[0].configurations[0].files.aiml_files.file, "./test-aiml/test.aiml")
        self.assertEqual(configuration.client_configuration.configurations[0].configurations[0].files.set_files.files, ["./test-sets"])
        self.assertEqual(configuration.client_configuration.configurations[0].configurations[0].files.map_files.files, ["./test-maps"])

    def test_load_from_text(self):
        xml = XMLConfigurationFile()
        self.assertIsNotNone(xml)
        configuration=xml.load_from_text("""<?xml version="1.0" encoding="UTF-8" ?>
<root>
	<brain>
		<overrides>
			<allow_system_aiml>true</allow_system_aiml>
			<allow_learn_aiml>true</allow_learn_aiml>
			<allow_learnf_aiml>true</allow_learnf_aiml>
		</overrides>
		<defaults>
			<default-get>test_unknown</default-get>
			<default-property>test_unknown</default-property>
			<default-map>test_unknown</default-map>
			<learn-filename>test-learnf.aiml</learn-filename>
		</defaults>
		<nodes>
			<pattern_nodes>$BOT_ROOT/config/test_pattern_nodes.conf</pattern_nodes>
			<template_nodes>$BOT_ROOT/config/test_template_nodes.conf</template_nodes>
		</nodes>
		<binaries>
			<save_binary>true</save_binary>
			<load_binary>true</load_binary>
			<binary_filename>/tmp/y-bot.brain</binary_filename>
			<load_aiml_on_binary_fail>true</load_aiml_on_binary_fail>
		</binaries>
        <braintree>
              <file>/tmp/braintree.xml</file>
              <content>xml</content>
        </braintree>
		<files>
			<aiml>
				<files>$BOT_ROOT/test-aiml</files>
				<extension>.test-aiml</extension>
				<directories>true</directories>
				<errors>/tmp/y-bot_errors.txt</errors>
				<duplicates>/tmp/y-bot_duplicates.txt</duplicates>
				<conversation>/tmp/y-bot_conversation.txt</conversation>
			</aiml>
			<sets>
				<files>$BOT_ROOT/test-sets</files>
				<extension>.test-txt</extension>
				<directories>true</directories>
			</sets>
			<maps>
				<files>$BOT_ROOT/test-maps</files>
				<extension>.test-txt</extension>
				<directories>true</directories>
			</maps>
			<denormal>$BOT_ROOT/config/test-denormal.txt</denormal>
			<normal>$BOT_ROOT/config/test-normal.txt</normal>
			<gender>$BOT_ROOT/config/test-gender.txt</gender>
			<person>$BOT_ROOT/config/test-person.txt</person>
			<person2>$BOT_ROOT/config/test-person2.txt</person2>
			<predicates>$BOT_ROOT/config/test-predicates.txt</predicates>
			<pronouns>$BOT_ROOT/config/test-pronouns.txt</pronouns>
			<properties>$BOT_ROOT/config/test-properties.txt</properties>
			<triples>$BOT_ROOT/config/test-triples.txt</triples>
			<preprocessors>$BOT_ROOT/config/test-preprocessors.conf</preprocessors>
			<postprocessors>$BOT_ROOT/config/test-postprocessors.conf</postprocessors>
			<regex_templates>$BOT_ROOT/config/regex-templates.txt</regex_templates>
		</files>
		<services>
			<REST>
				<classname>programy.services.rest.GenericRESTService</classname>
				<method>GET</method>
				<host>0.0.0.0</host>
			</REST>
			<Pannous>
				<classname>programy.services.pannous.PannousService</classname>
				<url>http://weannie.pannous.com/api</url>
			</Pannous>
			<Pandora>
				<classname>programy.services.pandora.PandoraService</classname>
				<url>http://www.pandorabots.com/pandora/talk-xml</url>
			</Pandora>
			<Wikipedia>
				<classname>programy.services.wikipediaservice.WikipediaService</classname>
			</Wikipedia>
		</services>
	</brain>
	<bot>
		<license_keys>$BOT_ROOT/config/test-license.keys</license_keys>
		<prompt>TEST>>></prompt>
		<initial_question>Hi, how can I help you test today?</initial_question>
		<default_response>Sorry, I don't have a test answer for that!</default_response>
		<empty_string>TEST-YEMPTY</empty_string>
		<exit_response>So long, and thanks for the test fish!</exit_response>
		<override_properties>true</override_properties>
		<max_question_recursion>1000</max_question_recursion>
        <max_question_timeout>60</max_question_timeout>
        <max_search_depth>100</max_search_depth>
        <max_search_timeout>60</max_search_timeout>
		<spelling>
			<classname>programy.spelling.checker.TestSpellingChecker</classname>
			<corpus>$BOT_ROOT/spelling/test-corpus.txt</corpus>
			<check_before>true</check_before>
			<check_and_retry>true</check_and_retry>
		</spelling>
	</bot>
	<rest>
		<host>127.0.0.1</host>
		<port>5000</port>
		<debug>false</debug>
	</rest>
	<webchat>
		<host>127.0.0.1</host>
		<port>5000</port>
		<debug>false</debug>
	</webchat>
	<twitter>
		<polling>true</polling>
		<polling_interval>49</polling_interval>
		<streaming>false</streaming>
		<use_status>true</use_status>
		<use_direct_message>true</use_direct_message>
		<auto_follow>true</auto_follow>
		<storage>file</storage>
		<storage_location>$BOT_ROOT/storage/twitter.data</storage_location>
		<welcome_message>Thanks for following me, send me a message and I'll try and help</welcome_message>
	</twitter>
	<facebook>
		<polling>false</polling>
		<polling_interval>30</polling_interval>
		<streaming>true</streaming>
	</facebook>
	<xmpp>
		<server>talk.google.com</server>
		<port>5222</port>
		<xep_0030>true</xep_0030>
		<xep_0004>true</xep_0004>
		<xep_0060>true</xep_0060>
		<xep_0199>true</xep_0199>
	</xmpp>
</root>
            """, ConsoleConfiguration(), ".")

        self.assertIsNotNone(configuration)
        self.assert_configuration(configuration)
