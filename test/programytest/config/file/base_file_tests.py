import unittest

class ConfigurationBaseFileTests(unittest.TestCase):

    def assert_configuration(self, configuration):
        self.assertIsNotNone(configuration)

        self.assertIsNotNone(configuration.client_configuration.configurations[0].configurations[0])

        self.assertIsNotNone(configuration.client_configuration.configurations[0].configurations[0].overrides)

        self.assertTrue(configuration.client_configuration.configurations[0].configurations[0].overrides.allow_system_aiml)
        self.assertTrue(configuration.client_configuration.configurations[0].configurations[0].overrides.allow_learn_aiml)
        self.assertTrue(configuration.client_configuration.configurations[0].configurations[0].overrides.allow_learnf_aiml)

        self.assertIsNotNone(configuration.client_configuration.configurations[0].configurations[0].defaults)

        self.assertEqual(configuration.client_configuration.configurations[0].configurations[0].defaults.default_get, "test_unknown")
        self.assertEqual(configuration.client_configuration.configurations[0].configurations[0].defaults.default_property, "test_unknown")
        self.assertEqual(configuration.client_configuration.configurations[0].configurations[0].defaults.default_map, "test_unknown")
        self.assertEqual(configuration.client_configuration.configurations[0].configurations[0].defaults.learnf_path, "/tmp/learnf")

        self.assertIsNotNone(configuration.client_configuration.configurations[0].configurations[0].nodes)

        self.assertEqual(configuration.client_configuration.configurations[0].configurations[0].nodes.pattern_nodes, "./config/test_pattern_nodes.conf")
        self.assertEqual(configuration.client_configuration.configurations[0].configurations[0].nodes.template_nodes, "./config/test_template_nodes.conf")

        self.assertIsNotNone(configuration.client_configuration.configurations[0].configurations[0].binaries)

        self.assertTrue(configuration.client_configuration.configurations[0].configurations[0].binaries.save_binary)
        self.assertTrue(configuration.client_configuration.configurations[0].configurations[0].binaries.load_binary)
        self.assertEqual(configuration.client_configuration.configurations[0].configurations[0].binaries.binary_filename, "/tmp/y-bot.brain")
        self.assertTrue(configuration.client_configuration.configurations[0].configurations[0].binaries.load_aiml_on_binary_fail)

        self.assertIsNotNone(configuration.client_configuration.configurations[0].configurations[0].braintree)

        self.assertEqual(configuration.client_configuration.configurations[0].configurations[0].braintree.file, "/tmp/braintree.xml")
        self.assertEqual(configuration.client_configuration.configurations[0].configurations[0].braintree.content, "xml")

        self.assertIsNotNone(configuration.client_configuration.configurations[0].configurations[0].files)

        self.assertIsNotNone(configuration.client_configuration.configurations[0].configurations[0].files.aiml_files)
        self.assertEqual(configuration.client_configuration.configurations[0].configurations[0].files.aiml_files.files, ["./test-aiml"])
        self.assertIsNone(configuration.client_configuration.configurations[0].configurations[0].files.aiml_files.file)
        self.assertEqual(configuration.client_configuration.configurations[0].configurations[0].files.aiml_files.extension, ".test-aiml")
        self.assertTrue(configuration.client_configuration.configurations[0].configurations[0].files.aiml_files.directories)
        self.assertEqual(configuration.client_configuration.configurations[0].configurations[0].files.aiml_files.errors.filename, "/tmp/y-bot_errors.txt")
        self.assertEqual(configuration.client_configuration.configurations[0].configurations[0].files.aiml_files.duplicates.filename, "/tmp/y-bot_duplicates.txt")
        self.assertEqual(configuration.client_configuration.configurations[0].configurations[0].files.aiml_files.conversation.filename, "/tmp/y-bot_conversation.txt")

        self.assertIsNotNone(configuration.client_configuration.configurations[0].configurations[0].files.set_files)
        self.assertEqual(configuration.client_configuration.configurations[0].configurations[0].files.set_files.files, ["./test-sets"])
        self.assertIsNone(configuration.client_configuration.configurations[0].configurations[0].files.set_files.file)
        self.assertEqual(configuration.client_configuration.configurations[0].configurations[0].files.set_files.extension, ".test-txt")
        self.assertTrue(configuration.client_configuration.configurations[0].configurations[0].files.set_files.directories)

        self.assertIsNotNone(configuration.client_configuration.configurations[0].configurations[0].files.map_files)
        self.assertEqual(configuration.client_configuration.configurations[0].configurations[0].files.map_files.files, ["./test-maps"])
        self.assertIsNone(configuration.client_configuration.configurations[0].configurations[0].files.map_files.file)
        self.assertEqual(configuration.client_configuration.configurations[0].configurations[0].files.map_files.extension, ".test-txt")
        self.assertTrue(configuration.client_configuration.configurations[0].configurations[0].files.map_files.directories)

        self.assertEqual(configuration.client_configuration.configurations[0].configurations[0].files.denormal, "./config/test-denormal.txt")
        self.assertEqual(configuration.client_configuration.configurations[0].configurations[0].files.normal, "./config/test-normal.txt")
        self.assertEqual(configuration.client_configuration.configurations[0].configurations[0].files.gender, "./config/test-gender.txt")
        self.assertEqual(configuration.client_configuration.configurations[0].configurations[0].files.person, "./config/test-person.txt")
        self.assertEqual(configuration.client_configuration.configurations[0].configurations[0].files.person2, "./config/test-person2.txt")
        self.assertEqual(configuration.client_configuration.configurations[0].configurations[0].files.properties, "./config/test-properties.txt")
        self.assertEqual(configuration.client_configuration.configurations[0].configurations[0].files.triples, "./config/test-triples.txt")
        self.assertEqual(configuration.client_configuration.configurations[0].configurations[0].files.preprocessors, "./config/test-preprocessors.conf")
        self.assertEqual(configuration.client_configuration.configurations[0].configurations[0].files.postprocessors, "./config/test-postprocessors.conf")
        self.assertEqual(configuration.client_configuration.configurations[0].configurations[0].files.regex_templates, "./config/regex-templates.txt")

        self.assertIsNotNone(configuration.client_configuration.configurations[0].configurations[0].services)

        self.assertTrue(configuration.client_configuration.configurations[0].configurations[0].services.exists('REST'))
        rest_config =configuration.client_configuration.configurations[0].configurations[0].services.service('REST')
        self.assertEqual("programy.services.rest.GenericRESTService", rest_config.classname)

        self.assertTrue(configuration.client_configuration.configurations[0].configurations[0].services.exists('Pannous'))
        self.assertTrue(configuration.client_configuration.configurations[0].configurations[0].services.exists('Pandora'))
        self.assertTrue(configuration.client_configuration.configurations[0].configurations[0].services.exists('Wikipedia'))
        self.assertFalse(configuration.client_configuration.configurations[0].configurations[0].services.exists('Other'))

        self.assertIsNotNone(configuration.client_configuration.configurations)
        self.assertEqual(configuration.client_configuration.configurations[0].initial_question, "Hi, how can I help you test today?")
        self.assertEqual(configuration.client_configuration.configurations[0].default_response, "Sorry, I don't have a test answer for that!")
        self.assertEqual(configuration.client_configuration.configurations[0].empty_string, "TEST-YEMPTY")
        self.assertEqual(configuration.client_configuration.configurations[0].exit_response, "So long, and thanks for the test fish!")
        self.assertTrue(configuration.client_configuration.configurations[0].override_properties)
        self.assertEqual(configuration.client_configuration.configurations[0].max_question_recursion, 1000)
        self.assertEqual(configuration.client_configuration.configurations[0].max_question_timeout, 60)
        self.assertEqual(configuration.client_configuration.configurations[0].max_search_depth, 100)
        self.assertEqual(configuration.client_configuration.configurations[0].max_search_timeout, 60)

        self.assertIsNotNone(configuration.client_configuration.configurations[0].spelling)
        self.assertEqual(configuration.client_configuration.configurations[0].spelling.section_name, "spelling")
        self.assertEqual(configuration.client_configuration.configurations[0].spelling.classname, "programy.spelling.checker.TestSpellingChecker")
        self.assertEqual(configuration.client_configuration.configurations[0].spelling.corpus, "./spelling/test-corpus.txt")
        self.assertTrue(configuration.client_configuration.configurations[0].spelling.check_before)
        self.assertTrue(configuration.client_configuration.configurations[0].spelling.check_and_retry)

        self.assertIsNotNone(configuration.client_configuration)
        self.assertEqual(configuration.client_configuration.section_name, "console")
