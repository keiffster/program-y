
import unittest

from programy.storage.stores.sql.dao.category import Category

class CategoryTests(unittest.TestCase):

    def test_init(self):

        category1 = Category(groupid='groupid', userid='userid', topic='topic', that='that', pattern='pattern', template='template')
        self.assertIsNotNone(category1)
        self.assertEqual("<Category(id='n/a', groupid='groupid', userid='userid', topic='topic', that='that', pattern='pattern', template='template'>", str(category1))

        category2 = Category(id=1, groupid='groupid', userid='userid', topic='topic', that='that', pattern='pattern', template='template')
        self.assertIsNotNone(category2)
        self.assertEqual("<Category(id='1', groupid='groupid', userid='userid', topic='topic', that='that', pattern='pattern', template='template'>", str(category2))
