import unittest

class ConfigurationBaseFileTests(unittest.TestCase):

    def assert_configuration(self, configuration):
        self.assertIsNotNone(configuration)

        self.assertIsNotNone(configuration.brain_configuration)

        self.assertIsNotNone(configuration.brain_configuration.overrides)

        self.assertTrue(configuration.brain_configuration.overrides.allow_system_aiml)
        self.assertTrue(configuration.brain_configuration.overrides.allow_learn_aiml)
        self.assertTrue(configuration.brain_configuration.overrides.allow_learnf_aiml)

        self.assertIsNotNone(configuration.brain_configuration.defaults)

        self.assertEqual(configuration.brain_configuration.defaults.default_get, "test_unknown")
        self.assertEqual(configuration.brain_configuration.defaults.default_property, "test_unknown")
        self.assertEqual(configuration.brain_configuration.defaults.default_map, "test_unknown")
        self.assertEqual(configuration.brain_configuration.defaults.learn_filename, "test-learnf.aiml")

        self.assertIsNotNone(configuration.brain_configuration.nodes)

        self.assertEqual(configuration.brain_configuration.nodes.pattern_nodes, "./config/test_pattern_nodes.conf")
        self.assertEqual(configuration.brain_configuration.nodes.template_nodes, "./config/test_template_nodes.conf")

        self.assertIsNotNone(configuration.brain_configuration.binaries)

        self.assertTrue(configuration.brain_configuration.binaries.save_binary)
        self.assertTrue(configuration.brain_configuration.binaries.load_binary)
        self.assertEqual(configuration.brain_configuration.binaries.binary_filename, "./output/test-y-bot.brain")
        self.assertTrue(configuration.brain_configuration.binaries.load_aiml_on_binary_fail)
        self.assertEqual(configuration.brain_configuration.binaries.dump_to_file, "./output/test-braintree.txt")

        self.assertIsNotNone(configuration.brain_configuration.files)

        self.assertIsNotNone(configuration.brain_configuration.files.aiml_files)
        self.assertEqual(configuration.brain_configuration.files.aiml_files.files, "./test-aiml")
        self.assertIsNone(configuration.brain_configuration.files.aiml_files.file)
        self.assertEqual(configuration.brain_configuration.files.aiml_files.extension, ".test-aiml")
        self.assertTrue(configuration.brain_configuration.files.aiml_files.directories)
        self.assertEqual(configuration.brain_configuration.files.aiml_files.errors, "./output/test-y-bot_errors.txt")
        self.assertEqual(configuration.brain_configuration.files.aiml_files.duplicates, "./output/test-y-bot_duplicates.txt")

        self.assertIsNotNone(configuration.brain_configuration.files.set_files)
        self.assertEqual(configuration.brain_configuration.files.set_files.files, "./test-sets")
        self.assertIsNone(configuration.brain_configuration.files.set_files.file)
        self.assertEqual(configuration.brain_configuration.files.set_files.extension, ".test-txt")
        self.assertTrue(configuration.brain_configuration.files.set_files.directories)

        self.assertIsNotNone(configuration.brain_configuration.files.map_files)
        self.assertEqual(configuration.brain_configuration.files.map_files.files, "./test-maps")
        self.assertIsNone(configuration.brain_configuration.files.map_files.file)
        self.assertEqual(configuration.brain_configuration.files.map_files.extension, ".test-txt")
        self.assertTrue(configuration.brain_configuration.files.map_files.directories)

        self.assertEqual(configuration.brain_configuration.files.denormal, "./config/test-denormal.txt")
        self.assertEqual(configuration.brain_configuration.files.normal, "./config/test-normal.txt")
        self.assertEqual(configuration.brain_configuration.files.gender, "./config/test-gender.txt")
        self.assertEqual(configuration.brain_configuration.files.person, "./config/test-person.txt")
        self.assertEqual(configuration.brain_configuration.files.person2, "./config/test-person2.txt")
        self.assertEqual(configuration.brain_configuration.files.properties, "./config/test-properties.txt")
        self.assertEqual(configuration.brain_configuration.files.triples, "./config/test-triples.txt")
        self.assertEqual(configuration.brain_configuration.files.preprocessors, "./config/test-preprocessors.conf")
        self.assertEqual(configuration.brain_configuration.files.postprocessors, "./config/test-postprocessors.conf")

        self.assertIsNotNone(configuration.brain_configuration.services)

        self.assertTrue(configuration.brain_configuration.services.exists('REST'))
        rest_config =configuration.brain_configuration.services.service('REST')
        self.assertEqual("programy.utils.services.rest.GenericRESTService", rest_config.classname)

        self.assertTrue(configuration.brain_configuration.services.exists('Pannous'))
        self.assertTrue(configuration.brain_configuration.services.exists('Pandora'))
        self.assertTrue(configuration.brain_configuration.services.exists('Wikipedia'))
        self.assertFalse(configuration.brain_configuration.services.exists('Other'))

        self.assertIsNotNone(configuration.bot_configuration)
        self.assertEqual(configuration.bot_configuration.license_keys, "./config/test-license.keys")
        self.assertEqual(configuration.bot_configuration.prompt, "TEST>>>")
        self.assertEqual(configuration.bot_configuration.initial_question, "Hi, how can I help you test today?")
        self.assertEqual(configuration.bot_configuration.default_response, "Sorry, I don't have a test answer for that!")
        self.assertEqual(configuration.bot_configuration.empty_string, "TEST-YEMPTY")
        self.assertEqual(configuration.bot_configuration.exit_response, "So long, and thanks for the test fish!")
        self.assertTrue(configuration.bot_configuration.override_properties)
        self.assertEqual(configuration.bot_configuration.max_question_recursion, 1000)
        self.assertEqual(configuration.bot_configuration.max_question_timeout, 60)
        self.assertEqual(configuration.bot_configuration.max_search_depth, 100)
        self.assertEqual(configuration.bot_configuration.max_search_timeout, 60)

        self.assertIsNotNone(configuration.bot_configuration.spelling)
        self.assertEqual(configuration.bot_configuration.spelling.section_name, "spelling")
        self.assertEqual(configuration.bot_configuration.spelling.classname, "programy.utils.spelling.checker.TestSpellingChecker")
        self.assertEqual(configuration.bot_configuration.spelling.corpus, "./spelling/test-corpus.txt")
        self.assertTrue(configuration.bot_configuration.spelling.check_before)
        self.assertTrue(configuration.bot_configuration.spelling.check_and_retry)

        self.assertIsNotNone(configuration.client_configuration)
        self.assertEqual(configuration.client_configuration.section_name, "console")
