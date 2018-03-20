import unittest
from unittest.mock import Mock
import os
import shutil

from programy.admin.tool import AdminTool


class MockAdminTool(AdminTool):

    _create_app = False
    _create_script = False

    @staticmethod
    def reset():
        MockAdminTool._create_app = False
        MockAdminTool._create_script = False

    @staticmethod
    def create_app(args):
        MockAdminTool._create_app = True

    @staticmethod
    def create_script(args):
        MockAdminTool._create_script = True


class AdminToolTests(unittest.TestCase):

    @staticmethod
    def get_tmp_folder():
        if os.name == 'posix':
            return "/tmp"
        elif os.name == 'nt':
            return "C:\\Windows\\Temp"
        else:
            raise Exception("Unknown operation system for tests [%s]"%os.name)

    def ensure_folder_does_not_exist(self, folder):
        if os.path.exists(folder):
            shutil.rmtree(folder)
        self.assertFalse(os.path.exists(folder))

    def ensure_file_does_not_exist(self, file):
        if os.path.exists(file):
            os.remove(file)
        self.assertFalse(os.path.exists(file))

    def test_create_sub_folder(self):
        temp_folder = self.get_tmp_folder()
        test_folder = temp_folder + os.sep + "prgytest"

        self.ensure_folder_does_not_exist(test_folder)

        AdminTool.create_sub_folder(temp_folder, "prgytest")
        self.assertTrue(os.path.exists(test_folder))

        self.ensure_folder_does_not_exist(test_folder)

    def test_create_file_with_content(self):
        temp_folder = self.get_tmp_folder()
        test_file = temp_folder + os.sep + "test.file"
        self.ensure_file_does_not_exist(test_file)

        AdminTool.create_file_with_content(test_file, "test data")
        self.assertTrue(os.path.exists(test_file))

        self.ensure_file_does_not_exist(test_file)

    def test_create_file_with_content_with_extra(self):
        temp_folder = self.get_tmp_folder()
        test_file = temp_folder + os.sep + "test.file"
        self.ensure_file_does_not_exist(test_file)

        AdminTool.create_file_with_content(test_file, "test data", extra="Extra")
        self.assertTrue(os.path.exists(test_file))

        self.ensure_file_does_not_exist(test_file)

    def test_make_executable(self):
        temp_folder = self.get_tmp_folder()
        test_file = temp_folder + os.sep + "test.file"
        self.ensure_file_does_not_exist(test_file)

        AdminTool.create_file_with_content(test_file, "test data")
        AdminTool.make_executable(test_file)
        self.assertTrue(os.path.exists(test_file))

        self.ensure_file_does_not_exist(test_file)

    def test_create_aiml_folder(self):
        temp_folder = self.get_tmp_folder()
        aiml_folder = temp_folder + os.sep + "aiml"
        self.ensure_folder_does_not_exist(aiml_folder)

        AdminTool.create_aiml_folder(temp_folder, False)
        self.assertTrue(os.path.exists(aiml_folder))

        self.ensure_folder_does_not_exist(aiml_folder)

    def test_create_aiml_folder_with_defaults(self):
        temp_folder = self.get_tmp_folder()
        aiml_folder = temp_folder + os.sep + "aiml"
        self.ensure_folder_does_not_exist(aiml_folder)

        aiml_file = temp_folder + os.sep + "aiml" + os.sep + "hello.aiml"
        self.ensure_file_does_not_exist(aiml_file)

        AdminTool.create_aiml_folder(temp_folder, True)
        self.assertTrue(os.path.exists(aiml_folder))
        self.assertTrue(os.path.exists(aiml_file))

        self.ensure_file_does_not_exist(aiml_file)
        self.ensure_folder_does_not_exist(aiml_folder)

    def test_create_logging_file_unix(self):
        temp_folder = self.get_tmp_folder()

        logging_file = temp_folder + os.sep + "logging.yaml"
        self.ensure_file_does_not_exist(logging_file)

        AdminTool.create_logging_file(temp_folder, "unix")
        self.assertTrue(os.path.exists(logging_file))

        self.ensure_file_does_not_exist(logging_file)

    def test_create_initial_properties(self):
        temp_folder = self.get_tmp_folder()
        AdminTool.create_sub_folder(temp_folder, "config")

        props_file = temp_folder + os.sep + "config" + os.sep + "properties.txt"
        self.ensure_file_does_not_exist(props_file)

        AdminTool.create_initial_properties(temp_folder)
        self.assertTrue(os.path.exists(props_file))

        self.ensure_file_does_not_exist(props_file)

    def test_create_config_file_console(self):
        temp_folder = self.get_tmp_folder()

        config_file = temp_folder + os.sep + "config.yaml"
        self.ensure_file_does_not_exist(config_file)

        AdminTool.create_config_file(temp_folder, "console")
        self.assertTrue(os.path.exists(config_file))

        self.ensure_file_does_not_exist(config_file)

    def test_create_config_file_webchat(self):
        temp_folder = self.get_tmp_folder()

        config_file = temp_folder + os.sep + "config.yaml"
        self.ensure_file_does_not_exist(config_file)

        AdminTool.create_config_file(temp_folder, "webchat")
        self.assertTrue(os.path.exists(config_file))

        self.ensure_file_does_not_exist(config_file)

    def test_create_config_file_rest(self):
        temp_folder = self.get_tmp_folder()

        config_file = temp_folder + os.sep + "config.yaml"
        self.ensure_file_does_not_exist(config_file)

        AdminTool.create_config_file(temp_folder, "rest")
        self.assertTrue(os.path.exists(config_file))

        self.ensure_file_does_not_exist(config_file)

    def test_create_config_file_xmpp(self):
        temp_folder = self.get_tmp_folder()

        config_file = temp_folder + os.sep + "config.yaml"
        self.ensure_file_does_not_exist(config_file)

        AdminTool.create_config_file(temp_folder, "xmpp")
        self.assertTrue(os.path.exists(config_file))

        self.ensure_file_does_not_exist(config_file)

    def test_create_config_file_socket(self):
        temp_folder = self.get_tmp_folder()

        config_file = temp_folder + os.sep + "config.yaml"
        self.ensure_file_does_not_exist(config_file)

        AdminTool.create_config_file(temp_folder, "socket")
        self.assertTrue(os.path.exists(config_file))

        self.ensure_file_does_not_exist(config_file)

    def test_create_config_file_unknown(self):
        temp_folder = self.get_tmp_folder()

        config_file = temp_folder + os.sep + "config.yaml"
        self.ensure_file_does_not_exist(config_file)

        with self.assertRaises(Exception):
            AdminTool.create_config_file(temp_folder, "unknown")

        self.ensure_file_does_not_exist(config_file)

    def test_create_shell_script_unix_console(self):
        temp_folder = self.get_tmp_folder()

        shell_script = temp_folder + os.sep + "console.sh"
        self.ensure_file_does_not_exist(shell_script)

        AdminTool.create_shell_script(temp_folder, 'console', 'unix')
        self.assertTrue(os.path.exists(shell_script))

        self.ensure_file_does_not_exist(shell_script)

    def test_create_shell_script_unix_webchat(self):
        temp_folder = self.get_tmp_folder()

        shell_script = temp_folder + os.sep + "webchat.sh"
        self.ensure_file_does_not_exist(shell_script)

        AdminTool.create_shell_script(temp_folder, 'webchat', 'unix')
        self.assertTrue(os.path.exists(shell_script))

        self.ensure_file_does_not_exist(shell_script)

    def test_create_shell_script_unix_rest(self):
        temp_folder = self.get_tmp_folder()

        shell_script = temp_folder + os.sep + "rest.sh"
        self.ensure_file_does_not_exist(shell_script)

        AdminTool.create_shell_script(temp_folder, 'rest', 'unix')
        self.assertTrue(os.path.exists(shell_script))

        self.ensure_file_does_not_exist(shell_script)

    def test_create_shell_script_unix_xmpp(self):
        temp_folder = self.get_tmp_folder()

        shell_script = temp_folder + os.sep + "xmpp.sh"
        self.ensure_file_does_not_exist(shell_script)

        AdminTool.create_shell_script(temp_folder, 'xmpp', 'unix')
        self.assertTrue(os.path.exists(shell_script))

        self.ensure_file_does_not_exist(shell_script)

    def test_create_shell_script_unix_twitter(self):
        temp_folder = self.get_tmp_folder()

        shell_script = temp_folder + os.sep + "twitter.sh"
        self.ensure_file_does_not_exist(shell_script)

        AdminTool.create_shell_script(temp_folder, 'twitter', 'unix')
        self.assertTrue(os.path.exists(shell_script))

        self.ensure_file_does_not_exist(shell_script)

    def test_create_shell_script_unix_socket(self):
        temp_folder = self.get_tmp_folder()

        shell_script = temp_folder + os.sep + "socket.sh"
        self.ensure_file_does_not_exist(shell_script)

        AdminTool.create_shell_script(temp_folder, 'socket', 'unix')
        self.assertTrue(os.path.exists(shell_script))

        self.ensure_file_does_not_exist(shell_script)

    def test_create_shell_script_unix_unknown(self):
        temp_folder = self.get_tmp_folder()

        shell_script = temp_folder + os.sep + "unknown.sh"
        self.ensure_file_does_not_exist(shell_script)

        with self.assertRaises(Exception):
            AdminTool.create_shell_script(temp_folder, 'unknown', 'unix')

        self.ensure_file_does_not_exist(shell_script)

    def test_create_shell_script_windows_console(self):
        temp_folder = self.get_tmp_folder()

        shell_script = temp_folder + os.sep + "console.cmd"
        self.ensure_file_does_not_exist(shell_script)

        AdminTool.create_shell_script(temp_folder, 'console', 'windows')
        self.assertTrue(os.path.exists(shell_script))

        self.ensure_file_does_not_exist(shell_script)

    def test_create_shell_script_windows_webchat(self):
        temp_folder = self.get_tmp_folder()

        shell_script = temp_folder + os.sep + "webchat.cmd"
        self.ensure_file_does_not_exist(shell_script)

        AdminTool.create_shell_script(temp_folder, 'webchat', 'windows')
        self.assertTrue(os.path.exists(shell_script))

        self.ensure_file_does_not_exist(shell_script)

    def test_create_shell_script_windows_rest(self):
        temp_folder = self.get_tmp_folder()

        shell_script = temp_folder + os.sep + "rest.cmd"
        self.ensure_file_does_not_exist(shell_script)

        AdminTool.create_shell_script(temp_folder, 'rest', 'windows')
        self.assertTrue(os.path.exists(shell_script))

        self.ensure_file_does_not_exist(shell_script)

    def test_create_shell_script_windows_xmpp(self):
        temp_folder = self.get_tmp_folder()

        shell_script = temp_folder + os.sep + "xmpp.cmd"
        self.ensure_file_does_not_exist(shell_script)

        AdminTool.create_shell_script(temp_folder, 'xmpp', 'windows')
        self.assertTrue(os.path.exists(shell_script))

        self.ensure_file_does_not_exist(shell_script)

    def test_create_shell_script_windows_twitter(self):
        temp_folder = self.get_tmp_folder()

        shell_script = temp_folder + os.sep + "twitter.cmd"
        self.ensure_file_does_not_exist(shell_script)

        AdminTool.create_shell_script(temp_folder, 'twitter', 'windows')
        self.assertTrue(os.path.exists(shell_script))

        self.ensure_file_does_not_exist(shell_script)

    def test_create_shell_script_windows_socket(self):
        temp_folder = self.get_tmp_folder()

        shell_script = temp_folder + os.sep + "socket.cmd"
        self.ensure_file_does_not_exist(shell_script)

        AdminTool.create_shell_script(temp_folder, 'socket', 'windows')
        self.assertTrue(os.path.exists(shell_script))

        self.ensure_file_does_not_exist(shell_script)

    def test_create_shell_script_windows_unknown(self):
        temp_folder = self.get_tmp_folder()

        shell_script = temp_folder + os.sep + "unknown.cmd"
        self.ensure_file_does_not_exist(shell_script)

        with self.assertRaises(Exception):
            AdminTool.create_shell_script(temp_folder, 'unknown', 'windows')

        self.ensure_file_does_not_exist(shell_script)

    def test_create_shell_script_unknown_unknown(self):
        temp_folder = self.get_tmp_folder()

        shell_script = temp_folder + os.sep + "unknown.cmd"
        self.ensure_file_does_not_exist(shell_script)

        with self.assertRaises(Exception):
            AdminTool.create_shell_script(temp_folder, 'unknown', 'unknown')

        self.ensure_file_does_not_exist(shell_script)

    def test_execute_create_app(self):

        args = Mock()
        args.create = 'app'

        tool = MockAdminTool()
        MockAdminTool.reset()

        self.assertFalse(tool._create_script)
        self.assertFalse(tool._create_app)
        tool.execute(args)
        self.assertFalse(tool._create_script)
        self.assertTrue(tool._create_app)

    def test_execute_create_script(self):

        args = Mock()
        args.create = 'script'

        tool = MockAdminTool()
        MockAdminTool.reset()

        self.assertFalse(tool._create_app)
        self.assertFalse(tool._create_script)
        tool.execute(args)
        self.assertFalse(tool._create_app)
        self.assertTrue(tool._create_script)

    def test_execute_create_unknown(self):

        args = Mock()
        args.create = 'unknown'

        tool = MockAdminTool()
        MockAdminTool.reset()

        self.assertFalse(tool._create_app)
        self.assertFalse(tool._create_script)
        with self.assertRaises(Exception):
            tool.execute(args)

    def test_create_app(self):
        temp_folder = self.get_tmp_folder() + os.sep + "prgytest"
        self.ensure_folder_does_not_exist(temp_folder)

        args = Mock()
        args.location = temp_folder
        args.app = 'console'
        args.os = 'unix'
        args.replace = False
        args.default = True

        AdminTool.create_app(args)

        self.assertTrue(os.path.exists(temp_folder))
        self.assertTrue(os.path.exists(temp_folder + os.sep + "config"))
        self.assertTrue(os.path.exists(temp_folder + os.sep + "conversations"))
        self.assertTrue(os.path.exists(temp_folder + os.sep + "maps"))
        self.assertTrue(os.path.exists(temp_folder + os.sep + "sets"))
        self.assertTrue(os.path.exists(temp_folder + os.sep + "rdf"))
        self.assertTrue(os.path.exists(temp_folder + os.sep + "spelling"))
        self.assertTrue(os.path.exists(temp_folder + os.sep + "storage"))

        self.assertTrue(os.path.exists(temp_folder + os.sep + "config.yaml"))
        self.assertTrue(os.path.exists(temp_folder + os.sep + "logging.yaml"))
        self.assertTrue(os.path.exists(temp_folder + os.sep + "config" + os.sep + "properties.txt"))
        self.assertTrue(os.path.exists(temp_folder + os.sep + "aiml" + os.sep + "hello.aiml"))

        self.ensure_folder_does_not_exist(temp_folder)

    def test_create_script_without_path(self):
        temp_folder = self.get_tmp_folder()

        args = Mock()
        args.location = temp_folder
        args.app = 'console'
        args.os = 'unix'

        shell_script = temp_folder + os.sep + "console.sh"
        self.ensure_file_does_not_exist(shell_script)

        AdminTool.create_script(args)
        self.assertTrue(os.path.exists(shell_script))

        self.ensure_file_does_not_exist(shell_script)

    def test_create_script_with_path(self):
        temp_folder = self.get_tmp_folder()

        args = Mock()
        args.location = temp_folder
        args.app = 'console'
        args.os = 'unix'
        args.path = './path1/pth2'

        shell_script = temp_folder + os.sep + "console.sh"
        self.ensure_file_does_not_exist(shell_script)

        AdminTool.create_script(args)
        self.assertTrue(os.path.exists(shell_script))

        self.ensure_file_does_not_exist(shell_script)

