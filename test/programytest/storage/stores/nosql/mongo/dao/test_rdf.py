import unittest

from programy.storage.stores.nosql.mongo.dao.rdf import RDF


class RDFTests(unittest.TestCase):

    def test_init_no_id(self):
        rdf = RDF(name="TEST", subject="subj", predicate="pred", object="obj")

        self.assertIsNotNone(rdf)
        self.assertIsNone(rdf.id)
        self.assertEqual("TEST", rdf.name)
        self.assertEqual("subj", rdf.subject)
        self.assertEqual("pred", rdf.predicate)
        self.assertEqual("obj", rdf.object)
        self.assertEqual({'name': 'TEST', 'object': 'obj', 'predicate': 'pred', 'subject': 'subj'}, rdf.to_document())

    def test_init_with_id(self):
        rdf = RDF(name="TEST", subject="subj", predicate="pred", object="obj")
        rdf.id = '666'

        self.assertIsNotNone(rdf)
        self.assertIsNotNone(rdf.id)
        self.assertEqual('666', rdf.id)
        self.assertEqual("TEST", rdf.name)
        self.assertEqual("subj", rdf.subject)
        self.assertEqual("pred", rdf.predicate)
        self.assertEqual("obj", rdf.object)
        self.assertEqual({'_id': '666', 'name': 'TEST', 'object': 'obj', 'predicate': 'pred', 'subject': 'subj'}, rdf.to_document())

    def test_from_document(self):
        rdf1 = RDF.from_document({'name': 'TEST', 'object': 'obj', 'predicate': 'pred', 'subject': 'subj'})
        self.assertIsNotNone(rdf1)
        self.assertIsNone(rdf1.id)
        self.assertEqual("TEST", rdf1.name)
        self.assertEqual("subj", rdf1.subject)
        self.assertEqual("pred", rdf1.predicate)
        self.assertEqual("obj", rdf1.object)

        rdf2 = RDF.from_document({'_id': '666', 'name': 'TEST', 'object': 'obj', 'predicate': 'pred', 'subject': 'subj'})
        self.assertIsNotNone(rdf2)
        self.assertIsNotNone(rdf2.id)
        self.assertEqual('666', rdf2.id)
        self.assertEqual("TEST", rdf2.name)
        self.assertEqual("subj", rdf2.subject)
        self.assertEqual("pred", rdf2.predicate)
        self.assertEqual("obj", rdf2.object)
