import unittest

from programy.clients.events.console.config import ConsoleConfiguration
from programy.clients.ping.config import PingResponderConfig
from programy.config.file.yaml_file import YamlConfigurationFile


class PingResponderConfigurationTests(unittest.TestCase):

    def test_with_data(self):
        yaml = YamlConfigurationFile()
        self.assertIsNotNone(yaml)
        yaml.load_from_text("""
        console:
            responder:
                name: Responder
                host: localhost
                port: 6000
                url: /api/v1.0/ping
                ssl_cert_file: /cert/cert.file
                ssl_key_file: /cert/keys.file
                shutdown: /api/v1.0/shutdown
                register: http://127.0.0.1:5000/api/healthcheck/v1.0/register
                unregister: http://127.0.0.1:5000/api/healthcheck/v1.0/unregister
        """, ConsoleConfiguration(), ".")

        console_config = yaml.get_section("console")

        responder_config = PingResponderConfig()
        responder_config.load_config_section(yaml, console_config, ".")

        self.assertEqual(responder_config.name, "Responder")
        self.assertEqual(responder_config.host, "localhost")
        self.assertEqual(responder_config.port, 6000)
        self.assertEqual(responder_config.ssl_cert_file, "/cert/cert.file")
        self.assertEqual(responder_config.ssl_key_file, "/cert/keys.file")
        self.assertEqual(responder_config.url, "/api/v1.0/ping")
        self.assertEqual(responder_config.shutdown, "/api/v1.0/shutdown")
        self.assertEqual(responder_config.register, "http://127.0.0.1:5000/api/healthcheck/v1.0/register")
        self.assertEqual(responder_config.unregister, "http://127.0.0.1:5000/api/healthcheck/v1.0/unregister")

    def test_without_data(self):
        yaml = YamlConfigurationFile()
        self.assertIsNotNone(yaml)
        yaml.load_from_text("""
        bot:
            responder:
        """, ConsoleConfiguration(), ".")

        console_config = yaml.get_section("console")

        responder_config = PingResponderConfig()
        responder_config.load_config_section(yaml, console_config, ".")

        self.assertEqual(responder_config.name, "Client Ping Responder")
        self.assertIsNone(responder_config.host)
        self.assertIsNone(responder_config.port)
        self.assertIsNone(responder_config.url)
        self.assertIsNone(responder_config.ssl_cert_file)
        self.assertIsNone(responder_config.ssl_key_file)
        self.assertIsNone(responder_config.shutdown)
        self.assertIsNone(responder_config.register)
        self.assertIsNone(responder_config.unregister)

    def test_with_no_data(self):
        yaml = YamlConfigurationFile()
        self.assertIsNotNone(yaml)
        yaml.load_from_text("""
        bot:
        """, ConsoleConfiguration(), ".")

        console_config = yaml.get_section("console")

        responder_config = PingResponderConfig()
        responder_config.load_config_section(yaml, console_config, ".")

        self.assertEqual(responder_config.name, "Client Ping Responder")
        self.assertIsNone(responder_config.host)
        self.assertIsNone(responder_config.port)
        self.assertIsNone(responder_config.url)
        self.assertIsNone(responder_config.ssl_cert_file)
        self.assertIsNone(responder_config.ssl_key_file)
        self.assertIsNone(responder_config.shutdown)
        self.assertIsNone(responder_config.register)
        self.assertIsNone(responder_config.unregister)

    def test_defaults(self):
        responder_config = PingResponderConfig()
        data = {}
        responder_config.to_yaml(data, True)

        PingResponderConfigurationTests.assert_defaults(self, data)

    @staticmethod
    def assert_defaults(test, data):
        test.assertEqual(data['name'], "Client Ping Responder")
        test.assertIsNone(data['host'])
        test.assertIsNone(data['port'])
        test.assertIsNone(data['ssl_cert_file'])
        test.assertIsNone(data['ssl_key_file'])
        test.assertIsNone(data['url'])
        test.assertIsNone(data['shutdown'])
        test.assertIsNone(data['register'])
        test.assertIsNone(data['unregister'])
        test.assertFalse(data['debug'])
