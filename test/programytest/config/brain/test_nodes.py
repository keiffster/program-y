import unittest

from programy.config.file.yaml_file import YamlConfigurationFile
from programy.config.brain.nodes import BrainNodesConfiguration
from programy.clients.events.console.config import ConsoleConfiguration

class BrainNodesConfigurationTests(unittest.TestCase):

    def test_with_data(self):
        yaml = YamlConfigurationFile()
        self.assertIsNotNone(yaml)
        yaml.load_from_text("""
        brain:
            nodes:
                pattern_nodes: $BOT_ROOT/config/pattern_nodes.conf
                template_nodes: $BOT_ROOT/config/template_nodes.conf
        """, ConsoleConfiguration(), ".")

        brain_config = yaml.get_section("brain")

        nodes_config = BrainNodesConfiguration()
        nodes_config.load_config_section(yaml, brain_config, ".")

        self.assertEquals("./config/pattern_nodes.conf", nodes_config.pattern_nodes)
        self.assertEquals("./config/template_nodes.conf", nodes_config.template_nodes)

    def test_without_data(self):
        yaml = YamlConfigurationFile()
        self.assertIsNotNone(yaml)
        yaml.load_from_text("""
        brain:
            nodes:
        """, ConsoleConfiguration(), ".")

        brain_config = yaml.get_section("brain")

        nodes_config = BrainNodesConfiguration()
        nodes_config.load_config_section(yaml, brain_config, ".")

        self.assertIsNone(nodes_config.pattern_nodes)
        self.assertIsNone(nodes_config.template_nodes)

    def test_with_no_data(self):
        yaml = YamlConfigurationFile()
        self.assertIsNotNone(yaml)
        yaml.load_from_text("""
        brain:
        """, ConsoleConfiguration(), ".")

        brain_config = yaml.get_section("brain")

        nodes_config = BrainNodesConfiguration()
        nodes_config.load_config_section(yaml, brain_config, ".")

        self.assertIsNone(nodes_config.pattern_nodes)
        self.assertIsNone(nodes_config.template_nodes)
