import re

from programytest.parser.pattern.matching.base import PatternMatcherBaseClass


class PatternMatcherRegexTests(PatternMatcherBaseClass):

    def test_basic_regex_match_as_text(self):

        self.add_pattern_to_graph(pattern="I AM <regex>^LEGION$</regex>", topic="*", that="*", template="1")

        context = self.match_sentence("I AM LEGION", topic="*", that="*")
        self.assertIsNotNone(context)
        self.assertIsNotNone(context.template_node)
        self.assertEqual("PTEMPLATE [*] [P(0)^(0)#(0)C(0)_(0)*(0)To(0)Th(0)Te(1)]",  context.template_node.to_string())
        self.assertEqual("LEGION", context.star(self._client_context, 1))

        context = self.match_sentence("I AM LEGIONAIRRE", topic="*", that="*")
        self.assertIsNone(context)

    def test_basic_regex_match_as_pattern(self):

        self.add_pattern_to_graph(pattern='I AM <regex pattern="^LEGION$" />', topic="*", that="*", template="1")

        context = self.match_sentence("I AM LEGION", topic="*", that="*")
        self.assertIsNotNone(context)
        self.assertIsNotNone(context.template_node)
        self.assertEqual("PTEMPLATE [*] [P(0)^(0)#(0)C(0)_(0)*(0)To(0)Th(0)Te(1)]",  context.template_node.to_string())
        self.assertEqual("LEGION", context.star(self._client_context, 1))

        context = self.match_sentence("I AM LEGIONAIRRE", topic="*", that="*")
        self.assertIsNone(context)

    def test_basic_regex_match_as_template(self):

        self._client_context.brain.regex_templates.add_regex("LEGION", re.compile("^LEGION$", re.IGNORECASE))

        self.add_pattern_to_graph(pattern='I AM <regex template="LEGION" />', topic="*", that="*", template="1")

        context = self.match_sentence("I AM LEGION", topic="*", that="*")
        self.assertIsNotNone(context)
        self.assertIsNotNone(context.template_node)
        self.assertEqual("PTEMPLATE [*] [P(0)^(0)#(0)C(0)_(0)*(0)To(0)Th(0)Te(1)]",  context.template_node.to_string())
        self.assertEqual("LEGION", context.star(self._client_context, 1))

        context = self.match_sentence("I AM LEGIONAIRRE", topic="*", that="*")
        self.assertIsNone(context)

    def test_part_word_regex_match_as_template(self):

        self._client_context.brain.regex_templates.add_regex("LEGION", re.compile("LEGION*", re.IGNORECASE))

        self.add_pattern_to_graph(pattern='I AM <regex template="LEGION" />', topic="*", that="*", template="1")

        context = self.match_sentence("I AM LEGION", topic="*", that="*")
        self.assertIsNotNone(context)
        self.assertIsNotNone(context.template_node)
        self.assertEqual("PTEMPLATE [*] [P(0)^(0)#(0)C(0)_(0)*(0)To(0)Th(0)Te(1)]",  context.template_node.to_string())
        self.assertEqual("LEGION", context.star(self._client_context, 1))

        context = self.match_sentence("I AM LEGIONAIRRE", topic="*", that="*")
        self.assertIsNotNone(context)
        self.assertIsNotNone(context.template_node)
        self.assertEqual("PTEMPLATE [*] [P(0)^(0)#(0)C(0)_(0)*(0)To(0)Th(0)Te(1)]",  context.template_node.to_string())
        self.assertEqual("LEGIONAIRRE", context.star(self._client_context, 1))

    def test_regex_loaded_from_file(self):

        self._client_context.brain.regex_templates.add_regex("ANYINTEGER", re.compile('^\\d+$', re.IGNORECASE))

        self.add_pattern_to_graph(pattern='I AM <regex template="ANYINTEGER" /> YEARS OLD', topic="*", that="*", template="CORRECT")

        context = self.match_sentence("I AM 27 YEARS OLD", topic="*", that="*")
        self.assertIsNotNone(context)
        self.assertIsNotNone(context.template_node)
        self.assertEqual("CORRECT", context.template_node.template.word)
        self.assertEqual("27", context.star(self._client_context, 1))
