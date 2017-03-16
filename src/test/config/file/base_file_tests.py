import unittest

class ConfigurationBaseFileTests(unittest.TestCase):

    def assert_config_data(self, config_data):
        self.assertIsNotNone(config_data)

        self.assertIsNotNone(config_data.bot_configuration)
        self.assertEqual(config_data.bot_configuration.prompt, ">>>")
        self.assertEqual(config_data.bot_configuration.default_response, "Sorry, I don't have an answer for that!")
        self.assertEqual(config_data.bot_configuration.exit_response, "So long, and thanks for the fish!")

        self.assertIsNotNone(config_data.brain_configuration)
        self.assertIsNotNone(config_data.brain_configuration.aiml_files)
        self.assertEqual(config_data.brain_configuration.aiml_files.files, "/aiml")
        self.assertEqual(config_data.brain_configuration.aiml_files.extension, ".aiml")
        self.assertEqual(config_data.brain_configuration.aiml_files.directories, True)

        self.assertIsNotNone(config_data.brain_configuration.set_files)
        self.assertEqual(config_data.brain_configuration.set_files.files, "/sets")
        self.assertEqual(config_data.brain_configuration.set_files.extension, ".txt")
        self.assertEqual(config_data.brain_configuration.set_files.directories, False)

        self.assertIsNotNone(config_data.brain_configuration.map_files)
        self.assertEqual(config_data.brain_configuration.map_files.files, "/maps")
        self.assertEqual(config_data.brain_configuration.map_files.extension, ".txt")
        self.assertEqual(config_data.brain_configuration.map_files.directories, True)

        self.assertEqual(config_data.brain_configuration.denormal, "denormal.txt")
        self.assertEqual(config_data.brain_configuration.normal, "normal.txt")
        self.assertEqual(config_data.brain_configuration.gender, "gender.txt")
        self.assertEqual(config_data.brain_configuration.person2, "person2.txt")
        self.assertEqual(config_data.brain_configuration.predicates, "predicates.txt")
        self.assertEqual(config_data.brain_configuration.pronouns, "pronouns.txt")
        self.assertEqual(config_data.brain_configuration.properties, "properties.txt")
        self.assertEqual(config_data.brain_configuration.triples, "triples.txt")
        self.assertEqual(config_data.brain_configuration.preprocessors, "preprocessors.txt")

        self.assertIsNotNone(config_data.brain_configuration.services)
        self.assertEqual(4, len(config_data.brain_configuration.services))

        self.assertIn(config_data.brain_configuration.services[0].name, ["REST", "PANNOUS", "PANDORA", "WIKIPEDIA"])
        self.assertIn(config_data.brain_configuration.services[0].path, ["programy.utils.services.rest.GenericRESTService",
                                                                         "programy.utils.services.pannous.PannousService",
                                                                         "programy.utils.services.pandora.PandoraService",
                                                                         "programy.utils.services.google.GoogleService",
                                                                         "programy.utils.services.wikipedia.WikipediaService"])

        self.assertIn(config_data.brain_configuration.services[1].name, ["REST", "PANNOUS", "PANDORA", "WIKIPEDIA"])
        self.assertIn(config_data.brain_configuration.services[1].path, ["programy.utils.services.rest.GenericRESTService",
                                                                         "programy.utils.services.pannous.PannousService",
                                                                         "programy.utils.services.pandora.PandoraService",
                                                                         "programy.utils.services.google.GoogleService",
                                                                         "programy.utils.services.wikipedia.WikipediaService"])

        self.assertIn(config_data.brain_configuration.services[2].name, ["REST", "PANNOUS", "PANDORA", "WIKIPEDIA"])
        self.assertIn(config_data.brain_configuration.services[2].path, ["programy.utils.services.rest.GenericRESTService",
                                                                         "programy.utils.services.pannous.PannousService",
                                                                         "programy.utils.services.pandora.PandoraService",
                                                                         "programy.utils.services.google.GoogleService",
                                                                         "programy.utils.services.wikipedia.WikipediaService"])

        self.assertIn(config_data.brain_configuration.services[3].name, ["REST", "PANNOUS", "PANDORA", "WIKIPEDIA"])
        self.assertIn(config_data.brain_configuration.services[3].path, ["programy.utils.services.rest.GenericRESTService",
                                                                         "programy.utils.services.pannous.PannousService",
                                                                         "programy.utils.services.pandora.PandoraService",
                                                                         "programy.utils.services.google.GoogleService",
                                                                         "programy.utils.services.wikipedia.WikipediaService"])
