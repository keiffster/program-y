import unittest

from programy.storage.stores.nosql.mongo.dao.oob import OOB


class OOBTests(unittest.TestCase):

    def test_init_no_id(self):
        oob = OOB(name="test", oob_class="test.oobclass")

        self.assertIsNotNone(oob)
        self.assertIsNone(oob.id)
        self.assertEqual("test", oob.name)
        self.assertEqual("test.oobclass", oob.oob_class)
        self.assertEqual({'name': 'test', 'oob_class': 'test.oobclass'}, oob.to_document())

    def test_init_with_id(self):
        oob = OOB(name="test", oob_class="test.oobclass")
        oob.id = '666'

        self.assertIsNotNone(oob)
        self.assertIsNotNone(oob.id)
        self.assertEqual('666', oob.id)
        self.assertEqual("test", oob.name)
        self.assertEqual("test.oobclass", oob.oob_class)
        self.assertEqual({'_id': '666', 'name': 'test', 'oob_class': 'test.oobclass'}, oob.to_document())

    def test_from_document_no_id(self):
        oob1 = OOB.from_document({'name': 'test', 'oob_class': 'test.oobclass'})
        self.assertIsNotNone(oob1)
        self.assertIsNone(oob1.id)
        self.assertEqual("test", oob1.name)
        self.assertEqual("test.oobclass", oob1.oob_class)

    def test_from_document_with_id(self):
        oob2 = OOB.from_document({'_id': '666', 'name': 'test', 'oob_class': 'test.oobclass'})
        self.assertIsNotNone(oob2)
        self.assertIsNotNone(oob2.id)
        self.assertEqual('666', oob2.id)
        self.assertEqual("test", oob2.name)
        self.assertEqual("test.oobclass", oob2.oob_class)

    def test_from_document_no_id(self):
        oob1 = OOB.from_document({'name': 'test', 'oob_class': 'test.oobclass'})
        self.assertEquals("<OOB(id='n/a', name='test', oob_class='test.oobclass')>", str(oob1))

    def test_from_document_with_id(self):
        oob2 = OOB.from_document({'_id': '666', 'name': 'test', 'oob_class': 'test.oobclass'})
        self.assertEquals("<OOB(id='666', name='test', oob_class='test.oobclass')>", str(oob2))

