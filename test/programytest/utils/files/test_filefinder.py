import os
import unittest

from programy.utils.files.filefinder import FileFinder


#############################################################################
#
class MockFileFinder(FileFinder):

    def __init__(self, except_on_load=False):
        FileFinder.__init__(self)
        self.files = []
        self.except_on_load = except_on_load

    def load_file_contents(self, fileid, filename, userid="*"):
        if self.except_on_load is True:
            raise Exception("Mock Exception")

        self.files.append(filename)
        return None


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

    def test_find_files_subdir_bad_dir(self):
        file_finder = MockFileFinder()
        files = file_finder.find_files(os.path.dirname(__file__)+ os.sep + "test_filesXXX", subdir=True, extension=".txt")
        self.assertEqual(len(files), 0)

    def test_load_dir_contents_no_subdir_filename_as_userid_false(self):
        file_finder = MockFileFinder()
        collection, file_maps = file_finder.load_dir_contents(os.path.dirname(__file__)+ os.sep + "test_files",
                                                              subdir=False, extension=".txt", filename_as_userid=False)

        self.assertEqual(len(file_finder.files), 3)

        self.assertTrue("FILE1"in collection)
        self.assertTrue("FILE2"in collection)
        self.assertTrue("FILE3"in collection)

        self.assertTrue("FILE1"in file_maps)
        self.assertTrue("FILE2"in file_maps)
        self.assertTrue("FILE3"in file_maps)

    def test_load_dir_contents_no_subdir_filename_as_userid_true(self):
        file_finder = MockFileFinder()
        collection, file_maps = file_finder.load_dir_contents(os.path.dirname(__file__)+ os.sep + "test_files",
                                                              subdir=False, extension=".txt", filename_as_userid=True)

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

    def test_load_dir_contents_subdir_except_on_load(self):
        file_finder = MockFileFinder(except_on_load=True)
        collection, file_maps = file_finder.load_dir_contents(os.path.dirname(__file__)+ os.sep + "test_files", subdir=True, extension=".txt")
        self.assertEquals({}, collection)
        self.assertEquals({}, file_maps)

    def test_load_single_file_contents(self):
        file_finder = MockFileFinder()
        collection = file_finder.load_single_file_contents(os.path.dirname(__file__)+ os.sep + "test_files" + os.sep + "file1.txt")
        self.assertIsNotNone(collection)
        self.assertTrue("file1" in collection)

    def test_load_single_file_contents_with_except(self):
        file_finder = MockFileFinder(except_on_load=True)
        collection = file_finder.load_single_file_contents(os.path.dirname(__file__)+ os.sep + "test_files" + os.sep + "file1.txt")
        self.assertIsNotNone(collection)
        self.assertEquals({}, collection)

    def test_get_just_filename_from_filepath(self):
        self.assertEquals("", FileFinder.get_just_filename_from_filepath(""))
        self.assertEquals("filename", FileFinder.get_just_filename_from_filepath("filename"))
        self.assertEquals("filename", FileFinder.get_just_filename_from_filepath("filename.txt"))
        self.assertEquals("filename", FileFinder.get_just_filename_from_filepath("somepath/otherpath/filename"))
        self.assertEquals("filename", FileFinder.get_just_filename_from_filepath("somepath/otherpath/filename.txt"))
        self.assertEquals("filename", FileFinder.get_just_filename_from_filepath("somepath/otherpath/filename.txt.pdf"))
