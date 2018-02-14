import unittest
from unittest.mock import Mock
import os
import shutil

from programy.admin.admin import AdminTool


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

    def test_create_config_file(self):
        temp_folder = self.get_tmp_folder()

        config_file = temp_folder + os.sep + "config.yaml"
        self.ensure_file_does_not_exist(config_file)

        AdminTool.create_config_file(temp_folder, "console")
        self.assertTrue(os.path.exists(config_file))

        self.ensure_file_does_not_exist(config_file)

    def test_create_shell_script(self):
        temp_folder = self.get_tmp_folder()

        shell_script = temp_folder + os.sep + "console.sh"
        self.ensure_file_does_not_exist(shell_script)

        AdminTool.create_shell_script(temp_folder, 'console', 'unix')
        self.assertTrue(os.path.exists(shell_script))

        self.ensure_file_does_not_exist(shell_script)

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

