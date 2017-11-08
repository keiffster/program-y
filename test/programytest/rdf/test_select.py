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

class RDFSelectTests(unittest.TestCase):

    def test_select_single_query_with_var(self):

        bot = TestBot()

        bot.brain.rdf.load_from_text("""
            MONKEY:legs:2
            MONKEY:fur:yes
            BEAR:legs:4
            BEAR:fur:yes
            BIRD:legs:2
            BIRD:feathers:yes
        """)

        select = RDFSelectStatement(["?x"], [
            RDFQuery(subject=TemplateWordNode("?x"), predicate=TemplateWordNode("LEGS"), obj=TemplateWordNode("2"))
        ])
        self.assertIsNotNone(select)

        result = select.execute(bot, "testid")
        self.assertIsNotNone(result)
        self.assertTrue([['?x', 'MONKEY']] in result)
        self.assertTrue([['?x', 'BIRD']] in result)

    def test_select_single_not_query_without_var(self):
        bot = TestBot()

        bot.brain.rdf.load_from_text("""
            MONKEY:legs:2
            MONKEY:fur:yes
            BEAR:legs:4
            BEAR:fur:yes
            BIRD:legs:2
            BIRD:feathers:yes
        """)

        select = RDFSelectStatement([], [
            RDFQuery(subject=TemplateWordNode("?x"), predicate=TemplateWordNode("LEGS"), obj=TemplateWordNode("2"), query_type=RDFQuery.NOT_QUERY)
        ])
        self.assertIsNotNone(select)

        result = select.execute(bot, "testid")
        self.assertIsNotNone(result)
        print(result)
        self.assertTrue([['?x', 'BEAR'],[None, 'LEGS'], [None, '4']] in result)
        self.assertTrue([['?x', 'BEAR'],[None, 'FUR'], [None, 'yes']] in result)

    def test_select_single_not_query_with_var(self):
        bot = TestBot()

        bot.brain.rdf.load_from_text("""
            MONKEY:legs:2
            MONKEY:fur:yes
            BEAR:legs:4
            BEAR:fur:yes
            BIRD:legs:2
            BIRD:feathers:yes
        """)

        select = RDFSelectStatement(["?x"], [
            RDFQuery(subject=TemplateWordNode("?x"), predicate=TemplateWordNode("LEGS"), obj=TemplateWordNode("2"), query_type=RDFQuery.NOT_QUERY)
        ])
        self.assertIsNotNone(select)

        result = select.execute(bot, "testid")
        self.assertIsNotNone(result)
        print(result)
        self.assertTrue([['?x', 'BEAR']] in result)
        self.assertTrue([['?x', 'BIRD']] in result)

    def test_select_multi_query(self):
        bot = TestBot()

        bot.brain.rdf.load_from_text("""
            MONKEY:legs:2
            MONKEY:fur:yes
            BEAR:legs:4
            BEAR:fur:yes
            BIRD:legs:2
            BIRD:feathers:yes
        """)

        select = RDFSelectStatement(["?x"], [
            RDFQuery(subject=TemplateWordNode("?x"), predicate=TemplateWordNode("LEGS"), obj=TemplateWordNode("2")),
            RDFQuery(subject=TemplateWordNode("?x"), predicate=TemplateWordNode("FEATHERS"), obj=TemplateWordNode("yes"))
        ])
        self.assertIsNotNone(select)

        result = select.execute(bot, "testid")
        self.assertIsNotNone(result)

        self.assertEquals(1, len(result))
        self.assertEquals(1, len(result[0]))
        self.assertTrue(['?x', 'BIRD'] in result[0])

    def test_select_multi_step_query(self):
        bot = TestBot()

        bot.brain.rdf.load_from_text("""
            TEST1:hasPurpose:to test
            TEST1:hasSize:9
            TEST1:isA:TEST2
            TEST2:hasPurpose:to test
            TEST2:hasSize:9
            TEST2:isA:TEST3
            TEST3:hasPurpose:to test
            TEST3:hasSize:1
            TEST3:isA:TEST4
            TEST4:hasPurpose:to test
        """)

        select = RDFSelectStatement(["?x", "?y", "?z", "?w"], [
            RDFQuery(subject=TemplateWordNode("?x"), predicate=TemplateWordNode("ISA"), obj=TemplateWordNode("?y")),
            RDFQuery(subject=TemplateWordNode("?y"), predicate=TemplateWordNode("ISA"), obj=TemplateWordNode("?z")),
            RDFQuery(subject=TemplateWordNode("?z"), predicate=TemplateWordNode("ISA"), obj=TemplateWordNode("?w"))
        ])
        self.assertIsNotNone(select)

        results = select.execute(bot, "testid")
        self.assertIsNotNone(results)

        self.assertEquals(1, len(results))
        self.assertEquals(4, len(results[0]))

        self.assertTrue(['?x', 'TEST1'] in results[0])
        self.assertTrue(['?y', 'TEST2'] in results[0])
        self.assertTrue(['?z', 'TEST3'] in results[0])
        self.assertTrue(['?w', 'TEST4'] in results[0])
