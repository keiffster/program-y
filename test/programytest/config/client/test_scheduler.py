import unittest

from programy.config.file.yaml_file import YamlConfigurationFile
from programy.config.client.scheduler import SchedulerConfiguration
from programy.clients.events.console.config import ConsoleConfiguration

class SchedulerConfigurationTests(unittest.TestCase):

    def test_with_data(self):
        yaml = YamlConfigurationFile()
        self.assertIsNotNone(yaml)
        yaml.load_from_text("""
        console:
          scheduler:
            name: Scheduler1
            debug_level: 0
            add_listeners: True
            remove_all_jobs: True
        """, ConsoleConfiguration(), ".")

        bot_config = yaml.get_section("console")

        scheduler_config = SchedulerConfiguration()
        scheduler_config.load_config_section(yaml, bot_config, ".")

        self.assertEquals("Scheduler1", scheduler_config.name)
        self.assertEquals(0, scheduler_config.debug_level)
        self.assertTrue(scheduler_config.add_listeners)
        self.assertTrue(scheduler_config.remove_all_jobs)

    def test_without_data(self):
        yaml = YamlConfigurationFile()
        self.assertIsNotNone(yaml)
        yaml.load_from_text("""
        bot:
            scheduler:
        """, ConsoleConfiguration(), ".")

        bot_config = yaml.get_section("console")

        scheduler_config = SchedulerConfiguration()
        scheduler_config.load_config_section(yaml, bot_config, ".")

        self.assertIsNone(scheduler_config.name)
        self.assertEquals(0, scheduler_config.debug_level)
        self.assertFalse(scheduler_config.add_listeners)
        self.assertFalse(scheduler_config.remove_all_jobs)

    def test_with_no_data(self):
        yaml = YamlConfigurationFile()
        self.assertIsNotNone(yaml)
        yaml.load_from_text("""
        bot:
        """, ConsoleConfiguration(), ".")

        bot_config = yaml.get_section("console")

        scheduler_config = SchedulerConfiguration()
        scheduler_config.load_config_section(yaml, bot_config, ".")

        self.assertIsNone(scheduler_config.name)
        self.assertEquals(0, scheduler_config.debug_level)
        self.assertFalse(scheduler_config.add_listeners)
        self.assertFalse(scheduler_config.remove_all_jobs)
