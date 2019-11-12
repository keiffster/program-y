import unittest.mock
from programy.storage.entities.store import Store


class StoreTests(unittest.TestCase):

    def test_init(self):
        store = Store()
        self.assertIsNotNone(store)

    def test_split_into_fields(self):
        pass

    def test_process_line(self):
        pass

    def test_upload_from_text(self):
        pass

    def test_get_file_processor(self):
        pass

    def test_get_just_filename_from_filepath(self):
        pass

    def test_upload_from_directory(self):
        pass

    def test_upload_from_file(self):
        pass

