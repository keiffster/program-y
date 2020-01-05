import unittest
from unittest.mock import patch
import os
import shutil
from programy.admin.tool import AdminTool


class MockAdminTool(AdminTool):

    def __init__(self):
        AdminTool.__init__(self)
        self.text = ""

    def display(self, text):
        self.text += text


class AdminToolTests(unittest.TestCase):

    def get_temp_dir(self):
        if os.name == 'posix':
            return '/tmp'
        elif os.name == 'nt':
            import tempfile
            return tempfile.gettempdir()
        else:
            raise Exception("Unknown operating system [%s]" % os.name)

    def create_file(self, filename):
        with open(filename, "w+") as file:
            file.writelines(["line1", "line2", "line3"])
            file.flush()
            file.close()

    def test_recursive_copy(self):
        tmp_dir = self.get_temp_dir() + os.sep +"programy"

        if os.path.exists(tmp_dir):
            shutil.rmtree(tmp_dir)

        os.mkdir(tmp_dir)

        src_dir =  tmp_dir + os.sep + "src"
        os.mkdir(src_dir)
        src_sub_dir = tmp_dir + os.sep + "src" + os.sep + "sub"
        os.mkdir(src_sub_dir)
        src_sub_dir2 = tmp_dir + os.sep + "src" + os.sep + "sub2"
        os.mkdir(src_sub_dir2)
        dest_dir = tmp_dir + os.sep + "dest"
        os.mkdir(dest_dir)

        self.create_file(src_dir + os.sep + "file1.txt")
        self.create_file(src_dir + os.sep + "file2.txt")
        self.create_file(src_dir + os.sep + "file3.txt")
        self.create_file(src_dir + os.sep + "sub" + os.sep + "file4.txt")

        AdminTool.recursive_copy(src_dir, dest_dir)

        self.assertTrue(os.path.exists(src_dir + os.sep + "file1.txt"))
        self.assertTrue(os.path.exists(src_dir + os.sep + "file2.txt"))
        self.assertTrue(os.path.exists(src_dir + os.sep + "file3.txt"))
        self.assertTrue(os.path.exists(src_dir + os.sep + "sub" + os.sep + "file4.txt"))
        self.assertTrue(os.path.exists(src_dir + os.sep + "sub2"))

        if os.path.exists(tmp_dir):
            shutil.rmtree(tmp_dir)

    def test_delete_folder_contents(self):
        tmp_dir = self.get_temp_dir() + os.sep +"programy"

        if os.path.exists(tmp_dir):
            shutil.rmtree(tmp_dir)

        os.mkdir(tmp_dir)

        src_dir =  tmp_dir + os.sep + "src"
        os.mkdir(src_dir)
        src_sub_dir = tmp_dir + os.sep + "src" + os.sep + "sub"
        os.mkdir(src_sub_dir)
        dest_dir = tmp_dir + os.sep + "dest"
        os.mkdir(dest_dir)

        self.create_file(src_dir + os.sep + "file1.txt")
        self.create_file(src_dir + os.sep + "file2.txt")
        self.create_file(src_dir + os.sep + "file3.txt")
        self.create_file(src_dir + os.sep + "sub" + os.sep + "file4.txt")

        self.assertTrue(os.path.exists(src_dir + os.sep + "file1.txt"))
        self.assertTrue(os.path.exists(src_dir + os.sep + "file2.txt"))
        self.assertTrue(os.path.exists(src_dir + os.sep + "file3.txt"))
        self.assertTrue(os.path.exists(src_dir + os.sep + "sub" + os.sep + "file4.txt"))

        AdminTool.delete_folder_contents(tmp_dir)

        self.assertFalse(os.path.exists(src_dir + os.sep + "file1.txt"))
        self.assertFalse(os.path.exists(src_dir + os.sep + "file2.txt"))
        self.assertFalse(os.path.exists(src_dir + os.sep + "file3.txt"))
        self.assertFalse(os.path.exists(src_dir + os.sep + "sub" + os.sep + "file4.txt"))

        if os.path.exists(tmp_dir):
            shutil.rmtree(tmp_dir)

    def test_make_executable(self):
        tmp_dir = self.get_temp_dir() + os.sep +"programy"

        if os.path.exists(tmp_dir):
            shutil.rmtree(tmp_dir)

        os.mkdir(tmp_dir)

        filepath = tmp_dir + os.sep + "file1.txt"
        self.create_file(filepath)

        self.assertTrue(os.path.exists(filepath))

        AdminTool.make_executable(filepath)

        if os.path.exists(tmp_dir):
            shutil.rmtree(tmp_dir)

    def test_make_all_executable(self):
        tmp_dir = self.get_temp_dir() + os.sep +"programy"

        if os.path.exists(tmp_dir):
            shutil.rmtree(tmp_dir)

        os.mkdir(tmp_dir)

        src_dir =  tmp_dir + os.sep + "src"
        os.mkdir(src_dir)
        src_sub_dir = tmp_dir + os.sep + "src" + os.sep + "sub"
        os.mkdir(src_sub_dir)
        dest_dir = tmp_dir + os.sep + "dest"
        os.mkdir(dest_dir)

        self.create_file(src_dir + os.sep + "file1.txt")
        self.create_file(src_dir + os.sep + "file2.txt")
        self.create_file(src_dir + os.sep + "file3.txt")
        self.create_file(src_dir + os.sep + "sub" + os.sep + "file4.txt")

        AdminTool.make_all_executable(tmp_dir)

        if os.path.exists(tmp_dir):
            shutil.rmtree(tmp_dir)

    def test_list_bots(self):
        tool = MockAdminTool()
        self.assertEqual("", tool.text)

        tool.list_bots()

        self.assertEquals("""Available bots are:
	alice2-y	professor-y	rosie-y	talk-y	y-bot	servusai-y	template-y	traintimes-y
	To download use 'python3 -m programy.admin.tool download <bot-name>'
Additional components are:
	textblob
	To install use 'python3 -m programy.admin.tool install <component>'""", tool.text)

    def patch_wget_download(self, url):
        return "mock.bot"

    @patch("programy.admin.tool.AdminTool.wget_download", patch_wget_download)
    def test_download_bot(self):
        tool = MockAdminTool()
        self.assertEqual("", tool.text)

        filename = tool.download_bot("y-bot")
        self.assertEqual("mock.bot", filename)

        self.assertEqual("""Downloading [y-bot] from [https://github.com/keiffster/y-bot/archive/master.zip]
Download complete""", tool.text)

    def test_zip_dir_name_from_filename(self):
        self.assertEqual("filename", AdminTool.zip_dir_name_from_filename('filename.zip'))
        self.assertEqual("filename", AdminTool.zip_dir_name_from_filename('filename'))

    def test_extract_bot_no_remove(self):
        tool = AdminTool()

        tmp_dir = self.get_temp_dir() + os.sep +"programy"

        if os.path.exists(tmp_dir):
            shutil.rmtree(tmp_dir)
        os.mkdir(tmp_dir)
        shutil.copyfile(os.path.dirname(__file__) + os.sep + "bot.zip", tmp_dir + os.sep + "bot.zip")

        tool.extract_bot(tmp_dir + os.sep + "bot.zip", path=tmp_dir, remove_after=False)

        self.assertTrue(os.path.exists(tmp_dir + os.sep + "bot.zip"))
        self.assertTrue(os.path.exists(tmp_dir + os.sep + "test1.txt"))
        self.assertTrue(os.path.exists(tmp_dir + os.sep + "test2.txt"))

        shutil.rmtree(tmp_dir)

    def test_extract_bot_with_remove(self):
        tool = AdminTool()

        tmp_dir = self.get_temp_dir() + os.sep +"programy"

        if os.path.exists(tmp_dir):
            shutil.rmtree(tmp_dir)
        os.mkdir(tmp_dir)
        shutil.copyfile(os.path.dirname(__file__) + os.sep + "bot.zip", tmp_dir + os.sep + "bot.zip")

        tool.extract_bot(tmp_dir + os.sep + "bot.zip", path=tmp_dir, remove_after=True)

        self.assertFalse(os.path.exists(tmp_dir + os.sep + "bot.zip"))
        self.assertTrue(os.path.exists(tmp_dir + os.sep + "test1.txt"))
        self.assertTrue(os.path.exists(tmp_dir + os.sep + "test2.txt"))

        shutil.rmtree(tmp_dir)

    def patch_download_and_make_active(self, bot_name):
        pass # Do nothing

    @patch("programy.admin.tool.AdminTool.download_and_make_active", patch_download_and_make_active)
    def test_install_bot(self):
        tool = MockAdminTool()
        self.assertEquals("", tool.text)

        tool.install_bot(["test", "y-bot"])
        self.assertEqual("""
To run y-bot bot in console mode, use the following commands
\tcd scripts/xnix\t./y-bot.sh""", tool.text)

    def test_install_bot_unknown(self):
        tool = MockAdminTool()
        self.assertEquals("", tool.text)

        with self.assertRaises(Exception):
            tool.install_bot(["test", "unknown"])

    def patch_install_textblob(self):
        pass # Do nothing

    @patch("programy.admin.tool.AdminTool.install_textblob", patch_install_textblob)
    def test_install_additional(self):
        tool = MockAdminTool()
        self.assertEquals("", tool.text)

        tool.install_additional(["test", "textblob"])
        self.assertEqual("Installing additional components for textblob", tool.text)

    def test_install_additional_invalid(self):
        tool = MockAdminTool()
        self.assertEquals("", tool.text)

        with self.assertRaises(Exception):
            tool.install_additional(["test", "xxxxxxx"])

    def test_show_execute_help(self):
        tool = MockAdminTool()
        self.assertEqual("", tool.text)

        tool.show_execute_help("y-bot")

        self.assertEqual("""
To run y-bot bot in console mode, use the following commands
\tcd scripts/xnix\t./y-bot.sh""", tool.text)

    def test_show_help(self):
        tool = MockAdminTool()
        self.assertEqual("", tool.text)

        tool.show_help()

        self.assertEqual("""Available commands are:
\thelp	list	download <bot-name>	install <component>""", tool.text)

    def test_run_no_words(self):
        tool = MockAdminTool()
        tool.run([])
        self.assertIsNotNone(tool.text)
        self.assertTrue(tool.text.startswith("Available commands are:"))

    def test_run_unknown_primary_command(self):
        tool = MockAdminTool()
        tool.run(['unknown'])
        self.assertIsNotNone(tool.text)
        self.assertTrue(tool.text.startswith("Unknown primary command [unknown]"))

    def test_run_missing_bot_name(self):
        tool = MockAdminTool()
        tool.run(['download'])
        self.assertIsNotNone(tool.text)
        self.assertTrue(tool.text.startswith("Missing bot name from download command"))

    def test_run_list(self):
        tool = MockAdminTool()
        tool.run(['list'])
        self.assertIsNotNone(tool.text)

    def test_run_download(self):
        tool = MockAdminTool()
        tool.run(['download'])
        self.assertIsNotNone(tool.text)

    def test_run_install(self):
        tool = MockAdminTool()
        tool.run(['install'])
        self.assertIsNotNone(tool.text)

    def test_run_help(self):
        tool = MockAdminTool()
        tool.run(['help'])
        self.assertIsNotNone(tool.text)
