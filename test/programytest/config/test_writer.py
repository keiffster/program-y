import unittest
import unittest.mock
from unittest.mock import patch
import os
import os.path

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

    def test_execute_no_args(self):
        with self.assertRaises(Exception):
            writer = MockConfigurationWriter()
            writer.execute(None)

    def test_execute_no_clients(self):
        args = unittest.mock.Mock()
        args.clients = None
        with self.assertRaises(Exception):
            writer = MockConfigurationWriter()
            writer.execute(args)

    def test_execute_console(self):
        args = unittest.mock.Mock()
        args.clients = ['console']
        args.defaults = False

        writer = MockConfigurationWriter()
        writer.execute(args)

        self.assertIsNotNone(writer.written_data)

    def test_execute_slack(self):
        args = unittest.mock.Mock()
        args.clients = ['slack']
        args.defaults = False

        writer = MockConfigurationWriter()
        writer.execute(args)

        self.assertIsNotNone(writer.written_data)

    def test_execute_socket(self):
        args = unittest.mock.Mock()
        args.clients = ['socket']
        args.defaults = False

        writer = MockConfigurationWriter()
        writer.execute(args)

        self.assertIsNotNone(writer.written_data)

    def test_execute_telegram(self):
        args = unittest.mock.Mock()
        args.clients = ['telegram']
        args.defaults = False

        writer = MockConfigurationWriter()
        writer.execute(args)

        self.assertIsNotNone(writer.written_data)

    def test_execute_twitter(self):
        args = unittest.mock.Mock()
        args.clients = ['twitter']
        args.defaults = False

        writer = MockConfigurationWriter()
        writer.execute(args)

        self.assertIsNotNone(writer.written_data)

    def test_execute_xmpp(self):
        args = unittest.mock.Mock()
        args.clients = ['xmpp']
        args.defaults = False

        writer = MockConfigurationWriter()
        writer.execute(args)

        self.assertIsNotNone(writer.written_data)

    def test_execute_rest(self):
        args = unittest.mock.Mock()
        args.clients = ['rest']
        args.defaults = False

        writer = MockConfigurationWriter()
        writer.execute(args)

        self.assertIsNotNone(writer.written_data)

    def test_execute_facebook(self):
        args = unittest.mock.Mock()
        args.clients = ['facebook']
        args.defaults = False

        writer = MockConfigurationWriter()
        writer.execute(args)

        self.assertIsNotNone(writer.written_data)

    def test_execute_kik(self):
        args = unittest.mock.Mock()
        args.clients = ['kik']
        args.defaults = False

        writer = MockConfigurationWriter()
        writer.execute(args)

        self.assertIsNotNone(writer.written_data)

    def test_execute_line(self):
        args = unittest.mock.Mock()
        args.clients = ['line']
        args.defaults = False

        writer = MockConfigurationWriter()
        writer.execute(args)

        self.assertIsNotNone(writer.written_data)

    def test_execute_twilio(self):
        args = unittest.mock.Mock()
        args.clients = ['twilio']
        args.defaults = False

        writer = MockConfigurationWriter()
        writer.execute(args)

        self.assertIsNotNone(writer.written_data)

    def test_execute_viber(self):
        args = unittest.mock.Mock()
        args.clients = ['viber']
        args.defaults = False

        writer = MockConfigurationWriter()
        writer.execute(args)

        self.assertIsNotNone(writer.written_data)

    def test_execute_sanic(self):
        args = unittest.mock.Mock()
        args.clients = ['sanic']
        args.defaults = False

        writer = MockConfigurationWriter()
        writer.execute(args)

        self.assertIsNotNone(writer.written_data)

    def get_temp_dir(self):
        if os.name == 'posix':
            return '/tmp'
        elif os.name == 'nt':
            import tempfile
            return tempfile.gettempdir()
        else:
            raise Exception("Unknown operating system [%s]" % os.name)

    def test_write_yaml(self):

        tmp_dir  = self.get_temp_dir()
        fullpath = tmp_dir + os.sep + "test.yaml"

        if os.path.exists(fullpath):
            os.remove(fullpath)

        writer = ConfigurationWriter()
        writer.write_yaml(fullpath, {"test": "value"})

        self.assertTrue(os.path.exists(fullpath))

        if os.path.exists(fullpath):
            os.remove(fullpath)

    def test_create_arguments(self):
        parser = ConfigurationWriter.create_arguments()
        self.assertIsNotNone(parser)

    def test_run_no_args(self):
        writer = ConfigurationWriter()
        with self.assertRaises(SystemExit):
            writer.run()

    def test_run_with_args(self):
        args = unittest.mock.Mock()
        args.clients = ['sanic']
        args.defaults = False

        writer = ConfigurationWriter()
        writer.run(args)

    def patch_execute(self, args):
        raise Exception("Mock Exception")

    @patch("programy.config.writer.ConfigurationWriter.execute", patch_execute)
    def test_run_exception_with_args(self):
        args = unittest.mock.Mock()
        args.clients = ['sanic']
        args.defaults = False

        writer = ConfigurationWriter()
        writer.run(args)
