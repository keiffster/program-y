import os
import xml.etree.ElementTree as ET

from programy.config.file.xml_file import XMLConfigurationFile
from programy.clients.events.console.config import ConsoleConfiguration
from programy.utils.substitutions.substitues import Substitutions

from programytest.config.file.base_file_tests import ConfigurationBaseFileTests


class XMLConfigurationFileTests(ConfigurationBaseFileTests):

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
        configuration = xml.load_from_file(os.path.dirname(__file__) + os.sep + "test_xml.xml",
                                            ConsoleConfiguration(), ".")
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
		<bot>bot</bot>
	</console>
	<bot>
		<brain>bot1</brain>
		<brain>bot2</brain>
	</bot>
</root>""", ConsoleConfiguration(), ".")
        self.assertIsNotNone(configuration)

        self.assertEqual(2, len(configuration.client_configuration.configurations[0].configurations))

    def test_load_from_text(self):
        xml = XMLConfigurationFile()
        self.assertIsNotNone(xml)
        configuration = xml.load_from_text("""<?xml version="1.0" encoding="UTF-8" ?>
<root>
	<console>
		<bot>bot</bot>
		<prompt>>>></prompt>
		<scheduler>
			<name>Scheduler1</name>
			<debug_level>50</debug_level>
			<add_listeners>false</add_listeners>
			<remove_all_jobs>false</remove_all_jobs>
		</scheduler>
		<storage>
			<entities>
				<users>sql</users>
				<linked_accounts>sql</linked_accounts>
				<links>sql</links>
				<properties>file</properties>
				<conversations>file</conversations>
				<categories>file</categories>
				<maps>file</maps>
				<sets>file</sets>
				<rdf>file</rdf>
				<denormal>file</denormal>
				<normal>file</normal>
				<gender>file</gender>
				<person>file</person>
				<person2>file</person2>
				<twitter>file</twitter>
				<spelling_corpus>file</spelling_corpus>
				<license_keys>file</license_keys>
				<nodes>file</nodes>
				<binaries>file</binaries>
				<braintree>file</braintree>
				<preprocessors>file</preprocessors>
				<postprocessors>file</postprocessors>
				<regex_templates>file</regex_templates>
				<variables>file</variables>
				<usergroups>file</usergroups>
				<learnf>file</learnf>
			</entities>
			<stores>
				<sql>
					<type>sql</type>
					<config>
						<url>sqlite:///:memory</url>
						<echo>false</echo>
						<encoding>utf-8</encoding>
						<create_db>true</create_db>
						<drop_all_first>true</drop_all_first>
					</config>
				</sql>
				<mongo>
					<type>mongo</type>
					<config>
						<url>mongodb://localhost:27017/</url>
						<database>programy</database>
						<drop_all_first>true</drop_all_first>
					</config>
				</mongo>
				<redis>
					<type>redis</type>
					<config>
						<host>localhost</host>
						<port>6379</port>
						<password />
						<db>0</db>
						<prefix>programy</prefix>
						<drop_all_first>true</drop_all_first>
					</config>
				</redis>
				<file>
					<type>file</type>
					<config>
						<category_storage>
							<files>./storage/categories</files>
						</category_storage>
						<conversation_storage>
							<files>./storage/conversations</files>
						</conversation_storage>
						<sets_storage>
							<files>./storage/sets</files>
							<extension>.txt</extension>
							<directories>false</directories>
						</sets_storage>
						<maps_storage>
							<files>./storage/maps</files>
							<extension>.txt</extension>
							<directories>false</directories>
						</maps_storage>
						<regex_templates>
							<files>./storage/regex</files>
						</regex_templates>
						<lookups_storage>
							<files>./storage/lookups</files>
							<extension>.txt</extension>
							<directories>false</directories>
						</lookups_storage>
						<properties_storage>
							<file>./storage/properties.txt</file>
						</properties_storage>
						<defaults_storage>
							<file>./storage/defaults.txt</file>
						</defaults_storage>
						<variables>
							<files>./storage/variables</files>
						</variables>
						<rdf_storage>
							<files>./storage/rdfs</files>
							<extension>.txt</extension>
							<directories>true</directories>
						</rdf_storage>
						<twitter_storage>
							<files>./storage/twitter</files>
						</twitter_storage>
						<spelling_corpus>
							<file>./storage/spelling/corpus.txt</file>
						</spelling_corpus>
						<license_keys>
							<file>./storage/license.keys</file>
						</license_keys>
						<nodes>
							<files>./storage/nodes</files>
						</nodes>
						<binaries>
							<files>./storage/binaries</files>
						</binaries>
						<braintree>
							<file>./storage/braintree/braintree.xml</file>
							<format>xml</format>
						</braintree>
						<preprocessors>
							<file>./storage/processing/preprocessors.txt</file>
						</preprocessors>
						<postprocessors>
							<file>./storage/processing/postprocessing.txt</file>
						</postprocessors>
						<usergroups>
							<files>./storage/security/usergroups.txt</files>
						</usergroups>
						<learnf>
							<files>./storage/categories/learnf</files>
						</learnf>
					</config>
				</file>
				<logger>
					<type>logger</type>
					<config>
						<conversation_logger>conversation</conversation_logger>
					</config>
				</logger>
			</stores>
		</storage>
	</console>
	<voice>
		<license_keys>$BOT_ROOT/config/license.keys</license_keys>
		<tts>osx</tts>
		<stt>azhang</stt>
		<osx>
			<classname>talky.clients.voice.tts.osxsay.OSXSayTextToSpeach</classname>
		</osx>
		<pytts>
			<classname>talky.clients.voice.tts.pyttssay.PyTTSSayTextToSpeach</classname>
			<rate_adjust>10</rate_adjust>
		</pytts>
		<azhang>
			<classname>talky.clients.voice.stt.azhang.AnthonyZhangSpeechToText</classname>
			<ambient_adjust>3</ambient_adjust>
			<service>ibm</service>
		</azhang>
	</voice>
	<rest>
		<host>0.0.0.0</host>
		<port>8989</port>
		<debug>false</debug>
		<workers>4</workers>
		<license_keys>$BOT_ROOT/config/license.keys</license_keys>
	</rest>
	<webchat>
		<host>0.0.0.0</host>
		<port>8090</port>
		<debug>false</debug>
		<license_keys>$BOT_ROOT/config/license.keys</license_keys>
		<api>/api/web/v1.0/ask</api>
	</webchat>
	<twitter>
		<polling>true</polling>
		<polling_interval>49</polling_interval>
		<streaming>false</streaming>
		<use_status>true</use_status>
		<use_direct_message>true</use_direct_message>
		<auto_follow>true</auto_follow>
		<storage>file</storage>
		<welcome_message>Thanks for following me, send me a message and I'll try and help</welcome_message>
		<license_keys>file</license_keys>
	</twitter>
	<xmpp>
		<server>talk.google.com</server>
		<port>5222</port>
		<xep_0030>true</xep_0030>
		<xep_0004>true</xep_0004>
		<xep_0060>true</xep_0060>
		<xep_0199>true</xep_0199>
		<license_keys>file</license_keys>
	</xmpp>
	<socket>
		<host>127.0.0.1</host>
		<port>9999</port>
		<queue>5</queue>
		<debug>true</debug>
		<license_keys>file</license_keys>
	</socket>
	<telegram>
		<unknown_command>Sorry, that is not a command I have been taught yet!</unknown_command>
		<license_keys />
	</telegram>
	<facebook>
		<host>127.0.0.1</host>
		<port>5000</port>
		<debug>false</debug>
		<license_keys>file</license_keys>
	</facebook>
	<twilio>
		<host>127.0.0.1</host>
		<port>5000</port>
		<debug>false</debug>
		<license_keys>file</license_keys>
	</twilio>
	<slack>
		<polling_interval>1</polling_interval>
		<license_keys>file</license_keys>
	</slack>
	<viber>
		<name>Servusai</name>
		<avatar>http://viber.com/avatar.jpg</avatar>
		<license_keys>file</license_keys>
	</viber>
	<line>
		<host>127.0.0.1</host>
		<port>8084</port>
		<debug>false</debug>
		<license_keys>file</license_keys>
	</line>
	<kik>
		<bot_name>servusai</bot_name>
		<webhook>https://93638f7a.ngrok.io/api/kik/v1.0/ask</webhook>
		<host>127.0.0.1</host>
		<port>8082</port>
		<debug>false</debug>
		<license_keys>file</license_keys>
	</kik>
	<bot>
		<brain>brain</brain>
		<initial_question>Hi, how can I help you today?</initial_question>
		<initial_question_srai>YINITIALQUESTION</initial_question_srai>
		<default_response>Sorry, I don't have an answer for that!</default_response>
		<default_response_srai>YEMPTY</default_response_srai>
		<empty_string>YEMPTY</empty_string>
		<exit_response>So long, and thanks for the fish!</exit_response>
		<exit_response_srai>YEXITRESPONSE</exit_response_srai>
		<override_properties>true</override_properties>
		<max_question_recursion>1000</max_question_recursion>
		<max_question_timeout>60</max_question_timeout>
		<max_search_depth>100</max_search_depth>
		<max_search_timeout>60</max_search_timeout>
		<spelling>
			<load>true</load>
			<classname>programy.spelling.norvig.NorvigSpellingChecker</classname>
			<alphabet>ABCDEFGHIJKLMNOPQRSTUVWXYZ</alphabet>
			<check_before>true</check_before>
			<check_and_retry>true</check_and_retry>
		</spelling>
		<conversations>
			<save>true</save>
			<load>false</load>
			<max_histories>100</max_histories>
			<restore_last_topic>false</restore_last_topic>
			<initial_topic>TOPIC1</initial_topic>
			<empty_on_start>false</empty_on_start>
		</conversations>
	</bot>
	<brain>
		<overrides>
			<allow_system_aiml>true</allow_system_aiml>
			<allow_learn_aiml>true</allow_learn_aiml>
			<allow_learnf_aiml>true</allow_learnf_aiml>
		</overrides>
		<defaults>
			<default-get>unknown</default-get>
			<default-property>unknown</default-property>
			<default-map>unknown</default-map>
			<learnf-path>file</learnf-path>
		</defaults>
		<binaries>
			<save_binary>true</save_binary>
			<load_binary>true</load_binary>
			<load_aiml_on_binary_fail>true</load_aiml_on_binary_fail>
		</binaries>
		<braintree>
			<create>true</create>
		</braintree>
		<services>
			<REST>
				<classname>programy.services.rest.GenericRESTService</classname>
				<method>GET</method>
				<host>0.0.0.0</host>
				<port>8080</port>
			</REST>
			<Pannous>
				<classname>programy.services.pannous.PannousService</classname>
				<url>http://weannie.pannous.com/api</url>
			</Pannous>
		</services>
		<security>
			<authentication>
				<classname>programy.security.authenticate.passthrough.BasicPassThroughAuthenticationService</classname>
				<denied_srai>AUTHENTICATION_FAILED</denied_srai>
			</authentication>
			<authorisation>
				<classname>programy.security.authorise.usergroupsauthorisor.BasicUserGroupAuthorisationService</classname>
				<denied_srai>AUTHORISATION_FAILED</denied_srai>
				<usergroups>
					<storage>file</storage>
				</usergroups>
			</authorisation>
		</security>
		<oob>
			<default>
				<classname>programy.oob.defaults.default.DefaultOutOfBandProcessor</classname>
			</default>
			<alarm>
				<classname>programy.oob.defaults.alarm.AlarmOutOfBandProcessor</classname>
			</alarm>
			<camera>
				<classname>programy.oob.defaults.camera.CameraOutOfBandProcessor</classname>
			</camera>
			<clear>
				<classname>programy.oob.defaults.clear.ClearOutOfBandProcessor</classname>
			</clear>
			<dial>
				<classname>programy.oob.defaults.dial.DialOutOfBandProcessor</classname>
			</dial>
			<dialog>
				<classname>programy.oob.defaults.dialog.DialogOutOfBandProcessor</classname>
			</dialog>
			<email>
				<classname>programy.oob.defaults.email.EmailOutOfBandProcessor</classname>
			</email>
			<geomap>
				<classname>programy.oob.defaults.map.MapOutOfBandProcessor</classname>
			</geomap>
			<schedule>
				<classname>programy.oob.defaults.schedule.ScheduleOutOfBandProcessor</classname>
			</schedule>
			<search>
				<classname>programy.oob.defaults.search.SearchOutOfBandProcessor</classname>
			</search>
			<sms>
				<classname>programy.oob.defaults.sms.SMSOutOfBandProcessor</classname>
			</sms>
			<url>
				<classname>programy.oob.defaults.url.URLOutOfBandProcessor</classname>
			</url>
			<wifi>
				<classname>programy.oob.defaults.wifi.WifiOutOfBandProcessor</classname>
			</wifi>
		</oob>
		<dynamic>
			<variables>
				<gettime>programy.dynamic.variables.datetime.GetTime</gettime>
			</variables>
			<sets>
				<numeric>programy.dynamic.sets.numeric.IsNumeric</numeric>
				<roman>programy.dynamic.sets.roman.IsRomanNumeral</roman>
			</sets>
			<maps>
				<romantodec>programy.dynamic.maps.roman.MapRomanToDecimal</romantodec>
				<dectoroman>programy.dynamic.maps.roman.MapDecimalToRoman</dectoroman>
			</maps>
		</dynamic>
	</brain>
</root>""", ConsoleConfiguration(), ".")

        self.assertIsNotNone(configuration)
        self.assert_configuration(configuration)

    def test_load_additionals(self):
        xml = XMLConfigurationFile()
        self.assertIsNotNone(xml)
        configuration = xml.load_from_text("""<?xml version="1.0" encoding="UTF-8" ?>
<root>
	<console>
		<bot>bot</bot>
	</console>
	<bot>
		<brain>brain</brain>
	</bot>
	<brain>
		<services>
			<authentication>
				<classname>programy.services.authenticate.passthrough.PassThroughAuthenticationService</classname>
				<denied_srai>ACCESS_DENIED</denied_srai>
			</authentication>
		</services>
	</brain>
</root>""", ConsoleConfiguration(), ".")

        self.assertIsNotNone(configuration)

        self.assertTrue(
            configuration.client_configuration.configurations[0].configurations[0].services.exists("authentication"))
        auth_service = configuration.client_configuration.configurations[0].configurations[0].services.service(
            "authentication")
        self.assertIsNotNone(auth_service)

        self.assertTrue(auth_service.exists("denied_srai"))
        self.assertEqual("ACCESS_DENIED", auth_service.value("denied_srai"))

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
