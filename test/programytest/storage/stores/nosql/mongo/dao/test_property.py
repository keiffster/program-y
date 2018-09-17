import unittest

from programy.storage.stores.nosql.mongo.dao.property import Property
from programy.storage.stores.nosql.mongo.dao.property import DefaultVariable
from programy.storage.stores.nosql.mongo.dao.property import Regex


class PropertyTests(unittest.TestCase):

    def test_init_no_id(self):
        property = Property(name='name', value='value')

        self.assertIsNotNone(property)
        self.assertIsNone(property.id)
        self.assertEqual('name', property.name)
        self.assertEqual('value', property.value)
        self.assertEqual({'value': 'value', 'name': 'name'}, property.to_document())

    def test_init_with_id(self):
        property = Property(name='name', value='value')
        property.id = '666'

        self.assertIsNotNone(property)
        self.assertIsNotNone(property.id)
        self.assertEqual('666', property.id)
        self.assertEqual('name', property.name)
        self.assertEqual('value', property.value)
        self.assertEqual({'_id': '666', 'value': 'value', 'name': 'name'}, property.to_document())

    def test_from_document(self):
        property1 = Property.from_document({'value': 'value', 'name': 'name'})
        self.assertIsNotNone(property1)
        self.assertIsNone(property1.id)
        self.assertEqual('name', property1.name)
        self.assertEqual('value', property1.value)

        property2 = Property.from_document({'_id': '666', 'value': 'value', 'name': 'name'})
        self.assertIsNotNone(property2)
        self.assertIsNotNone(property2.id)
        self.assertEqual('666', property2.id)
        self.assertEqual('666', property2.id)
        self.assertEqual('name', property2.name)
        self.assertEqual('value', property2.value)


class DefaultVariableTests(unittest.TestCase):

    def test_init_no_id(self):
        property = DefaultVariable(name='name', value='value')

        self.assertIsNotNone(property)
        self.assertIsNone(property.id)
        self.assertEqual('name', property.name)
        self.assertEqual('value', property.value)
        self.assertEqual({'value': 'value', 'name': 'name'}, property.to_document())

    def test_init_with_id(self):
        property = DefaultVariable(name='name', value='value')
        property.id = '666'

        self.assertIsNotNone(property)
        self.assertIsNotNone(property.id)
        self.assertEqual('666', property.id)
        self.assertEqual('name', property.name)
        self.assertEqual('value', property.value)
        self.assertEqual({'_id': '666', 'value': 'value', 'name': 'name'}, property.to_document())

    def test_from_document(self):
        property1 = DefaultVariable.from_document({'value': 'value', 'name': 'name'})
        self.assertIsNotNone(property1)
        self.assertIsNone(property1.id)
        self.assertEqual('name', property1.name)
        self.assertEqual('value', property1.value)

        property2 = DefaultVariable.from_document({'_id': '666', 'value': 'value', 'name': 'name'})
        self.assertIsNotNone(property2)
        self.assertIsNotNone(property2.id)
        self.assertEqual('666', property2.id)
        self.assertEqual('666', property2.id)
        self.assertEqual('name', property2.name)
        self.assertEqual('value', property2.value)


class RegexTests(unittest.TestCase):

    def test_init_no_id(self):
        property = Regex(name='name', value='value')

        self.assertIsNotNone(property)
        self.assertIsNone(property.id)
        self.assertEqual('name', property.name)
        self.assertEqual('value', property.value)
        self.assertEqual({'value': 'value', 'name': 'name'}, property.to_document())

    def test_init_with_id(self):
        property = Regex(name='name', value='value')
        property.id = '666'

        self.assertIsNotNone(property)
        self.assertIsNotNone(property.id)
        self.assertEqual('666', property.id)
        self.assertEqual('name', property.name)
        self.assertEqual('value', property.value)
        self.assertEqual({'_id': '666', 'value': 'value', 'name': 'name'}, property.to_document())

    def test_from_document(self):
        property1 = Regex.from_document({'value': 'value', 'name': 'name'})
        self.assertIsNotNone(property1)
        self.assertIsNone(property1.id)
        self.assertEqual('name', property1.name)
        self.assertEqual('value', property1.value)

        property2 = Regex.from_document({'_id': '666', 'value': 'value', 'name': 'name'})
        self.assertIsNotNone(property2)
        self.assertIsNotNone(property2.id)
        self.assertEqual('666', property2.id)
        self.assertEqual('666', property2.id)
        self.assertEqual('name', property2.name)
        self.assertEqual('value', property2.value)
