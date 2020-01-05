import os

from programy.clients.events.console.config import ConsoleConfiguration
from programy.config.file.json_file import JSONConfigurationFile
from programy.utils.substitutions.substitues import Substitutions
from programytest.config.file.base_file_tests import ConfigurationBaseFileTests


class JSONConfigurationFileTests(ConfigurationBaseFileTests):

    def test_invalid_file(self):
        config = JSONConfigurationFile()
        self.assertIsNotNone(config.load_from_file("unknown.json", ConsoleConfiguration(), "."))

    def test_get_methods(self):
        config_data = JSONConfigurationFile()
        self.assertIsNotNone(config_data)
        configuration = config_data.load_from_text("""
        {"brain": {
            "overrides": {
                  "allow_system_aiml": true,
                  "allow_learn_aiml": true,
                  "allow_learnf_aiml": true
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

    def test_get_invalid_values(self):
        config_data = JSONConfigurationFile()
        self.assertIsNotNone(config_data)
        configuration = config_data.load_from_text("""
        {"section1": {
            "section2": {
                  "boolvalue": true,
                  "intvalue": 23,
                  "strvalue": "hello",
                  "multivalue": [ "one", "two", "three" ]
                  }
              }
        }
                  """, ConsoleConfiguration(), ".")
        self.assertIsNotNone(configuration)

        section = config_data.get_section("section1")
        self.assertIsNotNone(section)

        child_section = config_data.get_section("section2", section)
        self.assertIsNotNone(child_section)

        self.assertEquals(1, config_data.get_int_option(child_section, "boolvalue"))
        self.assertEquals(23, config_data.get_int_option(child_section, "intvalue"))
        self.assertEquals(0, config_data.get_int_option(child_section, "strvalue"))

        self.assertTrue(config_data.get_bool_option(child_section, "boolvalue"))
        self.assertTrue(config_data.get_bool_option(child_section, "intvalue"))
        self.assertTrue(config_data.get_bool_option(child_section, "strvalue"))

        self.assertEquals(['one', 'two', 'three'], config_data.get_multi_option(child_section, "multivalue"))
        self.assertEquals([True], config_data.get_multi_option(child_section, "boolvalue"))
        self.assertEquals([23], config_data.get_multi_option(child_section, "intvalue"))
        self.assertEquals(["hello"], config_data.get_multi_option(child_section, "strvalue"))

        self.assertEquals(['one', 'two', 'three'], config_data.get_multi_file_option(child_section, "multivalue", "."))
        self.assertEquals([], config_data.get_multi_file_option(child_section, "boolvalue", "."))
        self.assertEquals([], config_data.get_multi_file_option(child_section, "intvalue", "."))
        self.assertEquals(["hello"], config_data.get_multi_file_option(child_section, "strvalue", "."))

        self.assertEquals([], config_data.get_multi_file_option(child_section, "unknown1", "."))
        self.assertEquals(["missing1", "missing2"], config_data.get_multi_file_option(child_section, "unknown1", ".", missing_value=["missing1", "missing2"]))

    def test_load_from_file(self):
        json = JSONConfigurationFile()
        self.assertIsNotNone(json)

        text_file = os.path.dirname(__file__) + os.sep + "test_json.json"

        configuration = json.load_from_file(text_file, ConsoleConfiguration(), ".")
        self.assertIsNotNone(configuration)
        self.assert_configuration(configuration)

    def test_load_from_text(self):
        json = JSONConfigurationFile()
        self.assertIsNotNone(json)

        text_file = os.path.dirname(__file__) + os.sep + "test_json.json"

        text = ""
        with open(text_file, "r+") as textfile:
            lines = textfile.readlines()
            for line in lines:
                text += line
                text += "\n"

        configuration = json.load_from_text(text, ConsoleConfiguration(), ".")

        self.assertIsNotNone(configuration)
        self.assert_configuration(configuration)

    def test_load_from_text_multis_one_value(self):
        json = JSONConfigurationFile()
        self.assertIsNotNone(json)
        configuration = json.load_from_text("""
{
    "bot": {
        "brain":  "bot1"
        }
}
        """, ConsoleConfiguration(), ".")
        self.assertIsNotNone(configuration)

        self.assertEqual(1, len(configuration.client_configuration.configurations[0].configurations))

    def test_load_from_text_multis_multiple_values(self):
        json = JSONConfigurationFile()
        self.assertIsNotNone(json)
        configuration = json.load_from_text("""
        {
          "console": {
            "bots": {
              "bot1": {
                "brains": {
                  "brain1": null,
                  "brain2": null
                }
              },
              "bot2": {
                "brains": {
                  "brain3": null
                }
              }
            }
          }
        }""", ConsoleConfiguration(), ".")
        self.assertIsNotNone(configuration)

        self.assertEqual(2, len(configuration.client_configuration.configurations[0].configurations))

    def test_load_with_subs(self):
        subs = Substitutions()
        subs.add_substitute("$ALLOW_SYSTEM", True)

        config_data = JSONConfigurationFile()
        self.assertIsNotNone(config_data)
        configuration = config_data.load_from_text("""
{"brain": {
    "overrides": {
          "allow_system_aiml": true,
          "allow_learn_aiml": true,
          "allow_learnf_aiml": true
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

        self.assertEqual(True, config_data.get_option(child_section, "allow_system_aiml"))
        self.assertEqual(True, config_data.get_bool_option(child_section, "allow_system_aiml"))
        self.assertEqual(False, config_data.get_bool_option(child_section, "other_value"))
