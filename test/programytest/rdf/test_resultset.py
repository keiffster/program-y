import unittest

from programy.rdf.resultset import RDFQueryResultSet
from programy.rdf.entity import RDFEntity


class RDFQueryResultSetTests(unittest.TestCase):

    def test_resultset_empty_results(self):
        resultset = RDFQueryResultSet("Subject", "Predicate", "Object", [])
        self.assertIsNotNone(resultset)
        self.assertIsNotNone(resultset.subject)
        self.assertIsNotNone(resultset.predicate)
        self.assertIsNotNone(resultset.object)
        self.assertEquals([], resultset.results)
        self.assertEquals("", resultset.to_string())

    def test_resultset_with_result(self):

        results = [RDFEntity(subject="Subject1", predicate="Predicate1", object="Object1")]

        resultset = RDFQueryResultSet("Subject", "Predicate", "Object", results)
        self.assertIsNotNone(resultset)
        self.assertIsNotNone(resultset.subject)
        self.assertIsNotNone(resultset.predicate)
        self.assertIsNotNone(resultset.object)
        self.assertEquals(results, resultset.results)
        self.assertEquals("( _=Subject1, _=Predicate1, _=Object1 )\n", resultset.to_string())

        self.assertEquals("Subject1", resultset.get_variable_value("Subject", results[0]))
        self.assertEquals("Predicate1", resultset.get_variable_value("Predicate", results[0]))
        self.assertEquals("Object1", resultset.get_variable_value("Object", results[0]))

    def test_resultset_with_result2(self):

        results = [RDFEntity(subject="Subject1", predicate="Predicate1", object="Object1"),
                   RDFEntity(subject="Subject2", predicate="Predicate2", object="Object2")]

        resultset = RDFQueryResultSet("Subject", "Predicate", "Object", results)
        self.assertIsNotNone(resultset)
        self.assertIsNotNone(resultset)
        self.assertIsNotNone(resultset.subject)
        self.assertIsNotNone(resultset.predicate)
        self.assertIsNotNone(resultset.object)
        self.assertEquals(results, resultset.results)
        self.assertEquals("( _=Subject1, _=Predicate1, _=Object1 )\n( _=Subject2, _=Predicate2, _=Object2 )\n", resultset.to_string())

        self.assertEquals("Subject1", resultset.get_variable_value("Subject", results[0]))
        self.assertEquals("Predicate1", resultset.get_variable_value("Predicate", results[0]))
        self.assertEquals("Object1", resultset.get_variable_value("Object", results[0]))

        self.assertEquals("Subject2", resultset.get_variable_value("Subject", results[1]))
        self.assertEquals("Predicate2", resultset.get_variable_value("Predicate", results[1]))
        self.assertEquals("Object2", resultset.get_variable_value("Object", results[1]))
