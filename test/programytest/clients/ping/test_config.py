import unittest

from programy.config.file.yaml_file import YamlConfigurationFile
from programy.clients.ping.config import PingResponderConfig
from programy.clients.events.console.config import ConsoleConfiguration


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
                shutdown: /api/v1.0/shutdown
                register: http://127.0.0.1:5000/api/healthcheck/v1.0/register
                unregister: http://127.0.0.1:5000/api/healthcheck/v1.0/unregister
        """, ConsoleConfiguration(), ".")

        console_config = yaml.get_section("console")

        responder_config = PingResponderConfig()
        responder_config.load_config_section(yaml, console_config, ".")

        self.assertEquals(responder_config.name, "Responder")
        self.assertEquals(responder_config.host, "localhost")
        self.assertEquals(responder_config.port, 6000)
        self.assertEquals(responder_config.url, "/api/v1.0/ping")
        self.assertEquals(responder_config.shutdown, "/api/v1.0/shutdown")
        self.assertEquals(responder_config.register, "http://127.0.0.1:5000/api/healthcheck/v1.0/register")
        self.assertEquals(responder_config.unregister, "http://127.0.0.1:5000/api/healthcheck/v1.0/unregister")

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

        self.assertEquals(responder_config.name, "Client Ping Responder")
        self.assertIsNone(responder_config.host)
        self.assertIsNone(responder_config.port)
        self.assertIsNone(responder_config.url)
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

        self.assertEquals(responder_config.name, "Client Ping Responder")
        self.assertIsNone(responder_config.host)
        self.assertIsNone(responder_config.port)
        self.assertIsNone(responder_config.url)
        self.assertIsNone(responder_config.shutdown)
        self.assertIsNone(responder_config.register)
        self.assertIsNone(responder_config.unregister)
