
from programytest.parser.pattern.matching.base import PatternMatcherBaseClass

class PatternMatcherTests(PatternMatcherBaseClass):

    def test_hash_tree_matching_empty(self):

        self.add_pattern_to_graph(pattern="#", topic="X", that="Y", template="1")

        context = self.match_sentence("A", topic="X", that="Y")
        self.assertIsNotNone(context)
        self.assertIsNotNone(context.template_node())
        self.assertEqual("1", context.template_node().template.word)

        self.assertEqual("A", context.star(1))

    def test_hash_tree_matching_single(self):

        self.add_pattern_to_graph(pattern="# A", topic="X", that="Y", template="1")

        context = self.match_sentence("B A", topic="X", that="Y")
        self.assertIsNotNone(context)
        self.assertIsNotNone(context.template_node())
        self.assertEqual("1", context.template_node().template.word)

        self.assertEqual("B", context.star(1))

        context = self.match_sentence("A", topic="X", that="Y")
        self.assertIsNotNone(context)
        self.assertIsNotNone(context.template_node())
        self.assertEqual("1", context.template_node().template.word)

        self.assertEqual("", context.star(1))

    def test_hash_tree_matching_front(self):

        self.add_pattern_to_graph(pattern="# C D", topic="X", that="Y", template="1")

        context = self.match_sentence("A B C D", topic="X", that="Y")
        self.assertIsNotNone(context)
        self.assertIsNotNone(context.template_node())
        self.assertEqual("1", context.template_node().template.word)

        self.assertEqual("A B", context.star(1))

        context = self.match_sentence("C D", topic="X", that="Y")
        self.assertIsNotNone(context)
        self.assertIsNotNone(context.template_node())
        self.assertEqual("1", context.template_node().template.word)

        self.assertEqual("", context.star(1))

    def test_hash_tree_matching_middle(self):

        self.add_pattern_to_graph(pattern="A # D", topic="X", that="Y", template="1")

        context = self.match_sentence("A B C D", topic="X", that="Y")
        self.assertIsNotNone(context)
        self.assertIsNotNone(context.template_node())
        self.assertEqual("1", context.template_node().template.word)

        self.assertEqual("B C", context.star(1))

        context = self.match_sentence("A D", topic="X", that="Y")
        self.assertIsNotNone(context)
        self.assertIsNotNone(context.template_node())
        self.assertEqual("1", context.template_node().template.word)

        self.assertEqual("", context.star(1))

    def test_hash_tree_matching_end(self):

        self.add_pattern_to_graph(pattern="A B #", topic="X", that="Y", template="1")

        context = self.match_sentence("A B C D", topic="X", that="Y")
        self.assertIsNotNone(context)
        self.assertIsNotNone(context.template_node())
        self.assertEqual("1", context.template_node().template.word)

        self.assertEqual("C D", context.star(1))

        context = self.match_sentence("A B", topic="X", that="Y")
        self.assertIsNotNone(context)
        self.assertIsNotNone(context.template_node())
        self.assertEqual("1", context.template_node().template.word)

        self.assertEqual("", context.star(1))

    def test_hash_front_and_back(self):

        self.add_pattern_to_graph(pattern="# F G", topic="*", that="*", template="2")
        self.add_pattern_to_graph(pattern="# A B #", topic="*", that="*", template="1")

        context = self.match_sentence("F A B G", topic="X", that="Y")
        self.assertIsNotNone(context)
        self.assertIsNotNone(context.template_node())

        self.assertEqual("1", context.template_node().template.word)
        self.assertEqual("F", context.star(1))
        self.assertEqual("G", context.star(2))

    def test_hash_deep_tree_matching(self):

        self.add_pattern_to_graph(pattern="A # B # C", topic="X", that="Z", template="1")
        self.add_pattern_to_graph(pattern="A # B # C", topic="X", that="Y", template="1")

        context = self.match_sentence("A X1 X2 X3 X4 B Y1 Y2 Y3 Y4 C", topic="X", that="Y")

        self.assertIsNotNone(context)
        self.assertIsNotNone(context.template_node())
        self.assertEqual("1", context.template_node().template.word)

        self.assertEqual("X1 X2 X3 X4", context.star(1))
        self.assertEqual("Y1 Y2 Y3 Y4", context.star(2))
        
    def test_hash_at_start_and_end(self):

        self.add_pattern_to_graph(pattern="# A # B #", topic="*", that="*", template="1")

        context = self.match_sentence("A B")
        self.assertIsNotNone(context)
        self.assertIsNotNone(context.template_node())
        self.assertEqual("1", context.template_node().template.word)

        context = self.match_sentence("X A B")
        self.assertIsNotNone(context)
        self.assertIsNotNone(context.template_node())
        self.assertEqual("1", context.template_node().template.word)

        context = self.match_sentence("A X B")
        self.assertIsNotNone(context)
        self.assertIsNotNone(context.template_node())
        self.assertEqual("1", context.template_node().template.word)

        context = self.match_sentence("A B X")
        self.assertIsNotNone(context)
        self.assertIsNotNone(context.template_node())
        self.assertEqual("1", context.template_node().template.word)

        context = self.match_sentence("X A X B X")
        self.assertIsNotNone(context)
        self.assertIsNotNone(context.template_node())
        self.assertEqual("1", context.template_node().template.word)

    def test_multiple_hash_at_start_and_end(self):

        self.add_pattern_to_graph(pattern="# A # B ^", topic="*", that="*", template="1")
        self.add_pattern_to_graph(pattern="# A # B # C", topic="*", that="*", template="2")

        context = self.match_sentence("A B")
        self.assertIsNotNone(context)
        self.assertIsNotNone(context.template_node())
        self.assertEqual("1", context.template_node().template.word)

        context = self.match_sentence("X A B")
        self.assertIsNotNone(context)
        self.assertIsNotNone(context.template_node())
        self.assertEqual("1", context.template_node().template.word)

        context = self.match_sentence("A B C")
        self.assertIsNotNone(context)
        self.assertIsNotNone(context.template_node())
        self.assertEqual("2", context.template_node().template.word)

        context = self.match_sentence("X A B C")
        self.assertIsNotNone(context)
        self.assertIsNotNone(context.template_node())
        self.assertEqual("2", context.template_node().template.word)
