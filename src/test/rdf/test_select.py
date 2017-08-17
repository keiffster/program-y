import unittest

from programy.rdf.select import RDFSelectStatement

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

    def load_data(self, rdf):
        rdf.load_from_text("""
            MONKEY:legs:2
            MONKEY:fur:yes
            BEAR:legs:4
            BEAR:fur:yes
            BIRD:legs:2
            BIRD:feathers:yes
        """)

    def test_select_single_query(self):
        bot = TestBot()
        self.load_data(bot.brain.rdf)

        select = RDFSelectStatement(["?x"], [
            RDFQuery(subject=TemplateWordNode("?x"), predicate=TemplateWordNode("legs"), object=TemplateWordNode("2"))
        ])
        self.assertIsNotNone(select)

        result = select.execute(bot, "testid")
        self.assertIsNotNone(result)
        self.assertEquals([['?x', 'MONKEY'], ['?x', 'BIRD']], result)

    def test_select_single_not_query(self):
        bot = TestBot()
        self.load_data(bot.brain.rdf)

        select = RDFSelectStatement(["?x"], [
            RDFQuery(subject=TemplateWordNode("?x"), predicate=TemplateWordNode("legs"), object=TemplateWordNode("2"), query_type=RDFQuery.NOT_QUERY)
        ])
        self.assertIsNotNone(select)

        result = select.execute(bot, "testid")
        self.assertIsNotNone(result)
        self.assertEquals([['?x', 'BEAR'], ['?x', 'BEAR']], result)

    def test_select_multi_query(self):
        bot = TestBot()
        self.load_data(bot.brain.rdf)

        select = RDFSelectStatement(["?x"], [
            RDFQuery(subject=TemplateWordNode("?x"), predicate=TemplateWordNode("legs"), object=TemplateWordNode("2")),
            RDFQuery(subject=TemplateWordNode("?x"), predicate=TemplateWordNode("feathers"), object=TemplateWordNode("yes"))
        ])
        self.assertIsNotNone(select)

        result = select.execute(bot, "testid")
        self.assertIsNotNone(result)
        self.assertEquals([['?x', 'BIRD']], result)


