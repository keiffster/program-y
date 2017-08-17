import unittest

from programy.rdf.query import RDFQuery
from programy.rdf.unique import RDFUniqueStatement
from programy.rdf.collection import RDFCollection
from programy.parser.template.nodes.word import TemplateWordNode

class TestBrain:

    def __init__(self):
        self.rdf = RDFCollection()

class TestBot:

    def __init__(self):
        self.brain = TestBrain()


class RDFUniqueStatementTests(unittest.TestCase):

    def test_execute_single_var(self):
        bot = TestBot()
        bot.brain.rdf.load_from_text("""
            ACCOUNT:hasPurpose:to track money
            ACCOUNT:hasSize:0
            ACCOUNT:hasSyllables:2
            ACCOUNT:isa:Concept
            ACCOUNT:lifeArea:Finances
            ACT:hasPurpose:to entertain by performing
        """)

        query = RDFQuery(subject=TemplateWordNode("ACCOUNT"), predicate=TemplateWordNode("hasSize"), object=TemplateWordNode("?x"))

        uniq = RDFUniqueStatement(query)

        result = uniq.execute(bot, "testid")
        self.assertIsNotNone(result)
        self.assertEquals(result, [['0']])
