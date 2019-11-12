import os
import unittest
from programy.utils.files.filewriter import ErrorsFileWriter
from programy.utils.files.filewriter import FileWriterConfiguration
from programytest.utils.files.utils import get_os_specific_path


class ErrorsFileWriterTests(unittest.TestCase):

    def test_init(self):

        filename = get_os_specific_path() + os.sep + "errirs.txt"
        config = FileWriterConfiguration(filename=filename, fileformat="txt", mode="a", encoding="utf-8", delete_on_start=False)

        writer = ErrorsFileWriter(config)
        self.assertIsNotNone(writer)

        writer.save_entry("<xml>Duplicate with line numbers</xml>", "test.aiml", 100, 666)
        writer.save_entry("<xml>Duplicate with no line numbers</xml>", "test2.aiml")
        self.assertEquals(2, len(writer.entries))
        writer.save_content()

        self.assertTrue(os.path.exists(filename))

        if os.path.exists(filename):
            os.remove(filename)
            self.assertFalse(os.path.exists(filename))
