import unittest

from programy.clients.config import ClientConfigurationData
from programy.clients.events.console.config import ConsoleConfiguration
from programy.config.file.yaml_file import YamlConfigurationFile


class ClientConfigurationDataTests(unittest.TestCase):

    def test_with_data_single_bot(self):
        yaml = YamlConfigurationFile()
        self.assertIsNotNone(yaml)
        yaml.load_from_text("""
        console:
          bot:  bot
          prompt: ">>>"
          bot_selector: programy.clients.botfactory.DefaultBotSelector
          renderer: programy.clients.render.text.TextRenderer
          scheduler:
            name: Scheduler1
            debug_level: 0
            add_listeners: True
            remove_all_jobs: True
        """, ConsoleConfiguration(), ".")

        client_config = ClientConfigurationData("console")
        client_config.load_configuration(yaml, ".")

        self.assertEqual(1, len(client_config.configurations))
        self.assertEqual("programy.clients.botfactory.DefaultBotSelector", client_config.bot_selector)

        self.assertIsNotNone(client_config.scheduler)
        self.assertEqual("Scheduler1", client_config.scheduler.name)
        self.assertEqual(0, client_config.scheduler.debug_level)
        self.assertTrue(client_config.scheduler.add_listeners)
        self.assertTrue(client_config.scheduler.remove_all_jobs)

        self.assertEqual("programy.clients.render.text.TextRenderer", client_config.renderer)

    def test_with_data_multiple_bots(self):
        yaml = YamlConfigurationFile()
        self.assertIsNotNone(yaml)
        yaml.load_from_text("""
        console:
          bot:  | 
                bot
                bot2
          prompt: ">>>"
          bot_selector: programy.clients.botfactory.DefaultBotSelector
          renderer: programy.clients.render.text.TextRenderer
          scheduler:
            name: Scheduler1
            debug_level: 0
            add_listeners: True
            remove_all_jobs: True
        """, ConsoleConfiguration(), ".")

        client_config = ClientConfigurationData("console")
        client_config.load_configuration(yaml, ".")

        self.assertEqual(2, len(client_config.configurations))
        self.assertEqual("programy.clients.botfactory.DefaultBotSelector", client_config.bot_selector)

        self.assertIsNotNone(client_config.scheduler)
        self.assertEqual("Scheduler1", client_config.scheduler.name)
        self.assertEqual(0, client_config.scheduler.debug_level)
        self.assertTrue(client_config.scheduler.add_listeners)
        self.assertTrue(client_config.scheduler.remove_all_jobs)

        self.assertEqual("programy.clients.render.text.TextRenderer", client_config.renderer)

    def test_without_data(self):
        yaml = YamlConfigurationFile()
        self.assertIsNotNone(yaml)
        yaml.load_from_text("""
        console:
        """, ConsoleConfiguration(), ".")

        client_config = ClientConfigurationData("console")
        client_config.load_configuration(yaml, ".")

        self.assertIsNotNone(client_config.bot_selector)

        self.assertIsNotNone(client_config.scheduler)
        self.assertEqual(None, client_config.scheduler.name)
        self.assertEqual(0, client_config.scheduler.debug_level)
        self.assertFalse(client_config.scheduler.add_listeners)
        self.assertFalse(client_config.scheduler.remove_all_jobs)

        self.assertIsNotNone(client_config.renderer)

    def test_with_no_data(self):
        yaml = YamlConfigurationFile()
        self.assertIsNotNone(yaml)
        yaml.load_from_text("""
        other:
        """, ConsoleConfiguration(), ".")

        client_config = ClientConfigurationData("console")
        client_config.load_configuration(yaml, ".")

        self.assertIsNotNone(client_config.bot_selector)

        self.assertIsNotNone(client_config.scheduler)
        self.assertEqual(None, client_config.scheduler.name)
        self.assertEqual(0, client_config.scheduler.debug_level)
        self.assertFalse(client_config.scheduler.add_listeners)
        self.assertFalse(client_config.scheduler.remove_all_jobs)

        self.assertIsNotNone(client_config.renderer)
