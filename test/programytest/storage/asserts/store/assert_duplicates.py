import unittest

class DuplicateStoreAsserts(unittest.TestCase):

    def assert_duplicates(self, store):

        duplicates = [["Duplicate1", "aiml1.xml", "100", "200"],
                      ["Duplicate2", "aiml2.xml", "200", "300"]]

        store.save_duplicates(duplicates)
