import unittest

from programy.config.programy import ProgramyConfiguration
from programy.config.base import BaseConfigurationData


class MockConfiguration(BaseConfigurationData):

    def __init__(self):
        BaseConfigurationData.__init__(self, "test")

    def load_configuration(self, config_file, bot_root):
        return


class ProgramyConfigurationTests(unittest.TestCase):

    def test_programy(self):
        program_config = ProgramyConfiguration(MockConfiguration())
        self.assertIsNotNone(program_config)
        self.assertIsNotNone(program_config.client_configuration)




