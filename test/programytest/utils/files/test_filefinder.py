import unittest
import os
from programy.utils.files.filefinder import FileFinder

#############################################################################
#
class MockFileFinder(FileFinder):

    def __init__(self):
        FileFinder.__init__(self)
        self.files = []

    def load_file_contents(self, id, filename, userid="*"):
        self.files.append(filename)


class FileFinderTests(unittest.TestCase):

    def test_find_files_no_subdir(self):
        file_finder = MockFileFinder()
        files = file_finder.find_files(os.path.dirname(__file__)+ os.sep + "test_files", subdir=False, extension=".txt")
        self.assertEqual(len(files), 3)
        self.assertEqual("file1.txt", files[0][0])
        self.assertEqual("file2.txt", files[1][0])
        self.assertEqual("file3.txt", files[2][0])

    def test_find_files_subdir(self):
        file_finder = MockFileFinder()
        files = file_finder.find_files(os.path.dirname(__file__)+ os.sep + "test_files", subdir=True, extension=".txt")
        self.assertEqual(len(files), 4)
        self.assertEqual("file1.txt", files[0][0])
        self.assertEqual("file2.txt", files[1][0])
        self.assertEqual("file3.txt", files[2][0])
        self.assertEqual("file4.txt", files[3][0])

    def test_load_dir_contents_no_subdir(self):
        file_finder = MockFileFinder()
        collection, file_maps = file_finder.load_dir_contents(os.path.dirname(__file__)+ os.sep + "test_files", subdir=False, extension=".txt")

        self.assertEqual(len(file_finder.files), 3)

        self.assertTrue("FILE1"in collection)
        self.assertTrue("FILE2"in collection)
        self.assertTrue("FILE3"in collection)

        self.assertTrue("FILE1"in file_maps)
        self.assertTrue("FILE2"in file_maps)
        self.assertTrue("FILE3"in file_maps)

    def test_load_dir_contents_subdir(self):
        file_finder = MockFileFinder()
        collection, file_maps = file_finder.load_dir_contents(os.path.dirname(__file__)+ os.sep + "test_files", subdir=True, extension=".txt")

        self.assertEqual(len(file_finder.files), 4)

        self.assertTrue("FILE1"in collection)
        self.assertTrue("FILE2"in collection)
        self.assertTrue("FILE3"in collection)
        self.assertTrue("FILE4"in collection)

        self.assertTrue("FILE1"in file_maps)
        self.assertTrue("FILE2"in file_maps)
        self.assertTrue("FILE3"in file_maps)
        self.assertTrue("FILE4"in collection)
