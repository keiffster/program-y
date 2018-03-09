import unittest
import os

from programy.utils.files.filewriter import TextFile
from programy.utils.files.filewriter import CSVFile
from programy.utils.files.filewriter import FileWriter
from programy.utils.files.filewriter import ConversationFileWriter
from programy.utils.files.filewriter import ErrorsFileWriter
from programy.utils.files.filewriter import DuplicatesFileWriter
from programy.config.brain.debugfile import DebugFileConfiguration

class MockFileWriter:

    def format_row_as_text(self, elements):
        return elements[0]


class OSFileTester(unittest.TestCase):

    def remove_file_assert_not_there(self, filename):
        if os.path.exists(filename):
            os.remove(filename)
        self.assertFalse(os.path.exists(filename))


class TextFileTests(OSFileTester):

    test_file = "./testfile.txt"

    def test_init(self):
        self.remove_file_assert_not_there(TextFileTests.test_file)

        text_file = TextFile(TextFileTests.test_file)
        self.assertIsNotNone(text_file)
        text_file.write_line(MockFileWriter(), ["test"])

        self.assertTrue(os.path.exists(TextFileTests.test_file))

        self.remove_file_assert_not_there(TextFileTests.test_file)


class CSVFileTests(OSFileTester):

    test_file = "./testfile.csv"

    def test_init(self):
        self.remove_file_assert_not_there(TextFileTests.test_file)

        csv_file = CSVFile(TextFileTests.test_file)
        self.assertIsNotNone(csv_file)
        csv_file.write_line(MockFileWriter(), ["test"])

        self.assertTrue(os.path.exists(TextFileTests.test_file))

        self.remove_file_assert_not_there(TextFileTests.test_file)


class FileWriterTests(OSFileTester):

    def test_as_text(self):
        configuration = DebugFileConfiguration(name="tests", filename="./testfile.txt")

        self.remove_file_assert_not_there(configuration.filename)

        file_writer = FileWriter(configuration)
        self.assertIsNotNone(file_writer)

        self.remove_file_assert_not_there(configuration.filename)

    def test_as_csv(self):
        configuration = DebugFileConfiguration(name="tests", filename="./testfile.txt")

        self.remove_file_assert_not_there(configuration.filename)

        file_writer = FileWriter(configuration)
        self.assertIsNotNone(file_writer)

        self.remove_file_assert_not_there(configuration.filename)


class ConversationFileWriterTests(OSFileTester):

    def test_writing(self):
        configuration = DebugFileConfiguration(name="tests", filename="./testfile.txt")

        self.remove_file_assert_not_there(configuration.filename)

        writer = ConversationFileWriter(configuration)
        self.assertIsNotNone(writer)
        writer.log_question_and_answer("testid", "hello", "hi there")

        self.assertTrue(os.path.exists(configuration.filename))

        self.remove_file_assert_not_there(configuration.filename)


class ErrorsFileWriterTests(OSFileTester):

    def test_error_writing(self):
        configuration = DebugFileConfiguration(name="tests", filename="./testfile.txt")

        self.remove_file_assert_not_there(configuration.filename)

        writer = ErrorsFileWriter(configuration)
        self.assertIsNotNone(writer)

        writer.save_entry("error1", "test.aiml", 100, 103)
        self.assertIsNotNone(writer.entries)
        self.assertEquals(1, len(writer.entries))
        writer.save_entry("error2", "test.aiml", 200, 203)
        self.assertEquals(2, len(writer.entries))

        writer.save_content()
        self.assertTrue(os.path.exists(configuration.filename))

        self.remove_file_assert_not_there(configuration.filename)


class DuplicatesFileWriterTests(OSFileTester):

    def test_error_writing(self):
        configuration = DebugFileConfiguration(name="tests", filename="./testfile.txt")

        self.remove_file_assert_not_there(configuration.filename)

        writer = DuplicatesFileWriter(configuration)
        self.assertIsNotNone(writer)

        writer.save_entry("duplicate1", "test.aiml", 100, 103)
        self.assertIsNotNone(writer.entries)
        self.assertEquals(1, len(writer.entries))
        writer.save_entry("duplicate2", "test.aiml", 200, 203)
        self.assertEquals(2, len(writer.entries))

        writer.save_content()
        self.assertTrue(os.path.exists(configuration.filename))

        self.remove_file_assert_not_there(configuration.filename)