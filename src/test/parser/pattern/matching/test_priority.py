
from test.parser.pattern.matching.base import PatternMatcherBaseClass

class PatternMatcherTests(PatternMatcherBaseClass):

    def test_priority_tree_matching_no_wildcards(self):

        self.add_pattern_to_graph(pattern="$A B D", topic="X", that="Y", template="1")
        self.add_pattern_to_graph(pattern="A B D", topic="X", that="Y", template="2")

        context = self.match_sentence("A B D", topic="X", that="Y")
        self.assertIsNotNone(context)
        self.assertIsNotNone(context.template_node())
        self.assertEqual("1", context.template_node().template.word)


