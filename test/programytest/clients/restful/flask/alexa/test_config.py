import unittest

from programy.config.file.yaml_file import YamlConfigurationFile
from programy.clients.restful.flask.alexa.config import AlexaConfiguration
from programy.clients.events.console.config import ConsoleConfiguration


class AlexaConfigurationTests(unittest.TestCase):

    def test_init(self):
        yaml = YamlConfigurationFile()
        self.assertIsNotNone(yaml)
        yaml.load_from_text("""
        alexa:
          host: 127.0.0.1
          port: 5000
          debug: false
          launch_text: Hello and welcome
          launch_srai: ALEXA_LAUNCH
          cancel_text: OK, what else can I do?
          cancel_srai: ALEXA_CANCEL
          stop_text: Good bye matey
          stop_srai: ALEXA_STOP
          help_text: Ask me anything, I know loads
          help_srai: ALEXA_HELP
          error_text: Oopsie there has been an error
          error_srai: ALEXA_ERROR
          leave_intents: AMAZON.CancelIntent, AMAZON.StopIntent
          intent_map_file: intents.map
        """, ConsoleConfiguration(), ".")

        alexa_config = AlexaConfiguration()
        alexa_config.load_configuration(yaml, ".")

        self.assertEqual("127.0.0.1", alexa_config.host)
        self.assertEqual(5000, alexa_config.port)
        self.assertEqual(False, alexa_config.debug)

        self.assertEqual(alexa_config.launch_text, "Hello and welcome")
        self.assertEqual(alexa_config.launch_srai, "ALEXA_LAUNCH")

        self.assertEqual(alexa_config.cancel_text, "OK, what else can I do?")
        self.assertEqual(alexa_config.cancel_srai, "ALEXA_CANCEL")

        self.assertEqual(alexa_config.stop_text, "Good bye matey")
        self.assertEqual(alexa_config.stop_srai, "ALEXA_STOP")

        self.assertEqual(alexa_config.help_text, "Ask me anything, I know loads")
        self.assertEqual(alexa_config.help_srai, "ALEXA_HELP")

        self.assertEqual(alexa_config.error_text, "Oopsie there has been an error")
        self.assertEqual(alexa_config.error_srai, "ALEXA_ERROR")

        self.assertTrue("AMAZON.CancelIntent" in alexa_config.leave_intents)
        self.assertTrue("AMAZON.StopIntent" in alexa_config.leave_intents)
        self.assertEqual(alexa_config.intent_map_file, "intents.map")

    def test_init_no_values(self):
        yaml = YamlConfigurationFile()
        self.assertIsNotNone(yaml)
        yaml.load_from_text("""
        alexa:
        """, ConsoleConfiguration(), ".")

        alexa_config = AlexaConfiguration()
        alexa_config.load_configuration(yaml, ".")

        self.assertEqual(alexa_config.host, "0.0.0.0")
        self.assertEqual(alexa_config.port, 80)
        self.assertEqual(alexa_config.debug, False)

        self.assertEqual(alexa_config.launch_text, "Hello and welcome")
        self.assertEqual(alexa_config.launch_srai, None)

        self.assertEqual(alexa_config.cancel_text, "OK, what else can I do?")
        self.assertEqual(alexa_config.cancel_srai, None)

        self.assertEqual(alexa_config.stop_text, "Good bye matey")
        self.assertEqual(alexa_config.stop_srai, None)

        self.assertEqual(alexa_config.error_text, "Oopsie there has been an error")
        self.assertEqual(alexa_config.error_srai, None)

        self.assertTrue("AMAZON.CancelIntent" in alexa_config.leave_intents)
        self.assertTrue("AMAZON.StopIntent" in alexa_config.leave_intents)
        self.assertEqual(alexa_config.intent_map_file, None)

    def test_to_yaml_with_defaults(self):
        config = AlexaConfiguration()

        data = {}
        config.to_yaml(data, True)

        self.assertEqual(data['host'], "0.0.0.0")
        self.assertEqual(data['port'], 80)
        self.assertEqual(data['debug'], False)

        self.assertEqual(data['launch_text'], "Hello and welcome")
        self.assertEqual(data['launch_srai'], None)

        self.assertEqual(data['cancel_text'], "OK, what else can I do?")
        self.assertEqual(data['cancel_srai'], None)

        self.assertEqual(data['stop_text'], "Good bye matey")
        self.assertEqual(data['stop_srai'], None)

        self.assertEqual(data['error_text'], "Oopsie there has been an error")
        self.assertEqual(data['error_srai'], None)

        self.assertTrue("AMAZON.CancelIntent" in data['leave_intents'])
        self.assertTrue("AMAZON.StopIntent" in data['leave_intents'])

        self.assertEqual(data['intent_map_file'], None)
