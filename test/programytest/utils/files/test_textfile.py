import unittest
import os
from programy.utils.files.filewriter import TextFile
from programytest.utils.files.utils import get_os_specific_path


class MockFileWriter:

    def format_row_as_text(self, row):
        return row


class TextFileTests(unittest.TestCase):

    def test_init(self):
        filename = get_os_specific_path() + 'textfile.tmp'

        if os.path.exists(filename):
            os.remove(filename)

        self.assertFalse(os.path.exists(filename))

        textfile = TextFile(filename)
        self.assertIsNotNone(textfile)

        self.assertEqual("/tmp/textfile.tmp", textfile.filename)
        self.assertEqual("utf-8", textfile.encoding)
        self.assertTrue(os.path.exists(filename))

        textfile.write_line(MockFileWriter(), "this is a row")

        os.remove(filename)

        self.assertFalse(os.path.exists(filename))



