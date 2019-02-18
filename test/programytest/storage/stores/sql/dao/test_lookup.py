
import unittest

from programy.storage.stores.sql.dao.lookup import Denormal
from programy.storage.stores.sql.dao.lookup import Normal
from programy.storage.stores.sql.dao.lookup import Gender
from programy.storage.stores.sql.dao.lookup import Person
from programy.storage.stores.sql.dao.lookup import Person2

class DenormalTests(unittest.TestCase):

    def test_init(self):
        lookup1 = Denormal(key="key", value="value")
        self.assertIsNotNone(lookup1)
        self.assertEqual("<Denormal(id='n/a', key='key', value='value')>", str(lookup1))

        lookup2 = Denormal(id=1, key="key", value="value")
        self.assertIsNotNone(lookup2)
        self.assertEqual("<Denormal(id='1', key='key', value='value')>", str(lookup2))


class NormalTests(unittest.TestCase):

    def test_init(self):
        lookup1 = Normal(key="key", value="value")
        self.assertIsNotNone(lookup1)
        self.assertEqual("<Normal(id='n/a', key='key', value='value')>", str(lookup1))

        lookup2 = Normal(id=1, key="key", value="value")
        self.assertIsNotNone(lookup2)
        self.assertEqual("<Normal(id='1', key='key', value='value')>", str(lookup2))

class GenderTests(unittest.TestCase):

    def test_init(self):
        lookup1 = Gender(key="key", value="value")
        self.assertIsNotNone(lookup1)
        self.assertEqual("<Gender(id='n/a', key='key', value='value')>", str(lookup1))

        lookup2 = Gender(id=1, key="key", value="value")
        self.assertIsNotNone(lookup2)
        self.assertEqual("<Gender(id='1', key='key', value='value')>", str(lookup2))

class PersonTests(unittest.TestCase):

    def test_init(self):
        lookup1 = Person(key="key", value="value")
        self.assertIsNotNone(lookup1)
        self.assertEqual("<Person(id='n/a', key='key', value='value')>", str(lookup1))

        lookup2 = Person(id=1, key="key", value="value")
        self.assertIsNotNone(lookup2)
        self.assertEqual("<Person(id='1', key='key', value='value')>", str(lookup2))

class Person2Tests(unittest.TestCase):

    def test_init(self):
        lookup1 = Person2(key="key", value="value")
        self.assertIsNotNone(lookup1)
        self.assertEqual("<Person2(id='n/a', key='key', value='value')>", str(lookup1))

        lookup2 = Person2(id=1, key="key", value="value")
        self.assertIsNotNone(lookup2)
        self.assertEqual("<Person2(id='1', key='key', value='value')>", str(lookup2))
