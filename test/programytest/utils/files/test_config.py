import unittest
from programy.utils.files.filewriter import FileWriterConfiguration


class FileWriterConfigurationTests(unittest.TestCase):

    def test_init_defaults(self):
        config = FileWriterConfiguration("filename.txt")

        self.assertEquals("filename.txt", config.filename)
        self.assertEquals(None, config.file_format)
        self.assertEquals("a", config.mode)
        self.assertEquals("utf-8", config.encoding)
        self.assertEquals(False, config.delete_on_start)

    def test_init_no_defaults(self):
        config = FileWriterConfiguration("filename2.txt", fileformat="txt", mode="r", encoding="ascii", delete_on_start=True)

        self.assertEquals("filename2.txt", config.filename)
        self.assertEquals("txt", config.file_format)
        self.assertEquals("r", config.mode)
        self.assertEquals("ascii", config.encoding)
        self.assertEquals(True, config.delete_on_start)
