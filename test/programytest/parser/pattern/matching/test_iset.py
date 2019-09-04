from programytest.parser.pattern.matching.base import PatternMatcherBaseClass


class PatternMatcherISetTests(PatternMatcherBaseClass):

    def test_basic_iset_match(self):

        self.add_pattern_to_graph(pattern="I AM A <iset>MAN, WOMAN</iset>", topic="*", that="*", template="1")

        context = self.match_sentence("I AM A MAN", topic="*", that="*")
        self.assertIsNotNone(context)
        self.assertIsNotNone(context.template_node)
        self.assertEqual("PTEMPLATE [*] [P(0)^(0)#(0)C(0)_(0)*(0)To(0)Th(0)Te(1)]",  context.template_node.to_string())

        context = self.match_sentence("I AM A WOMAN", topic="*", that="*")
        self.assertIsNotNone(context)
        self.assertIsNotNone(context.template_node)
        self.assertEqual("PTEMPLATE [*] [P(0)^(0)#(0)C(0)_(0)*(0)To(0)Th(0)Te(1)]",  context.template_node.to_string())

    def test_multiple_iset_match(self):

        self.add_pattern_to_graph(pattern="I LIKE TO <iset>PARTY, DRINK, SLEEP</iset> DURING THE DAY", topic="*", that="*", template="1")
        self.add_pattern_to_graph(pattern="I LIKE TO <iset>PARTY, DRINK, SLEEP</iset> DURING THE NIGHT", topic="*", that="*", template="2")

        context = self.match_sentence("I LIKE TO PARTY DURING THE DAY", topic="*", that="*")
        self.assertIsNotNone(context)
        self.assertIsNotNone(context.template_node)
        self.assertEqual("PTEMPLATE [*] [P(0)^(0)#(0)C(0)_(0)*(0)To(0)Th(0)Te(1)]",  context.template_node.to_string())

        context = self.match_sentence("I LIKE TO PARTY DURING THE NIGHT", topic="*", that="*")
        self.assertIsNotNone(context)
        self.assertIsNotNone(context.template_node)
        self.assertEqual("2", context.template_node.template.word)
