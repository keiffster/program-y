import os

from programy.config.file.json_file import JSONConfigurationFile
from programy.clients.events.console.config import ConsoleConfiguration

from programytest.config.file.base_file_tests import ConfigurationBaseFileTests

class JsonConfigurationFileTests(ConfigurationBaseFileTests):

    def test_get_methods(self):
        config_data = JSONConfigurationFile()
        self.assertIsNotNone(config_data)
        configuration = config_data.load_from_text("""
        {
        	"brain": {
        		"overrides": {
        			"allow_system_aiml": true,
        			"allow_learn_aiml": true,
        			"allow_learnf_aiml": true,
        			"int_value": 999
        		}
        	}
        }
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
        json = JSONConfigurationFile()
        self.assertIsNotNone(json)
        configuration = json.load_from_file(os.path.dirname(__file__)+ os.sep + "test_json.json", ConsoleConfiguration(), ".")
        self.assertIsNotNone(configuration)
        self.assert_configuration(configuration)

    def test_load_from_text_single_files(self):
        json = JSONConfigurationFile()
        self.assertIsNotNone(json)
        configuration = json.load_from_text("""
{
	"brain": {
		"files": {
			"aiml": {
				"files": "$BOT_ROOT/test-aiml",
				"extension": ".test-aiml",
				"directories": true,
				"errors": "/tmp/y-bot_errors.txt",
				"duplicates": "/tmp/y-bot_duplicates.txt",
				"conversation": "/tmp/y-bot_conversation.txt"
			},
			"sets": {
				"files": "$BOT_ROOT/test-sets",
				"extension": ".test-txt",
				"directories": true
			},
			"maps": {
				"files": "$BOT_ROOT/test-maps",
				"extension": ".test-txt",
				"directories": true
			}
		}
	}
}
        """, ConsoleConfiguration(), ".")
        self.assertIsNotNone(configuration)

        self.assertTrue(configuration.client_configuration.configurations[0].configurations[0].files.aiml_files.has_multiple_files())
        self.assertFalse(configuration.client_configuration.configurations[0].configurations[0].files.aiml_files.has_single_file())

        self.assertEqual(configuration.client_configuration.configurations[0].configurations[0].files.aiml_files.files, ["./test-aiml"])
        self.assertEqual(configuration.client_configuration.configurations[0].configurations[0].files.set_files.files, ["./test-sets"])
        self.assertEqual(configuration.client_configuration.configurations[0].configurations[0].files.map_files.files, ["./test-maps"])

    def test_load_from_text_multi_files(self):
        json = JSONConfigurationFile()
        self.assertIsNotNone(json)
        configuration = json.load_from_text("""
        {
        	"brain": {
        		"files": {
        			"aiml": {
        				"files": ["$BOT_ROOT/test-aiml", "/my-aiml/test.aiml"],
        				"extension": ".test-aiml",
        				"directories": true,
        				"errors": "/tmp/y-bot_errors.txt",
        				"duplicates": "/tmp/y-bot_duplicates.txt",
        				"conversation": "/tmp/y-bot_conversation.txt"
        			},
        			"sets": {
        				"files": "$BOT_ROOT/test-sets",
        				"extension": ".test-txt",
        				"directories": true
        			},
        			"maps": {
        				"files": "$BOT_ROOT/test-maps",
        				"extension": ".test-txt",
        				"directories": true
        			}
        		}
        	}
        }
                """, ConsoleConfiguration(), ".")
        self.assertIsNotNone(configuration)

        self.assertTrue(configuration.client_configuration.configurations[0].configurations[0].files.aiml_files.has_multiple_files())
        self.assertFalse(configuration.client_configuration.configurations[0].configurations[0].files.aiml_files.has_single_file())

        self.assertEqual(configuration.client_configuration.configurations[0].configurations[0].files.aiml_files.files, ['./test-aiml', '/my-aiml/test.aiml'])
        self.assertEqual(configuration.client_configuration.configurations[0].configurations[0].files.set_files.files, ["./test-sets"])
        self.assertEqual(configuration.client_configuration.configurations[0].configurations[0].files.map_files.files, ["./test-maps"])

    def test_load_from_text_single_file(self):
        json = JSONConfigurationFile()
        self.assertIsNotNone(json)
        configuration = json.load_from_text("""
    {
    	"brain": {
    		"files": {
    			"aiml": {
    				"file": "$BOT_ROOT/test-aiml/test.aiml",
    				"extension": ".test-aiml",
    				"directories": true,
    				"errors": "/tmp/y-bot_errors.txt",
    				"duplicates": "/tmp/y-bot_duplicates.txt",
    				"conversation": "/tmp/y-bot_conversation.txt"
    			},
    			"sets": {
    				"files": ["$BOT_ROOT/test-sets"],
    				"extension": ".test-txt",
    				"directories": true
    			},
    			"maps": {
    				"files": ["$BOT_ROOT/test-maps"],
    				"extension": ".test-txt",
    				"directories": true
    			}
    		}
    	}
    }
            """, ConsoleConfiguration(), ".")
        self.assertIsNotNone(configuration)

        self.assertFalse(configuration.client_configuration.configurations[0].configurations[0].files.aiml_files.has_multiple_files())
        self.assertTrue(configuration.client_configuration.configurations[0].configurations[0].files.aiml_files.has_single_file())

        self.assertEqual(configuration.client_configuration.configurations[0].configurations[0].files.aiml_files.file, "./test-aiml/test.aiml")
        self.assertEqual(configuration.client_configuration.configurations[0].configurations[0].files.set_files.files, ["./test-sets"])
        self.assertEqual(configuration.client_configuration.configurations[0].configurations[0].files.map_files.files, ["./test-maps"])

    def test_load_from_text(self):
        json = JSONConfigurationFile()
        self.assertIsNotNone(json)
        configuration = json.load_from_text("""
{
	"brain": {
		"overrides": {
			"allow_system_aiml": true,
			"allow_learn_aiml": true,
			"allow_learnf_aiml": true
		},
		"defaults": {
			"default-get": "test_unknown",
			"default-property": "test_unknown",
			"default-map": "test_unknown",
			"learn-filename": "test-learnf.aiml"
		},
		"nodes": {
			"pattern_nodes": "$BOT_ROOT/config/test_pattern_nodes.conf",
			"template_nodes": "$BOT_ROOT/config/test_template_nodes.conf"
		},
		"binaries": {
			"save_binary": true,
			"load_binary": true,
			"binary_filename": "/tmp/y-bot.brain",
			"load_aiml_on_binary_fail": true
		},
        "braintree": {
              "file": "/tmp/braintree.xml",
              "content": "xml"
        },
		"files": {
			"aiml": {
				"files": "$BOT_ROOT/test-aiml",
				"extension": ".test-aiml",
				"directories": true,
				"errors": "/tmp/y-bot_errors.txt",
				"duplicates": "/tmp/y-bot_duplicates.txt",
				"conversation": "/tmp/y-bot_conversation.txt"
			},
			"sets": {
				"files": "$BOT_ROOT/test-sets",
				"extension": ".test-txt",
				"directories": true
			},
			"maps": {
				"files": "$BOT_ROOT/test-maps",
				"extension": ".test-txt",
				"directories": true
			},
			"denormal": "$BOT_ROOT/config/test-denormal.txt",
			"normal": "$BOT_ROOT/config/test-normal.txt",
			"gender": "$BOT_ROOT/config/test-gender.txt",
			"person": "$BOT_ROOT/config/test-person.txt",
			"person2": "$BOT_ROOT/config/test-person2.txt",
			"predicates": "$BOT_ROOT/config/test-predicates.txt",
			"pronouns": "$BOT_ROOT/config/test-pronouns.txt",
			"properties": "$BOT_ROOT/config/test-properties.txt",
			"triples": "$BOT_ROOT/config/test-triples.txt",
			"preprocessors": "$BOT_ROOT/config/test-preprocessors.conf",
			"postprocessors": "$BOT_ROOT/config/test-postprocessors.conf",
			"regex_templates": "$BOT_ROOT/config/regex-templates.txt"
		},
		"services": {
			"REST": {
				"classname": "programy.services.rest.GenericRESTService",
				"method": "GET",
				"host": "0.0.0.0"
			},
			"Pannous": {
				"classname": "programy.services.pannous.PannousService",
				"url": "http://weannie.pannous.com/api"
			},
			"Pandora": {
				"classname": "programy.services.pandora.PandoraService",
				"url": "http://www.pandorabots.com/pandora/talk-xml"
			},
			"Wikipedia": {
				"classname": "programy.services.wikipediaservice.WikipediaService"
			}
		}
	},
	"bot": {
		"license_keys": "$BOT_ROOT/config/test-license.keys",
		"prompt": "TEST>>>",
		"initial_question": "Hi, how can I help you test today?",
		"default_response": "Sorry, I don't have a test answer for that!",
		"empty_string": "TEST-YEMPTY",
		"exit_response": "So long, and thanks for the test fish!",
		"override_properties": true,
        "max_question_recursion": 1000,
        "max_question_timeout": 60,
        "max_search_depth": 100,
        "max_search_timeout": 60,
		"spelling": {
			"classname": "programy.spelling.checker.TestSpellingChecker",
			"corpus": "$BOT_ROOT/spelling/test-corpus.txt",
			"check_before": true,
			"check_and_retry": true
		}
	},
	"rest": {
		"host": "127.0.0.1",
		"port": 5000,
		"debug": false
	},
	"webchat": {
		"host": "127.0.0.1",
		"port": 5000,
		"debug": false
	},
	"twitter": {
		"polling": true,
		"polling_interval": 49,
		"streaming": false,
		"use_status": true,
		"use_direct_message": true,
		"auto_follow": true,
		"storage": "file",
		"storage_location": "$BOT_ROOT/storage/twitter.data",
		"welcome_message": "Thanks for following me, send me a message and I'll try and help"
	},
	"facebook": {
		"polling": false,
		"polling_interval": 30,
		"streaming": true
	},
	"xmpp": {
		"server": "talk.google.com",
		"port": 5222,
		"xep_0030": true,
		"xep_0004": true,
		"xep_0060": true,
		"xep_0199": true
	}
}
        """, ConsoleConfiguration(), ".")
        self.assertIsNotNone(configuration)
        self.assert_configuration(configuration)



