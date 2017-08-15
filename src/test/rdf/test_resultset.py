import unittest

from programy.rdf.resultset import RDFQueryResultSet
from programy.parser.template.nodes.word import TemplateWordNode


class RDFQueryResultSetTests(unittest.TestCase):

    def test_resultset(self):
        resultset = RDFQueryResultSet(TemplateWordNode("Subject"), TemplateWordNode("Predicate"), TemplateWordNode("Object"), [])
        self.assertIsNotNone(resultset)