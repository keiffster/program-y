import unittest

from programy.clients.events.console.config import ConsoleConfiguration
from programy.clients.restful.flask.google.config import GoogleConfiguration
from programy.config.file.yaml_file import YamlConfigurationFile


class GoogleConfigurationTests(unittest.TestCase):

    def test_init(self):
        yaml = YamlConfigurationFile()
        self.assertIsNotNone(yaml)
        yaml.load_from_text("""
        google:
          host: 127.0.0.1
          port: 5000
          debug: false
          launch_text: Hello and welcome
          launch_srai: GOOGLE_LAUNCH
          quit_text: Good bye matey
          quit_srai: GOOGLE_STOP
          help_text: Ask me anything, I know loads
          help_srai: GOOGLE_HELP
          error_text: Oopsie there has been an error
          error_srai: GOOGLE_ERROR
        """, ConsoleConfiguration(), ".")

        google_config = GoogleConfiguration()
        google_config.load_configuration(yaml, ".")

        self.assertEqual("127.0.0.1", google_config.host)
        self.assertEqual(5000, google_config.port)
        self.assertEqual(False, google_config.debug)

        self.assertEqual(google_config.launch_text, "Hello and welcome")
        self.assertEqual(google_config.launch_srai, "GOOGLE_LAUNCH")

        self.assertEqual(google_config.quit_text, "Good bye matey")
        self.assertEqual(google_config.quit_srai, "GOOGLE_STOP")

        self.assertEqual(google_config.help_text, "Ask me anything, I know loads")
        self.assertEqual(google_config.help_srai, "GOOGLE_HELP")

        self.assertEqual(google_config.error_text, "Oopsie there has been an error")
        self.assertEqual(google_config.error_srai, "GOOGLE_ERROR")

    def test_init_no_values(self):
        yaml = YamlConfigurationFile()
        self.assertIsNotNone(yaml)
        yaml.load_from_text("""
        google:
        """, ConsoleConfiguration(), ".")

        google_config = GoogleConfiguration()
        google_config.load_configuration(yaml, ".")

        self.assertEqual(google_config.host, "0.0.0.0")
        self.assertEqual(google_config.port, 80)
        self.assertEqual(google_config.debug, False)

        self.assertEqual(google_config.launch_text, "Hello and welcome")
        self.assertEqual(google_config.launch_srai, None)

        self.assertEqual(google_config.quit_text, "Good bye matey")
        self.assertEqual(google_config.quit_srai, None)

        self.assertEqual(google_config.error_text, "Oopsie there has been an error")
        self.assertEqual(google_config.error_srai, None)

    def test_to_yaml_with_defaults(self):
        config = GoogleConfiguration()

        data = {}
        config.to_yaml(data, True)

        self.assertEqual(data["launch_text"], GoogleConfiguration.DEFAULT_LAUNCH_TEXT)
        self.assertIsNone(data["launch_srai"])

        self.assertEqual(data["quit_text"], GoogleConfiguration.DEFAULT_QUIT_TEXT)
        self.assertIsNone(data["quit_srai"])

        self.assertEqual(data["help_text"], GoogleConfiguration.DEFAULT_HELP_TEXT)
        self.assertIsNone(data["help_srai"])

        self.assertEqual(data["error_text"], GoogleConfiguration.DEFAULT_ERROR_TEXT)
        self.assertIsNone(data["error_srai"])

    def test_to_yaml_with_no_defaults(self):
        config = GoogleConfiguration()

        data = {}
        config.to_yaml(data, False)

        self.assertEqual(data["launch_text"], GoogleConfiguration.DEFAULT_LAUNCH_TEXT)
        self.assertIsNone(data["launch_srai"])

        self.assertEqual(data["quit_text"], GoogleConfiguration.DEFAULT_QUIT_TEXT)
        self.assertIsNone(data["quit_srai"])

        self.assertEqual(data["help_text"], GoogleConfiguration.DEFAULT_HELP_TEXT)
        self.assertIsNone(data["help_srai"])

        self.assertEqual(data["error_text"], GoogleConfiguration.DEFAULT_ERROR_TEXT)
        self.assertIsNone(data["error_srai"])
