import unittest

from programy.storage.stores.sql.dao.rdf import RDF


class RDFTests(unittest.TestCase):

    def test_init(self):
        rdf1 = RDF(name='name', subject='subject', predicate='predicate', object='object')
        self.assertIsNotNone(rdf1)
        self.assertEqual("<RDF(id='n/a', name='name', subject='subject', predicate='predicate', object='object')>", str(rdf1))

        rdf2 = RDF(id=1, name='name', subject='subject', predicate='predicate', object='object')
        self.assertIsNotNone(rdf2)
        self.assertEqual("<RDF(id='1', name='name', subject='subject', predicate='predicate', object='object')>", str(rdf2))
