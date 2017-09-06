import unittest

from programy.utils.classes.loader import ClassLoader

#############################################################################
#

class ClassLoaderTests(unittest.TestCase):

    def test_instantiate_module_class(self):
        loader = ClassLoader()
        self.assertIsNotNone(loader)

        meta_class = loader.instantiate_class("programytest.utils.classes.testclass.TestClass")
        self.assertIsNotNone(meta_class)
        new_class = meta_class()
        self.assertIsNotNone(new_class)
        self.assertTrue(new_class.test_method())