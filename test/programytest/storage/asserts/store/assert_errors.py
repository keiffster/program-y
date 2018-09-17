import unittest

class ErrorStoreAsserts(unittest.TestCase):

    def assert_errors(self, store):

        errors = [["Error1", "aiml1.xml", "100", "200"],
                  ["Error1", "aiml2.xml", "200", "300"]]

        store.save_errors(errors)
