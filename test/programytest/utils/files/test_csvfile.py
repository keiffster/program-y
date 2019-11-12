import unittest
import os
from programy.utils.files.filewriter import CSVFile
from programytest.utils.files.utils import get_os_specific_path


class CSVFileTests(unittest.TestCase):

    def test_init(self):
        filename = get_os_specific_path() + 'csvfile.csv'

        if os.path.exists(filename):
            os.remove(filename)

        self.assertFalse(os.path.exists(filename))

        csvfile = CSVFile(filename)
        self.assertIsNotNone(csvfile)

        self.assertEqual("/tmp/csvfile.csv", csvfile.filename)
        self.assertEqual("utf-8", csvfile.encoding)
        self.assertTrue(os.path.exists(filename))

        csvfile.write_line(None, ["A", "B", "C"])

        csvfile.flush()

        os.remove(filename)

        self.assertFalse(os.path.exists(filename))



