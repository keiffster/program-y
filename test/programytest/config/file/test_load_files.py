import os

from programy.config.file.factory import ConfigurationFactory
from programy.clients.events.console.config import ConsoleConfiguration

from programytest.config.file.base_file_tests import ConfigurationBaseFileTests

# Hint
# Created the appropriate yaml file, then convert to json and xml using the following tool
# https://codebeautify.org/yaml-to-json-xml-csv

class LoadConfigurationDataTests(ConfigurationBaseFileTests):

    def test_load_config_data_yaml(self):
        config_data = ConfigurationFactory.load_configuration_from_file(ConsoleConfiguration(), os.path.dirname(__file__)+ os.sep + "test_yaml.yaml")
        self.assert_configuration(config_data)

    def test_load_config_data_json(self):
        config_data = ConfigurationFactory.load_configuration_from_file(ConsoleConfiguration(), os.path.dirname(__file__)+ os.sep + "test_json.json")
        self.assert_configuration(config_data)

    def test_load_config_data_xml(self):
        config_data = ConfigurationFactory.load_configuration_from_file(ConsoleConfiguration(), os.path.dirname(__file__)+ os.sep + "test_xml.xml")
        self.assert_configuration(config_data)

