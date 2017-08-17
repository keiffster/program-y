import unittest

from programy.rdf.query import RDFQuery

from programy.rdf.collection import RDFCollection
from programy.parser.template.nodes.word import TemplateWordNode

class TestBrain:

    def __init__(self):
        self.rdf = RDFCollection()

class TestBot:

    def __init__(self):
        self.brain = TestBrain()

class RDFQueryTests(unittest.TestCase):

    def test_query(self):
        query = RDFQuery(subject=TemplateWordNode("Subject"), predicate=TemplateWordNode("Predicate"), object=TemplateWordNode("Object"))
        self.assertIsNotNone(query)
        self.assertEquals(query.query_type, RDFQuery.QUERY)
        self.assertEquals("<q><subj>Subject</subj><pred>Predicate</pred><obj>Object</obj></q>", query.to_xml(None, None))

    def test_not_query(self):
        query = RDFQuery(subject=TemplateWordNode("Subject"), predicate=TemplateWordNode("Predicate"), object=TemplateWordNode("Object"), query_type=RDFQuery.NOT_QUERY)
        self.assertIsNotNone(query)
        self.assertEquals(query.query_type, RDFQuery.NOT_QUERY)
        self.assertEquals("<notq><subj>Subject</subj><pred>Predicate</pred><obj>Object</obj></notq>", query.to_xml(None, None))

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
        resultset = query.execute(bot, "testid")
        self.assertIsNotNone(resultset)
        result = resultset.results[0]
        self.assertIsNotNone(result)
        self.assertEquals(result[0][1], "ACCOUNT")
        self.assertEquals(result[1][1], "hasSize")
        self.assertEquals(result[2][1], "0")

    def test_execute_multi_vars(self):
        bot = TestBot()
        bot.brain.rdf.load_from_text("""
            ACCOUNT:hasPurpose:to track money
            ACCOUNT:hasSize:0
            ACCOUNT:hasSyllables:2
            ACCOUNT:isa:Concept
            ACCOUNT:lifeArea:Finances
            ACT:hasPurpose:to entertain by performing
        """)
        query = RDFQuery(subject=TemplateWordNode("ACCOUNT"), predicate=TemplateWordNode("?x"), object=TemplateWordNode("?y"))
        resultset = query.execute(bot, "testid")
        self.assertIsNotNone(resultset)
        self.assertEquals(5, len(resultset.results))
