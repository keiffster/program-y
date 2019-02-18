import unittest
import os

from programy.config.file.yaml_file import YamlConfigurationFile
from programy.utils.email.config import EmailConfiguration
from programy.clients.events.console.config import ConsoleConfiguration


class EmailConfigurationTests(unittest.TestCase):

    def test_with_data(self):
        yaml = YamlConfigurationFile()
        self.assertIsNotNone(yaml)
        yaml.load_from_text("""
        console:
            email:
                host: 127.0.0.1
                port: 80
                username: emailuser
                password: emailpassword
                from_addr: emailfromuser
        """, ConsoleConfiguration(), ".")

        client_config = yaml.get_section("console")

        email_config = EmailConfiguration()
        email_config.load_config_section(yaml, client_config, ".")

        self.assertEqual("127.0.0.1", email_config.host)
        self.assertEqual(80, email_config.port)
        self.assertEqual("emailuser", email_config.username)
        self.assertEqual("emailpassword", email_config.password)
        self.assertEqual("emailfromuser", email_config.from_addr)

    def test_without_data(self):
        yaml = YamlConfigurationFile()
        self.assertIsNotNone(yaml)
        yaml.load_from_text("""
        console:
            email:
        """, ConsoleConfiguration(), ".")

        client_config = yaml.get_section("email")

        email_config = EmailConfiguration()
        email_config.load_config_section(yaml, client_config, ".")

        self.assertIsNone(email_config.host)
        self.assertIsNone(email_config.port)
        self.assertIsNone(email_config.username)
        self.assertIsNone(email_config.password)
        self.assertIsNone(email_config.from_addr)

    def test_with_no_data(self):
        yaml = YamlConfigurationFile()
        self.assertIsNotNone(yaml)
        yaml.load_from_text("""
        console:
        """, ConsoleConfiguration(), ".")

        client_config = yaml.get_section("email")

        email_config = EmailConfiguration()
        email_config.load_config_section(yaml, client_config, ".")

        self.assertIsNone(email_config.host)
        self.assertIsNone(email_config.port)
        self.assertIsNone(email_config.username)
        self.assertIsNone(email_config.password)
        self.assertIsNone(email_config.from_addr)

