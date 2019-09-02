from programytest.parser.pattern.matching.base import PatternMatcherBaseClass


class PatternMatcherTests(PatternMatcherBaseClass):

    def test_underline_tree_matching_single(self):

        self.add_pattern_to_graph(pattern="_", topic="X", that="Y", template="1")

        context = self.match_sentence("A B D", topic="X", that="Y")
        self.assertIsNotNone(context)
        self.assertIsNotNone(context.template_node.to_string())
        self.assertEqual("PTEMPLATE [*] [P(0)^(0)#(0)C(0)_(0)*(0)To(0)Th(0)Te(1)]", context.template_node.to_string())

    def test_underline_tree_matching_front(self):

        self.add_pattern_to_graph(pattern="_ C D", topic="X", that="Y", template="1")

        context = self.match_sentence("A B C D", topic="X", that="Y")
        self.assertIsNotNone(context)
        self.assertIsNotNone(context.template_node.to_string())
        self.assertEqual("PTEMPLATE [*] [P(0)^(0)#(0)C(0)_(0)*(0)To(0)Th(0)Te(1)]", context.template_node.to_string())

    def test_underline_tree_matching_middle(self):

        self.add_pattern_to_graph(pattern="A _ D", topic="X", that="Y", template="1")

        context = self.match_sentence("A B C D", topic="X", that="Y")
        self.assertIsNotNone(context)
        self.assertIsNotNone(context.template_node.to_string())
        self.assertEqual("PTEMPLATE [*] [P(0)^(0)#(0)C(0)_(0)*(0)To(0)Th(0)Te(1)]", context.template_node.to_string())

    def test_underline_tree_matching_end(self):

        self.add_pattern_to_graph(pattern="A B _", topic="X", that="Y", template="1")

        context = self.match_sentence("A B C D", topic="X", that="Y")
        self.assertIsNotNone(context)
        self.assertIsNotNone(context.template_node.to_string())
        self.assertEqual("PTEMPLATE [*] [P(0)^(0)#(0)C(0)_(0)*(0)To(0)Th(0)Te(1)]", context.template_node.to_string())

    def test_underline_tree_matching_multiple(self):

        self.add_pattern_to_graph(pattern="A _ _ D", topic="X", that="Y", template="1")

        context = self.match_sentence("A B C D", topic="X", that="Y")
        self.assertIsNotNone(context)
        self.assertIsNotNone(context.template_node.to_string())
        self.assertEqual("PTEMPLATE [*] [P(0)^(0)#(0)C(0)_(0)*(0)To(0)Th(0)Te(1)]", context.template_node.to_string())

    def test_underline_tree_matching_all(self):

        self.add_pattern_to_graph(pattern="A _ D", topic="_", that="_", template="1")

        context = self.match_sentence("A B C D", topic="X Y", that="Z")
        self.assertIsNotNone(context)
        self.assertIsNotNone(context.template_node.to_string())
        self.assertEqual("PTEMPLATE [*] [P(0)^(0)#(0)C(0)_(0)*(0)To(0)Th(0)Te(1)]", context.template_node.to_string())

    def test_underline_front_and_back(self):

        self.add_pattern_to_graph(pattern="_ F G", topic="*", that="*", template="2")
        self.add_pattern_to_graph(pattern="_ A B _", topic="*", that="*", template="1")

        context = self.match_sentence("F A B G", topic="X", that="Y")
        self.assertIsNotNone(context)
        self.assertIsNotNone(context.template_node.to_string())
        self.assertEqual("PTEMPLATE [*] [P(0)^(0)#(0)C(0)_(0)*(0)To(0)Th(0)Te(1)]", context.template_node.to_string())

    def test_underline_deep_tree_matching(self):

        self.add_pattern_to_graph(pattern="A _ B _ C", topic="X", that="Z", template="1")
        self.add_pattern_to_graph(pattern="A _ B _ C", topic="X", that="Y", template="1")

        context = self.match_sentence("A X1 X2 X3 X4 B Y1 Y2 Y3 Y4 C", topic="X", that="Y")
        self.assertIsNotNone(context)
        self.assertIsNotNone(context.template_node.to_string())
        self.assertEqual("PTEMPLATE [*] [P(0)^(0)#(0)C(0)_(0)*(0)To(0)Th(0)Te(1)]", context.template_node.to_string())

        self.assertEqual("X1 X2 X3 X4", context.star(self._client_context, 1))
        self.assertEqual("Y1 Y2 Y3 Y4", context.star(self._client_context, 2))
