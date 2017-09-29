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

    def test_get_parameter_value(self):
        parameters = [["name1", "value1"], ["name2", "value2"]]
        self.assertEqual("value1", RDFQuery.get_parameter_value("name1", parameters))
        self.assertEqual("value2", RDFQuery.get_parameter_value("name2", parameters))
        self.assertIsNone(RDFQuery.get_parameter_value("name3", parameters))

    def test_query(self):
        query = RDFQuery(rdf_subject=TemplateWordNode("Subject"), rdf_predicate=TemplateWordNode("Predicate"), rdf_object=TemplateWordNode("Object"))
        self.assertIsNotNone(query)
        self.assertEquals(query.query_type, RDFQuery.QUERY)
        self.assertEquals("<q><subj>Subject</subj><pred>Predicate</pred><obj>Object</obj></q>", query.to_xml(None, None))
        self.assertEquals("query=( subj=Subject, pred=Predicate, obj=Object )", query.to_string(None, None))

    def test_not_query(self):
        query = RDFQuery(rdf_subject=TemplateWordNode("Subject"), rdf_predicate=TemplateWordNode("Predicate"), rdf_object=TemplateWordNode("Object"), query_type=RDFQuery.NOT_QUERY)
        self.assertIsNotNone(query)
        self.assertEquals(query.query_type, RDFQuery.NOT_QUERY)
        self.assertEquals("<notq><subj>Subject</subj><pred>Predicate</pred><obj>Object</obj></notq>", query.to_xml(None, None))
        self.assertEquals("not=( subj=Subject, pred=Predicate, obj=Object )", query.to_string(None, None))

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
        query = RDFQuery(rdf_subject=TemplateWordNode("ACCOUNT"), rdf_predicate=TemplateWordNode("hasSize"), rdf_object=TemplateWordNode("?x"))

        self.assertEquals("query=( subj=ACCOUNT, pred=hasSize, obj=?x )", query.to_string(None, None))

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
        query = RDFQuery(rdf_subject=TemplateWordNode("ACCOUNT"), rdf_predicate=TemplateWordNode("?x"), rdf_object=TemplateWordNode("?y"))

        self.assertEquals("query=( subj=ACCOUNT, pred=?x, obj=?y )", query.to_string(None, None))

        resultset = query.execute(bot, "testid")
        self.assertIsNotNone(resultset)
        self.assertEquals(5, len(resultset.results))
