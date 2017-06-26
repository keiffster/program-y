
from test.parser.pattern.matching.base import PatternMatcherBaseClass

from programy.mappings.sets import SetLoader

class PatternMatcherSetTests(PatternMatcherBaseClass):

    def test_basic_set_match(self):

        loader = SetLoader()

        self.bot.brain.sets.add_set("SEX", loader.load_from_text("""
        Man
        Woman
        """))

        self.add_pattern_to_graph(pattern="I AM A <set>sex</set>", topic="X", that="Y", template="1")

        context = self.match_sentence("I AM A MAN", topic="X", that="Y")
        self.assertIsNotNone(context)
        self.assertIsNotNone(context.template_node())
        self.assertEqual("1", context.template_node().template.word)
        self.assertEqual("Man", context.star(1))

        context = self.match_sentence("I AM A WOMAN", topic="X", that="Y")
        self.assertIsNotNone(context)
        self.assertIsNotNone(context.template_node())
        self.assertEqual("1", context.template_node().template.word)
        self.assertEqual("Woman", context.star(1))

    def test_basic_set_number_match(self):

        self.add_pattern_to_graph(pattern="I AM <set>number</set> YEARS OLD", topic="X", that="Y", template="1")

        context = self.match_sentence("I AM 49 YEARS OLD", topic="X", that="Y")
        self.assertIsNotNone(context)
        self.assertIsNotNone(context.template_node())
        self.assertEqual("1", context.template_node().template.word)

        self.assertEqual("49", context.star(1))
