import unittest
import os
from programy.utils.files.filewriter import TextFile
from programy.utils.files.filewriter import CSVFile
from programy.utils.files.filewriter import ConversationFileWriter
from programy.utils.files.filewriter import FileWriter
from programy.utils.files.filewriter import FileWriterConfiguration
from programy.utils.files.filewriter import ContentFileWriter
from programy.utils.files.filewriter import ErrorsFileWriter
from programy.utils.files.filewriter import DuplicatesFileWriter


def get_os_specific_path():
    if os.name == 'posix':
        return '/tmp/'
    elif os.name == 'nt':
        return ''
    else:
        raise Exception("Unknown OS [%s]" % os.name)


class MockFileWriterConfig(object):

    def __init__(self, name, delete=True, format='txt', encoding='utf-8'):
        self.filename = name
        self.delete_on_start = delete
        self.file_format = format
        self.encoding = encoding


class TextFileTests(unittest.TestCase):

    def test_creation(self):

        filename = get_os_specific_path()+'textfile.tmp'

        if os.path.exists(filename):
            os.remove(filename)

        self.assertFalse(os.path.exists(filename))

        textfile = TextFile(filename)
        self.assertIsNotNone(textfile)

        self.assertTrue(os.path.exists(filename))

        os.remove(filename)

        self.assertFalse(os.path.exists(filename))


class CSVFileTests(unittest.TestCase):

    def test_creation(self):

        filename = get_os_specific_path()+'csvfile.tmp'

        if os.path.exists(filename):
            os.remove(filename)

        self.assertFalse(os.path.exists(filename))

        csvfile = CSVFile(filename)
        self.assertIsNotNone(csvfile)

        self.assertTrue(os.path.exists(filename))

        os.remove(filename)

        self.assertFalse(os.path.exists(filename))


class FileWriterTests(unittest.TestCase):

    def test_writeline(self):

        filename = get_os_specific_path()+'writefile.tmp'

        if os.path.exists(filename):
            os.remove(filename)

        self.assertFalse(os.path.exists(filename))

        filewriter = FileWriter(MockFileWriterConfig(filename))
        self.assertIsNotNone(filewriter)

        self.assertTrue(os.path.exists(filename))

        os.remove(filename)

        self.assertFalse(os.path.exists(filename))

    def test_invalid_file_format(self):

        filename = get_os_specific_path()+'writefile.tmp'

        with self.assertRaises(Exception):
            filewriter = FileWriter(MockFileWriterConfig(filename, format="unknown"))


class ConversationFileWriterTests(unittest.TestCase):

    def test_init(self):
        config =FileWriterConfiguration(filename="filename.test", file_format="txt", mode="a", encoding="utf-8", delete_on_start=False)

        writer = ConversationFileWriter(config)
        self.assertIsNotNone(writer)

        if os.path.exists("filename.test"):
            os.remove("filename.test")
            self.assertFalse(os.path.exists("filename.test"))


class ContentFileWriterTests(unittest.TestCase):

    def test_init(self):
        config = FileWriterConfiguration(filename="filename.test", file_format="txt", mode="a", encoding="utf-8", delete_on_start=False)

        writer = ContentFileWriter(config, content_type="txt")
        self.assertIsNotNone(writer)

        if os.path.exists("filename.test"):
            os.remove("filename.test")
            self.assertFalse(os.path.exists("filename.test"))


class ErrorsFileWriterTests(unittest.TestCase):

    def test_init(self):
        config = FileWriterConfiguration(filename="filename.test", file_format="txt", mode="a", encoding="utf-8", delete_on_start=False)

        writer = ErrorsFileWriter(config)
        self.assertIsNotNone(writer)

        if os.path.exists("filename.test"):
            os.remove("filename.test")
            self.assertFalse(os.path.exists("filename.test"))


class DuplicatesFileWriterTests(unittest.TestCase):

    def test_init(self):
        config = FileWriterConfiguration(filename="filename.test", file_format="txt", mode="a", encoding="utf-8", delete_on_start=False)

        writer = DuplicatesFileWriter(config)
        self.assertIsNotNone(writer)

        if os.path.exists("filename.test"):
            os.remove("filename.test")
            self.assertFalse(os.path.exists("filename.test"))
