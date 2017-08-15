import unittest

from programy.rdf.entity import RDFEntity

class RDFEntityTests(unittest.TestCase):

    def test_entity_defaults(self):
        entity = RDFEntity()
        self.assertIsNotNone(entity)
        self.assertIsNone(entity.subject)
        self.assertIsNone(entity.predicate)
        self.assertIsNone(entity.object)

    def test_entity_no_defaults(self):
        entity = RDFEntity(subject="Subject", predicate="Predicate", object="Object")
        self.assertIsNotNone(entity)
        self.assertIsNotNone(entity.subject)
        self.assertEquals("Subject", entity.subject)
        self.assertIsNotNone(entity.predicate)
        self.assertEquals("Predicate", entity.predicate)
        self.assertIsNotNone(entity.object)
        self.assertEquals("Object", entity.object)

