import os
import unittest
from programy.utils.files.filewriter import ContentFileWriter
from programy.utils.files.filewriter import FileWriterConfiguration
from programytest.utils.files.utils import get_os_specific_path


class ContentFileWriterTests(unittest.TestCase):

    def test_init(self):
        config = FileWriterConfiguration(filename="filename.test", fileformat="txt", mode="a", encoding="utf-8", delete_on_start=False)

        writer = ContentFileWriter(config, content_type="txt")
        self.assertIsNotNone(writer)

        writer.display_debug_info()

        if os.path.exists("filename.test"):
            os.remove("filename.test")
            self.assertFalse(os.path.exists("filename.test"))
