import unittest

from programy.storage.stores.nosql.mongo.dao.processor import PreProcessor
from programy.storage.stores.nosql.mongo.dao.processor import PostProcessor
from programy.storage.stores.nosql.mongo.dao.processor import PostQuestionProcessor


class PreProcessorTests(unittest.TestCase):

    def test_init_no_id(self):
        processor = PreProcessor(classname="test.processorclass")

        self.assertIsNotNone(processor)
        self.assertIsNone(processor.id)
        self.assertEqual("test.processorclass", processor.classname)
        self.assertEqual({'classname': 'test.processorclass'}, processor.to_document())

    def test_init_with_id(self):
        processor = PreProcessor(classname="test.processorclass")
        processor.id = '666'

        self.assertIsNotNone(processor)
        self.assertIsNotNone(processor.id)
        self.assertEqual('666', processor.id)
        self.assertEqual("test.processorclass", processor.classname)
        self.assertEqual({'_id': '666', 'classname': 'test.processorclass'}, processor.to_document())

    def test_from_document(self):
        processor1 = PreProcessor.from_document({'classname': 'test.processorclass'})
        self.assertIsNotNone(processor1)
        self.assertIsNone(processor1.id)
        self.assertEqual("test.processorclass", processor1.classname)

        processor2 = PreProcessor.from_document({'_id': '666', 'classname': 'test.processorclass'})
        self.assertIsNotNone(processor2)
        self.assertIsNotNone(processor2.id)
        self.assertEqual('666', processor2.id)
        self.assertEqual("test.processorclass", processor2.classname)


class PostProcessorTests(unittest.TestCase):

    def test_init_no_id(self):
        processor = PostProcessor(classname="test.processorclass")

        self.assertIsNotNone(processor)
        self.assertIsNone(processor.id)
        self.assertEqual("test.processorclass", processor.classname)
        self.assertEqual({'classname': 'test.processorclass'}, processor.to_document())

    def test_init_with_id(self):
        processor = PostProcessor(classname="test.processorclass")
        processor.id = '666'

        self.assertIsNotNone(processor)
        self.assertIsNotNone(processor.id)
        self.assertEqual('666', processor.id)
        self.assertEqual("test.processorclass", processor.classname)
        self.assertEqual({'_id': '666', 'classname': 'test.processorclass'}, processor.to_document())

    def test_from_document(self):
        processor1 = PostProcessor.from_document({'classname': 'test.processorclass'})
        self.assertIsNotNone(processor1)
        self.assertIsNone(processor1.id)
        self.assertEqual("test.processorclass", processor1.classname)

        processor2 = PostProcessor.from_document({'_id': '666', 'classname': 'test.processorclass'})
        self.assertIsNotNone(processor2)
        self.assertIsNotNone(processor2.id)
        self.assertEqual('666', processor2.id)
        self.assertEqual("test.processorclass", processor2.classname)


class PostQuestionProcessorTests(unittest.TestCase):

    def test_init_no_id(self):
        processor = PostQuestionProcessor(classname="test.processorclass")

        self.assertIsNotNone(processor)
        self.assertIsNone(processor.id)
        self.assertEqual("test.processorclass", processor.classname)
        self.assertEqual({'classname': 'test.processorclass'}, processor.to_document())

    def test_init_with_id(self):
        processor = PostQuestionProcessor(classname="test.processorclass")
        processor.id = '666'

        self.assertIsNotNone(processor)
        self.assertIsNotNone(processor.id)
        self.assertEqual('666', processor.id)
        self.assertEqual("test.processorclass", processor.classname)
        self.assertEqual({'_id': '666', 'classname': 'test.processorclass'}, processor.to_document())

    def test_from_document(self):
        processor1 = PostQuestionProcessor.from_document({'classname': 'test.processorclass'})
        self.assertIsNotNone(processor1)
        self.assertIsNone(processor1.id)
        self.assertEqual("test.processorclass", processor1.classname)

        processor2 = PostQuestionProcessor.from_document({'_id': '666', 'classname': 'test.processorclass'})
        self.assertIsNotNone(processor2)
        self.assertIsNotNone(processor2.id)
        self.assertEqual('666', processor2.id)
        self.assertEqual("test.processorclass", processor2.classname)
