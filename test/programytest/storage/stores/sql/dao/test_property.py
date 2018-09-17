import unittest

from programy.storage.stores.sql.dao.property import Property
from programy.storage.stores.sql.dao.property import DefaultVariable
from programy.storage.stores.sql.dao.property import Regex


class PropertyTests(unittest.TestCase):

    def test_init(self):
        property1 = Property(name='name', value='value')
        self.assertIsNotNone(property1)
        self.assertEqual("<Property(id='n/a', name='name', value='value')>", str(property1))

        property2 = Property(id=1, name='name', value='value')
        self.assertIsNotNone(property2)
        self.assertEqual("<Property(id='1', name='name', value='value')>", str(property2))


class DefaultVariableTests(unittest.TestCase):

    def test_init(self):
        property1 = DefaultVariable(name='name', value='value')
        self.assertIsNotNone(property1)
        self.assertEqual("<DefaultVariable(id='n/a', name='name', value='value')>", str(property1))

        property2 = DefaultVariable(id=1, name='name', value='value')
        self.assertIsNotNone(property2)
        self.assertEqual("<DefaultVariable(id='1', name='name', value='value')>", str(property2))


class RegexTests(unittest.TestCase):

    def test_init(self):
        property1 = Regex(name='name', value='value')
        self.assertIsNotNone(property1)
        self.assertEqual("<Regex(id='n/a', name='name', value='value')>", str(property1))

        property2 = Regex(id=1, name='name', value='value')
        self.assertIsNotNone(property2)
        self.assertEqual("<Regex(id='1', name='name', value='value')>", str(property2))
