import unittest
import os
import os.path


class MockAIMLParser(object):

    def __init__(self):
        self.aimls = []

    def parse_csv_line(self, aiml_csv):
        self.aimls.append(aiml_csv)

    def parse_category(self, category_xml, namespace, topic_element=None, add_to_graph=True, userid="*"):
        self.aimls.append(category_xml)


class CategoryStoreAsserts(unittest.TestCase):

    def assert_category_storage(self, store):
        store.empty()

        store.store_category("TEST", "user1", '*', '*', 'HELLO', "Hi there!")
        store.commit()

        mock_parser = MockAIMLParser()
        store.load_all(mock_parser)

        self.assertEqual(1, len(mock_parser.aimls))

    def assert_category_by_groupid_storage(self, store):
        store.empty()

        store.store_category("TEST1", "user1", '*', '*', 'HELLO', "Hi there!")
        store.store_category("TEST2", "user1", '*', '*', 'HELLO', "Hi there!")
        store.commit()

        mock_parser = MockAIMLParser()
        store.load_categories("TEST2", mock_parser)

        self.assertEqual(1, len(mock_parser.aimls))

    def assert_upload_from_file(self, store):
        store.empty()

        store.upload_from_file(os.path.dirname(__file__) + os.sep + "data" + os.sep + "categories" + os.sep + "kinghorn.aiml", verbose=True)
        store.commit ()

        mock_parser = MockAIMLParser()
        store.load_all(mock_parser)

        self.assertEqual(3, len(mock_parser.aimls))

    def assert_upload_from_directory(self, store):
        store.empty()

        store.upload_from_directory(os.path.dirname(__file__) + os.sep + "data" + os.sep + "categories", subdir=False)
        store.commit ()

        mock_parser = MockAIMLParser()
        store.load_all(mock_parser)

        self.assertEqual(3, len(mock_parser.aimls))
