import os

from programy.config.file.factory import ConfigurationFactory
from programy.config.client.client import ClientConfiguration
from test.config.file.base_file_tests import ConfigurationBaseFileTests

class LoadConfigurationDataTests(ConfigurationBaseFileTests):

    def test_load_config_data_yaml(self):
        client_config = ClientConfiguration()
        ConfigurationFactory.load_configuration_from_file(client_config, os.path.dirname(__file__)+"/test_yaml.yaml")
        self.assert_config_data(client_config)

    def test_load_config_data_json(self):
        client_config = ClientConfiguration()
        ConfigurationFactory.load_configuration_from_file(client_config, os.path.dirname(__file__)+"/test_json.json")
        self.assert_config_data(client_config)

    def test_load_config_data_xml(self):
        client_config = ClientConfiguration()
        ConfigurationFactory.load_configuration_from_file(client_config, os.path.dirname(__file__)+"/test_xml.xml")
        self.assert_config_data(client_config)

