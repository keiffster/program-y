import unittest

class ConfigurationBaseFileTests(unittest.TestCase):

    def assert_configuration(self, configuration):

        self.assertIsNotNone(configuration)

        client_configuration = configuration.client_configuration
        self.assertIsNotNone(client_configuration)
        self.assertEqual(client_configuration.section_name, "console")
        self.assertEqual(client_configuration.prompt, ">>>")

        self.assertEqual(1, len(client_configuration.configurations))
        bot_configuration = client_configuration.configurations[0]
        self.assertIsNotNone(bot_configuration)

        self.assertEqual(bot_configuration.initial_question, "Hi, how can I help you today?")
        self.assertEqual(bot_configuration.initial_question_srai, "YINITIALQUESTION")
        self.assertEqual(bot_configuration.default_response, "Sorry, I don't have an answer for that!")
        self.assertEqual(bot_configuration.default_response_srai, "YEMPTY")
        self.assertEqual(bot_configuration.empty_string, "YEMPTY")
        self.assertEqual(bot_configuration.exit_response, "So long, and thanks for the fish!")
        self.assertEqual(bot_configuration.exit_response_srai, "YEXITRESPONSE")

        self.assertEqual(bot_configuration.override_properties, True)

        self.assertEqual(bot_configuration.max_question_recursion, 1000)
        self.assertEqual(bot_configuration.max_question_timeout, 60)
        self.assertEqual(bot_configuration.max_search_depth, 100)
        self.assertEqual(bot_configuration.max_search_timeout, 60)

        self.assertIsNotNone(bot_configuration.spelling)
        self.assertEqual(bot_configuration.spelling.section_name, "spelling")
        self.assertEqual(bot_configuration.spelling.classname, "programy.spelling.norvig.NorvigSpellingChecker")
        self.assertTrue(bot_configuration.spelling.check_before)
        self.assertTrue(bot_configuration.spelling.check_and_retry)

        self.assertIsNotNone(bot_configuration.conversations)
        self.assertIsNotNone(bot_configuration.conversations.max_histories, 100)
        self.assertIsNotNone(bot_configuration.conversations.restore_last_topic, False)
        self.assertIsNotNone(bot_configuration.conversations.initial_topic, "TOPIC1")
        self.assertIsNotNone(bot_configuration.conversations.empty_on_start, False)

        self.assertEqual(1, len(bot_configuration.configurations))
        brain_configuration = bot_configuration.configurations[0]
        self.assertIsNotNone(brain_configuration)

        self.assertIsNotNone(brain_configuration.overrides)
        self.assertTrue(brain_configuration.overrides.allow_system_aiml)
        self.assertTrue(brain_configuration.overrides.allow_learn_aiml)
        self.assertTrue(brain_configuration.overrides.allow_learnf_aiml)

        self.assertIsNotNone(brain_configuration.defaults)
        self.assertEqual(brain_configuration.defaults.default_get, "unknown")
        self.assertEqual(brain_configuration.defaults.default_property, "unknown")
        self.assertEqual(brain_configuration.defaults.default_map, "unknown")

        self.assertIsNotNone(brain_configuration.binaries)
        self.assertTrue(brain_configuration.binaries.save_binary)
        self.assertTrue(brain_configuration.binaries.load_binary)
        self.assertTrue(brain_configuration.binaries.load_aiml_on_binary_fail)

        self.assertIsNotNone(brain_configuration.braintree)
        self.assertTrue(brain_configuration.braintree.create)

        self.assertIsNotNone(brain_configuration.services)
        self.assertTrue(brain_configuration.services.exists('REST'))
        rest_config=brain_configuration.services.service('REST')
        self.assertEqual("programy.services.rest.GenericRESTService", rest_config.classname)
        self.assertEqual(rest_config.method, "GET")
        self.assertEqual(rest_config.host, "0.0.0.0")
        self.assertEqual(rest_config.port, 8080)
        pannous_config =brain_configuration.services.service('Pannous')
        self.assertEqual("programy.services.pannous.PannousService", pannous_config.classname)
        self.assertEqual(pannous_config.url, "http://weannie.pannous.com/api")

        self.assertIsNotNone(brain_configuration.security)
        self.assertIsNotNone(brain_configuration.security.authorisation)
        self.assertIsNotNone(brain_configuration.security.authentication)

        self.assertIsNotNone(brain_configuration.oob)
        self.assertTrue(brain_configuration.oob.exists("default"))

        self.assertIsNotNone(brain_configuration.dynamics)
        self.assertIsNotNone(brain_configuration.dynamics.dynamic_sets)

        self.assertIsNotNone(brain_configuration.dynamics.dynamic_maps)
        self.assertIsNotNone(brain_configuration.dynamics.dynamic_vars)
