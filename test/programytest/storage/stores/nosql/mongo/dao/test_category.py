import unittest

from programy.storage.stores.nosql.mongo.dao.category import Category


class CategoryTests(unittest.TestCase):

    def test_init(self):
        category1 = Category("groupid", "userid", "topic", "that", "pattern", "template")
        self.assertIsNotNone(category1)
        self.assertEqual("<Category(id='n/a', groupid='groupid', userid='userid', topic='topic', that='that', pattern='pattern', template='template'>", str(category1))
        doc1 = category1.to_document()
        self.assertIsNotNone(doc1)
        self.assertEqual({'groupid': 'groupid', 'pattern': 'pattern', 'template': 'template', 'that': 'that', 'topic': 'topic', 'userid': 'userid'}, doc1)

        category2 = Category("groupid", "userid", "topic", "that", "pattern", "template", id=None)
        self.assertIsNotNone(category2)
        self.assertEqual("<Category(id='n/a', groupid='groupid', userid='userid', topic='topic', that='that', pattern='pattern', template='template'>", str(category2))
        doc2 = category1.to_document()
        self.assertIsNotNone(doc2)
        self.assertEqual({'groupid': 'groupid', 'pattern': 'pattern', 'template': 'template', 'that': 'that', 'topic': 'topic', 'userid': 'userid'}, doc2)

        category3 = Category("groupid", "userid", "topic", "that", "pattern", "template", id=666)
        self.assertIsNotNone(category3)
        self.assertEqual("<Category(id='666', groupid='groupid', userid='userid', topic='topic', that='that', pattern='pattern', template='template'>", str(category3))
        doc3 = category3.to_document()
        self.assertIsNotNone(doc3)
        self.assertEqual({'_id': 666, 'groupid': 'groupid', 'pattern': 'pattern', 'template': 'template', 'that': 'that', 'topic': 'topic', 'userid': 'userid'}, doc3)

    def test_from_document(self):
        data1 = {'_id': 666, 'groupid': 'groupid', 'pattern': 'pattern', 'template': 'template', 'that': 'that', 'topic': 'topic', 'userid': 'userid'}
        category1 = Category.from_document(data1)
        self.assertIsNotNone(category1)

        data2 = {'groupid': 'groupid', 'pattern': 'pattern', 'template': 'template', 'that': 'that', 'topic': 'topic', 'userid': 'userid'}
        category2 = Category.from_document(data2)
        self.assertIsNotNone(category2)
