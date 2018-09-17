
import unittest

from programy.storage.stores.sql.dao.processor import PreProcessor
from programy.storage.stores.sql.dao.processor import PostProcessor


class PreProcessorTests(unittest.TestCase):
    
    def test_init(self):
        processor1 = PreProcessor(classname='class')
        self.assertIsNotNone(processor1)
        self.assertEqual("<PreProcessor Node(id='n/a', classname='class')>", str(processor1))
        
        processor2 = PreProcessor(id=1, classname='class')
        self.assertIsNotNone(processor2)
        self.assertEqual("<PreProcessor Node(id='1', classname='class')>", str(processor2))


class PostProcessorTests(unittest.TestCase):

    def test_init(self):
        processor1 = PostProcessor(classname='class')
        self.assertIsNotNone(processor1)
        self.assertEqual("<PostProcessor Node(id='n/a', classname='class')>", str(processor1))

        processor2 = PostProcessor(id=1, classname='class')
        self.assertIsNotNone(processor2)
        self.assertEqual("<PostProcessor Node(id='1', classname='class')>", str(processor2))
