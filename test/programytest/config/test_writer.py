import unittest
import unittest.mock

from programy.config.writer import ConfigurationWriter


class MockConfigurationWriter(ConfigurationWriter):

    def __init__(self):
        self.written_data = None

    def write_yaml(self, filename, data):
        self.written_data = data


class ConfigurationWriterTests(unittest.TestCase):

    def test_execute_all_with_defaults(self):

        args = unittest.mock.Mock()
        args.clients = ['all']
        args.defaults = True

        writer = MockConfigurationWriter()
        writer.execute(args)

        self.assertIsNotNone(writer.written_data)

    def test_execute_all_without_defaults(self):

        args = unittest.mock.Mock()
        args.clients = ['all']
        args.defaults = False

        writer = MockConfigurationWriter()
        writer.execute(args)

        self.assertIsNotNone(writer.written_data)