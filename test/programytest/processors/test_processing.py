import unittest

from programy.processors.pre.toupper import ToUpperPreProcessor
from programy.processors.processing import ProcessorCollection


class ProcessorCollectionTests(unittest.TestCase):

    def test_processing(self):
        collection = ProcessorCollection()
        collection.add_processor(ToUpperPreProcessor())
        collection.add_processor(ToUpperPreProcessor())

        result = collection.process(None, "hello")
        self.assertIsNotNone(result)
        self.assertEquals("HELLO", result)

    def test_processing_no_processors(self):
        collection = ProcessorCollection()

        result = collection.process(None, "hello")
        self.assertIsNotNone(result)
        self.assertEquals("hello", result)