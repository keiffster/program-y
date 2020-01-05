import os
import unittest
from programy.utils.files.filewriter import FileWriter
from programytest.utils.files.utils import get_os_specific_path


class MockFileWriterConfig(object):

    def __init__(self, name, delete=True, fileformat='txt', encoding='utf-8'):
        self.filename = name
        self.delete_on_start = delete
        self.file_format = fileformat
        self.encoding = encoding


class FileWriterTests(unittest.TestCase):

    def test_init_txt(self):

        filename = get_os_specific_path()+'writefile.tmp'

        if os.path.exists(filename):
            os.remove(filename)

        self.assertFalse(os.path.exists(filename))

        filewriter = FileWriter(MockFileWriterConfig(filename, delete=True, fileformat='txt', encoding='utf-8'))
        self.assertIsNotNone(filewriter)

        filewriter.write_header()
        self.assertEquals("line", filewriter.format_row_as_text("line"))

        self.assertTrue(os.path.exists(filename))

        os.remove(filename)

        self.assertFalse(os.path.exists(filename))

    def test_init_txt_with_existing_file(self):

        filename = get_os_specific_path()+'writefile.tmp'

        if os.path.exists(filename) is False:
            with open(filename, 'w') as newfile:
                newfile.writelines(["line1"])

        self.assertTrue(os.path.exists(filename))

        filewriter = FileWriter(MockFileWriterConfig(filename, delete=True, fileformat='txt', encoding='utf-8'))
        self.assertIsNotNone(filewriter)

        self.assertTrue(os.path.exists(filename))

        os.remove(filename)

        self.assertFalse(os.path.exists(filename))


    def test_init_csv(self):

        filename = get_os_specific_path()+'writefile.tmp'

        if os.path.exists(filename):
            os.remove(filename)

        self.assertFalse(os.path.exists(filename))

        filewriter = FileWriter(MockFileWriterConfig(filename, delete=True, fileformat='csv', encoding='utf-8'))
        self.assertIsNotNone(filewriter)

        self.assertTrue(os.path.exists(filename))

        os.remove(filename)

        self.assertFalse(os.path.exists(filename))

    def test_invalid_file_format(self):

        filename = get_os_specific_path()+'writefile.tmp'

        with self.assertRaises(Exception):
            filewriter = FileWriter(MockFileWriterConfig(filename, fileformat="unknown"))

