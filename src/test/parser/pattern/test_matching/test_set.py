
from test.parser.pattern.test_matching.base import PatternMatcherBaseClass

class PatternMatcherSetTests(PatternMatcherBaseClass):

    def test_basic_set_match(self):

        self.add_pattern_to_graph(pattern="I AM <set>number</set> YEARS OLD", topic="X", that="Y", template="1")

        self.dump_graph()

        context = self.match_sentence("I AM 49 YEARS OLD", topic="X", that="Y")
        self.assertIsNotNone(context)
        self.assertIsNotNone(context.template_node())
        self.assertEqual("1", context.template_node().template.word)

        self.assertEqual("49", context.star(1))
