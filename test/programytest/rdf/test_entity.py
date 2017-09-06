import unittest

from programy.rdf.entity import RDFEntity
from programy.rdf.resultset import RDFQueryResultSet
from programy.parser.template.nodes.word import TemplateWordNode

class RDFEntityTests(unittest.TestCase):

    def test_entity_defaults(self):
        entity = RDFEntity()
        self.assertIsNotNone(entity)
        self.assertIsNone(entity.subject)
        self.assertIsNone(entity.predicate)
        self.assertIsNone(entity.object)

        resultset = RDFQueryResultSet("Subject", "Predicate", "Object", [])
        self.assertEquals("(  )", entity.to_string(resultset))
        self.assertEquals("<subj></subj><pred></pred><obj></obj>", entity.to_xml(None, None))

    def test_entity_no_variables(self):
        entity = RDFEntity(subject="Subject", predicate="Predicate", object="Object")
        self.assertIsNotNone(entity)
        self.assertIsNotNone(entity.subject)
        self.assertEquals("Subject", entity.subject)
        self.assertIsNotNone(entity.predicate)
        self.assertEquals("Predicate", entity.predicate)
        self.assertIsNotNone(entity.object)
        self.assertEquals("Object", entity.object)

        resultset = RDFQueryResultSet("Subject", "Predicate", "Object", [])
        self.assertEquals("( _=Subject, _=Predicate, _=Object )", entity.to_string(resultset))
        self.assertEquals("<subj>Subject</subj><pred>Predicate</pred><obj>Object</obj>", entity.to_xml(None, None))

    def test_entity_variables(self):
        entity = RDFEntity(subject="Subject", predicate="Predicate", object="Object")
        self.assertIsNotNone(entity)
        self.assertIsNotNone(entity.subject)
        self.assertEquals("Subject", entity.subject)
        self.assertIsNotNone(entity.predicate)
        self.assertEquals("Predicate", entity.predicate)
        self.assertIsNotNone(entity.object)
        self.assertEquals("Object", entity.object)

        resultset = RDFQueryResultSet("?x", "?y", "?z", [])
        self.assertEquals("( ?x=Subject, ?y=Predicate, ?z=Object )", entity.to_string(resultset))
        self.assertEquals("<subj>Subject</subj><pred>Predicate</pred><obj>Object</obj>", entity.to_xml(None, None))
