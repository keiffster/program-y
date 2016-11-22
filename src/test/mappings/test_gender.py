import unittest

from programy.mappings.gender import GenderCollection


class GenderTests(unittest.TestCase):

    def test_collection(self):
        collection = GenderCollection()
        self.assertIsNotNone(collection)

        count = collection.load_from_text("""
                " with him "," with her "
                " with her "," with him "
                " to him "," to her "
                " to her "," to him "
                " on him "," on her "
                " on her "," on him "
                " in him "," in her "
                " in her "," in him "
                " for him "," for her "
                " for her "," for him "
                " he "," she "
                " his "," her "
                " him "," her "
                " her "," his "
                " she "," he "
        """)
        self.assertEqual(count, 15)

        self.assertEqual(collection.genderise_string("This is with him "), "This is with her")
