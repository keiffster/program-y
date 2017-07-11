import os

from programy.config.file.factory import ConfigurationFactory
from programy.config.sections.client.console import ConsoleConfiguration

from test.config.file.base_file_tests import ConfigurationBaseFileTests

# Hint
# Created the appropriate yaml file, then convert to json and xml using the following tool
# https://codebeautify.org/yaml-to-json-xml-csv

class LoadConfigurationDataTests(ConfigurationBaseFileTests):

    def test_load_config_data_yaml(self):
        client_config = ConsoleConfiguration()
        config_data = ConfigurationFactory.load_configuration_from_file(client_config, os.path.dirname(__file__)+"/test_yaml.yaml")
        self.assert_config_data(config_data)

    def test_load_config_data_json(self):
        client_config = ConsoleConfiguration()
        config_data = ConfigurationFactory.load_configuration_from_file(client_config, os.path.dirname(__file__)+"/test_json.json")
        self.assert_config_data(client_config)

    def test_load_config_data_xml(self):
        client_config = ConsoleConfiguration()
        config_data = ConfigurationFactory.load_configuration_from_file(client_config, os.path.dirname(__file__)+"/test_xml.xml")
        self.assert_config_data(config_data)

