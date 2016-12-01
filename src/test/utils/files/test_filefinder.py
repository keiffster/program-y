import unittest
import os
from programy.utils.files.filefinder import FileFinder

#############################################################################
#
class TestFileFinder(FileFinder):
    def __init__(self):
        FileFinder.__init__(self)
        self.files = []

    def load_file_contents(self, filename):
        self.files.append(filename)

class FileFinderTests(unittest.TestCase):

    def test_find_files_no_subdir(self):
        file_finder = TestFileFinder()
        files = file_finder.find_files(os.path.dirname(__file__)+ "/test_files", subdir=False, extension=".txt")
        self.assertEqual(len(files), 3)

    def test_find_files_subdir(self):
        file_finder = TestFileFinder()
        files = file_finder.find_files(os.path.dirname(__file__)+ "/test_files", subdir=True, extension=".txt")
        self.assertEqual(len(files), 4)

    def test_load_dir_contents_no_subdir(self):
        file_finder = TestFileFinder()
        file_finder.load_dir_contents(os.path.dirname(__file__)+ "/test_files", subdir=False, extension=".txt")
        self.assertEqual(len(file_finder.files), 3)

    def test_load_dir_contents_subdir(self):
        file_finder = TestFileFinder()
        file_finder.load_dir_contents(os.path.dirname(__file__)+ "/test_files", subdir=True, extension=".txt")
        self.assertEqual(len(file_finder.files), 4)
