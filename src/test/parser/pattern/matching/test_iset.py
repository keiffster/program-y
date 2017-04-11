
from test.parser.pattern.matching.base import PatternMatcherBaseClass

class PatternMatcherISetTests(PatternMatcherBaseClass):

    def test_basic_iset_match(self):

        self.add_pattern_to_graph(pattern="I AM A <iset>MAN, WOMAN</iset>", topic="*", that="*", template="1")

        context = self.match_sentence("I AM A MAN", topic="*", that="*")
        self.assertIsNotNone(context)
        self.assertIsNotNone(context.template_node())
        self.assertEqual("1", context.template_node().template.word)

        context = self.match_sentence("I AM A WOMAN", topic="*", that="*")
        self.assertIsNotNone(context)
        self.assertIsNotNone(context.template_node())
        self.assertEqual("1", context.template_node().template.word)
