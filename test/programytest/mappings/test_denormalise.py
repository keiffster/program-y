import unittest

from programy.mappings.denormal import DenormalCollection


class DenormaliseTests(unittest.TestCase):

    def test_collection(self):
        collection = DenormalCollection()
        self.assertIsNotNone(collection)

        count = collection.load_from_text("""
            " www dot ","www."
            " dot com ",".com "
            " dot co ",".co"
            " dot uk ",".uk"
            " dot net ",".net"
            " dot ca ",".ca"
            " dot de ",".de"
            " dot jp ",".jp"
            " dot fr ",".fr"
            " dot es ",".es"
            " dot mil ",".mil"
            " dot co ",".co"
            " are not "," aren't "
            " can not "," can't "
            " could not "," couldn't "
            " could have "," could've "
         """)
        self.assertEqual(count, 16)

        self.assertEqual(collection.denormalise_string("You are not him"), "You aren't him")
        self.assertEqual(collection.denormalise_string("keithsterling dot co dot uk"), "keithsterling.co.uk")

        self.assertEqual(collection.denormalise_string("www dot google dot com"), "www.google.com")

        self.assertIsNone(collection.denormalise(" dot cox "))

