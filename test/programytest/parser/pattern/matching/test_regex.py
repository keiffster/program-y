import re

from programytest.parser.pattern.matching.base import PatternMatcherBaseClass

class PatternMatcherRegexTests(PatternMatcherBaseClass):

    def test_basic_regex_match_as_text(self):

        self.add_pattern_to_graph(pattern="I AM <regex>^LEGION$</regex>", topic="*", that="*", template="1")

        context = self.match_sentence("I AM LEGION", topic="*", that="*")
        self.assertIsNotNone(context)
        self.assertIsNotNone(context.template_node())
        self.assertEqual("1", context.template_node().template.word)
        self.assertEqual("LEGION", context.star(1))

        context = self.match_sentence("I AM LEGIONAIRRE", topic="*", that="*")
        self.assertIsNone(context)

    def test_basic_regex_match_as_pattern(self):

        self.add_pattern_to_graph(pattern='I AM <regex pattern="^LEGION$" />', topic="*", that="*", template="1")

        context = self.match_sentence("I AM LEGION", topic="*", that="*")
        self.assertIsNotNone(context)
        self.assertIsNotNone(context.template_node())
        self.assertEqual("1", context.template_node().template.word)
        self.assertEqual("LEGION", context.star(1))

        context = self.match_sentence("I AM LEGIONAIRRE", topic="*", that="*")
        self.assertIsNone(context)

    def test_basic_regex_match_as_template(self):

        self._client_context.brain._regex_templates['LEGION']= re.compile("^LEGION$")

        self.add_pattern_to_graph(pattern='I AM <regex template="LEGION" />', topic="*", that="*", template="1")

        context = self.match_sentence("I AM LEGION", topic="*", that="*")
        self.assertIsNotNone(context)
        self.assertIsNotNone(context.template_node())
        self.assertEqual("1", context.template_node().template.word)
        self.assertEqual("LEGION", context.star(1))

        context = self.match_sentence("I AM LEGIONAIRRE", topic="*", that="*")
        self.assertIsNone(context)
