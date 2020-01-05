import unittest.mock

from programy.parser.pattern.nodes.base import MultiValueDict


class MultiValueDictTests(unittest.TestCase):

    def test_add_remove(self):
        multidict = MultiValueDict()
        multidict["name"] = "value1"
        multidict["name"].append("value2")

        self.assertTrue("name" in multidict)

        multidict.remove("name", "value1")

        self.assertTrue("name" in multidict)

        multidict.remove("name", "value2")

        self.assertFalse("name" in multidict)

    def test_remove_no_key(self):
        multidict = MultiValueDict()
        multidict["name"] = "value1"
        multidict["name"].append("value2")

        multidict.remove("other", "value1")

    def test_remove_no_value(self):
        multidict = MultiValueDict()
        multidict["name"] = "value1"
        multidict["name"].append("value2")

        multidict.remove("name", "value3")
