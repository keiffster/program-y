import unittest

from programy.mappings.normal import NormalCollection

class NormaliseTests(unittest.TestCase):

    def test_normalise(self):
        collection = NormalCollection ()
        self.assertIsNotNone(collection)

        count = collection.load_from_text("""
            " www. ","www dot "
            " www."," www dot "
            ".com "," dot com "
            "%24"," dollars "
            "%27","'"
            "%2A","*"
            "%2D","-"
            "%2d","-"
            "%2E","."
            "%2e","."
            " aren t "," are not "
            " aren.t "," are not "
            " arent "," are not "
            " aren't "," are not "
            " are'nt "," are not "
            " arn t "," are not "
        """)
        self.assertEqual(count, 16)

        self.assertEqual(collection.normalise_string("That will be 24 %24"), "That will be 24 dollars")
        self.assertEqual(collection.normalise_string("You aren't him"), "You are not him")

        self.assertEqual(collection.normalise_string("www.google.com"), "www dot google dot com")

        self.assertIsNone(collection.normalise(" other "))