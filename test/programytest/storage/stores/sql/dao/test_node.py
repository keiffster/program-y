
import unittest

from programy.storage.stores.sql.dao.node import PatternNode
from programy.storage.stores.sql.dao.node import TemplateNode

class PatternNodeTests(unittest.TestCase):
    
    def test_init(self):
        node1 = PatternNode(name='name', node_class='class')
        self.assertIsNotNone(node1)
        self.assertEqual("<Pattern Node(id='n/a', name='name', node_class='class')>", str(node1))
        
        node2 = PatternNode(id=1, name='name', node_class='class')
        self.assertIsNotNone(node2)
        self.assertEqual("<Pattern Node(id='1', name='name', node_class='class')>", str(node2))


class TemplateNodeTests(unittest.TestCase):

    def test_init(self):
        node1 = TemplateNode(name='name', node_class='class')
        self.assertIsNotNone(node1)
        self.assertEqual("<Template Node(id='n/a', name='name', node_class='class')>", str(node1))

        node2 = TemplateNode(id=1, name='name', node_class='class')
        self.assertIsNotNone(node2)
        self.assertEqual("<Template Node(id='1', name='name', node_class='class')>", str(node2))
