import unittest

class MockAIMLParser(object):

    def __init__(self):
        self.aimls = []

    def parse_csv_line(self, aiml_csv):
        self.aimls.append(aiml_csv)


class CategoryStoreAsserts(unittest.TestCase):

    def assert_category_storage(self, store):
        store.empty()

        store.store_category("TEST", "user1", '*', '*', 'HELLO', "Hi there!")
        store.commit()

        mock_parser = MockAIMLParser()
        store.load_all(mock_parser)

        self.assertEquals(1, len(mock_parser.aimls))

    def assert_category_by_groupid_storage(self, store):
        store.empty()

        store.store_category("TEST1", "user1", '*', '*', 'HELLO', "Hi there!")
        store.store_category("TEST2", "user1", '*', '*', 'HELLO', "Hi there!")
        store.commit()

        mock_parser = MockAIMLParser()
        store.load_categories("TEST2", mock_parser)

        self.assertEquals(1, len(mock_parser.aimls))
