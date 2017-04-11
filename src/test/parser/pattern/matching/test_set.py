
from test.parser.pattern.matching.base import PatternMatcherBaseClass

class PatternMatcherSetTests(PatternMatcherBaseClass):

    def test_basic_set_match(self):

        self.bot.brain.sets.add_set("SEX", ["MAN", "WOMAN"])

        self.add_pattern_to_graph(pattern="I AM A <set>sex</set>", topic="X", that="Y", template="1")

        context = self.match_sentence("I AM A MAN", topic="X", that="Y")
        self.assertIsNotNone(context)
        self.assertIsNotNone(context.template_node())
        self.assertEqual("1", context.template_node().template.word)
        self.assertEqual("MAN", context.star(1))

        context = self.match_sentence("I AM A WOMAN", topic="X", that="Y")
        self.assertIsNotNone(context)
        self.assertIsNotNone(context.template_node())
        self.assertEqual("1", context.template_node().template.word)
        self.assertEqual("WOMAN", context.star(1))

    def test_basic_set_number_match(self):

        self.add_pattern_to_graph(pattern="I AM <set>number</set> YEARS OLD", topic="X", that="Y", template="1")

        context = self.match_sentence("I AM 49 YEARS OLD", topic="X", that="Y")
        self.assertIsNotNone(context)
        self.assertIsNotNone(context.template_node())
        self.assertEqual("1", context.template_node().template.word)

        self.assertEqual("49", context.star(1))
