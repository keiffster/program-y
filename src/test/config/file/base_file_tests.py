import unittest

class ConfigurationBaseFileTests(unittest.TestCase):

    def assert_config_data(self, config_data):
        self.assertIsNotNone(config_data)

        #TODO Add tests on data here