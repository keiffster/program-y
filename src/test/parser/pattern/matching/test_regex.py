
from test.parser.pattern.matching.base import PatternMatcherBaseClass

class PatternMatcherRegexTests(PatternMatcherBaseClass):

    def test_basic_regex_match(self):

        self.add_pattern_to_graph(pattern="I AM <regex>^LEGION$</regex>", topic="*", that="*", template="1")

        context = self.match_sentence("I AM LEGION", topic="*", that="*")
        self.assertIsNotNone(context)
        self.assertIsNotNone(context.template_node())
        self.assertEqual("1", context.template_node().template.word)
        self.assertEqual("LEGION", context.star(1))

        context = self.match_sentence("I AM LEGIONAIRRE", topic="*", that="*")
        self.assertIsNone(context)

