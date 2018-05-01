import unittest

from programy.config.brain.brain import BrainConfiguration
from programy.config.file.yaml_file import YamlConfigurationFile
from programy.clients.events.console.config import ConsoleConfiguration

class BrainConfigurationTests(unittest.TestCase):

    def test_with_data(self):
        yaml = YamlConfigurationFile()
        self.assertIsNotNone(yaml)
        yaml.load_from_text("""
            brain:
                overrides:
                  allow_system_aiml: true
                  allow_learn_aiml: true
                  allow_learnf_aiml: true
            
                defaults:
                  default-get: unknown
                  default-property: unknown
                  default-map: unknown
                  learnf-path: /tmp/learnf

                nodes:
                  pattern_nodes: $BOT_ROOT/config/pattern_nodes.conf
                  template_nodes: $BOT_ROOT/config/template_nodes.conf
            
                binaries:
                  save_binary: false
                  load_binary: false
                  binary_filename: /tmp/y-bot.brain
                  load_aiml_on_binary_fail: false

                braintree:
                  file: /tmp/braintree.xml
                  content: xml
            
                files:
                    aiml:
                        files: $BOT_ROOT/aiml
                        extension: .aiml
                        directories: true
                        errors: /tmp/y-bot_errors.txt
                        duplicates: /tmp/y-bot_duplicates.txt
                        conversation: /tmp/y-bot_conversation.txt
                    sets:
                        files: $BOT_ROOT/sets
                        extension: .txt
                        directories: false
                    maps:
                        files: $BOT_ROOT/maps
                        extension: .txt
                        directories: false
                    denormal: $BOT_ROOT/config/denormal.txt
                    normal: $BOT_ROOT/config/normal.txt
                    gender: $BOT_ROOT/config/gender.txt
                    person: $BOT_ROOT/config/person.txt
                    person2: $BOT_ROOT/config/person2.txt
                    properties: $BOT_ROOT/config/properties.txt
                    triples: $BOT_ROOT/config/triples.txt
                    preprocessors: $BOT_ROOT/config/preprocessors.conf
                    postprocessors: $BOT_ROOT/config/postprocessors.conf
                    regex_templates: $BOT_ROOT/config/regex-templates.txt
            
                security:
                    authentication:
                        classname: programy.security.authenticate.passthrough.PassThroughAuthenticationService
                        denied_srai: AUTHENTICATION_FAILED
                    authorisation:
                        classname: programy.security.authorise.passthrough.PassThroughAuthorisationService
                        denied_srai: AUTHORISATION_FAILED

                oob:
                  default:
                    classname: programy.oob.default.DefaultOutOfBandProcessor
                  dial:
                    classname: programy.oob.dial.DialOutOfBandProcessor
                  email:
                    classname: programy.oob.email.EmailOutOfBandProcessor

                dynamic:
                    variables:
                        gettime: programy.dynamic.variables.datetime.GetTime
                    sets:
                        number: programy.dynamic.sets.numeric.IsNumeric
                        roman:   programy.dynamic.sets.roman.IsRomanNumeral
                    maps:
                        romantodec: programy.dynamic.maps.roman.MapRomanToDecimal
                        dectoroman: programy.dynamic.maps.roman.MapDecimalToRoman

                services:
                    REST:
                        classname: programy.services.rest.GenericRESTService
                        method: GET
                        host: 0.0.0.0
                    Pannous:
                        classname: programy.services.pannous.PannousService
                        url: http://weannie.pannous.com/api
                    Pandora:
                        classname: programy.services.pandora.PandoraService
                        url: http://www.pandorabots.com/pandora/talk-xml
                    Wikipedia:
                        classname: programy.services.wikipediaservice.WikipediaService        
        """, ConsoleConfiguration(), ".")

        brain_config = BrainConfiguration()
        brain_config.load_configuration(yaml, ".")

        self.assertIsNotNone(brain_config.overrides)
        self.assertTrue(brain_config.overrides.allow_system_aiml)
        self.assertTrue(brain_config.overrides.allow_learn_aiml)
        self.assertTrue(brain_config.overrides.allow_learnf_aiml)

        self.assertIsNotNone(brain_config.defaults)
        self.assertEqual("unknown", brain_config.defaults.default_get)
        self.assertEqual("unknown", brain_config.defaults.default_property)
        self.assertEqual("unknown", brain_config.defaults.default_map)
        self.assertEqual("/tmp/learnf", brain_config.defaults.learnf_path)

        self.assertIsNotNone(brain_config.nodes)
        self.assertEquals("./config/pattern_nodes.conf", brain_config.nodes.pattern_nodes)
        self.assertEquals("./config/template_nodes.conf", brain_config.nodes.template_nodes)

        self.assertIsNotNone(brain_config.binaries)
        self.assertFalse(brain_config.binaries.save_binary)
        self.assertFalse(brain_config.binaries.load_binary)
        self.assertEquals("/tmp/y-bot.brain", brain_config.binaries.binary_filename)
        self.assertFalse(brain_config.binaries.load_aiml_on_binary_fail)

        self.assertIsNotNone(brain_config.braintree)
        self.assertEquals("/tmp/braintree.xml", brain_config.braintree.file)
        self.assertEquals("xml", brain_config.braintree.content)

        self.assertIsNotNone(brain_config.files)
        self.assertIsNotNone(brain_config.files.aiml_files)
        self.assertEqual(["./aiml"], brain_config.files.aiml_files.files)
        self.assertEqual(".aiml", brain_config.files.aiml_files.extension)
        self.assertTrue(brain_config.files.aiml_files.directories)
        self.assertEqual("/tmp/y-bot_errors.txt", brain_config.files.aiml_files.errors.filename)
        self.assertEqual("/tmp/y-bot_duplicates.txt", brain_config.files.aiml_files.duplicates.filename)
        self.assertEqual("/tmp/y-bot_conversation.txt", brain_config.files.aiml_files.conversation.filename)

        self.assertIsNotNone(brain_config.files.set_files)
        self.assertEqual(["./sets"], brain_config.files.set_files.files)
        self.assertEqual(".txt", brain_config.files.set_files.extension)
        self.assertFalse(brain_config.files.set_files.directories)

        self.assertIsNotNone(brain_config.files.map_files)
        self.assertEqual(["./maps"], brain_config.files.map_files.files)
        self.assertEqual(".txt", brain_config.files.map_files.extension)
        self.assertFalse(brain_config.files.map_files.directories)

        self.assertEqual(brain_config.files.denormal, "./config/denormal.txt")
        self.assertEqual(brain_config.files.normal, "./config/normal.txt")
        self.assertEqual(brain_config.files.gender, "./config/gender.txt")
        self.assertEqual(brain_config.files.person, "./config/person.txt")
        self.assertEqual(brain_config.files.person2, "./config/person2.txt")
        self.assertEqual(brain_config.files.properties, "./config/properties.txt")
        self.assertEqual(brain_config.files.triples, "./config/triples.txt")
        self.assertEqual(brain_config.files.preprocessors, "./config/preprocessors.conf")
        self.assertEqual(brain_config.files.postprocessors, "./config/postprocessors.conf")
        self.assertEqual(brain_config.files.regex_templates, "./config/regex-templates.txt")

        self.assertIsNotNone(brain_config.security)
        self.assertIsNotNone(brain_config.security.authorisation)
        self.assertIsNotNone(brain_config.security.authentication)

        self.assertIsNotNone(brain_config.services)
        self.assertTrue(brain_config.services.exists("REST"))
        self.assertTrue(brain_config.services.exists("Pannous"))
        self.assertTrue(brain_config.services.exists("Pandora"))
        self.assertTrue(brain_config.services.exists("Wikipedia"))
        self.assertFalse(brain_config.services.exists("Other"))

        self.assertIsNotNone(brain_config.oob)
        self.assertIsNotNone(brain_config.oob.oobs())
        self.assertIsNotNone(brain_config.oob.default())
        self.assertIsNotNone(brain_config.oob.oob("dial"))
        self.assertIsNotNone(brain_config.oob.oob("email"))

        self.assertIsNotNone(brain_config.dynamics)
        self.assertIsNotNone(brain_config.dynamics.dynamic_sets)
        self.assertTrue("NUMBER" in brain_config.dynamics.dynamic_sets)
        self.assertTrue("ROMAN" in brain_config.dynamics.dynamic_sets)
        self.assertIsNotNone(brain_config.dynamics.dynamic_maps)
        self.assertTrue("ROMANTODEC" in brain_config.dynamics.dynamic_maps)
        self.assertTrue("DECTOROMAN" in brain_config.dynamics.dynamic_maps)
        self.assertIsNotNone(brain_config.dynamics.dynamic_vars)
        self.assertTrue("GETTIME" in brain_config.dynamics.dynamic_vars)
