from programytest.parser.pattern.matching.base import PatternMatcherBaseClass


class PatternMatcherBotTests(PatternMatcherBaseClass):

    def test_basic_bot_match_as_text(self):

        self._client_context.brain.properties.add_property('firstname', 'testbot')

        self.add_pattern_to_graph(pattern="<bot>firstname</bot>", topic="X", that="Y", template="1")

        context = self.match_sentence("testbot", topic="X", that="Y")
        self.assertIsNotNone(context)
        self.assertIsNotNone(context.template_node)
        self.assertEqual("PTEMPLATE [*] [P(0)^(0)#(0)C(0)_(0)*(0)To(0)Th(0)Te(1)]",  context.template_node.to_string())

        self.assertEqual("testbot", context.star(self._client_context, 1))

    def test_basic_bot_match_as_name(self):

        self._client_context.brain.properties.add_property('firstname', 'testbot')

        self.add_pattern_to_graph(pattern='<bot name="firstname" />', topic="X", that="Y", template="1")

        context = self.match_sentence("testbot", topic="X", that="Y")
        self.assertIsNotNone(context)
        self.assertIsNotNone(context.template_node)
        self.assertEqual("PTEMPLATE [*] [P(0)^(0)#(0)C(0)_(0)*(0)To(0)Th(0)Te(1)]",  context.template_node.to_string())

        self.assertEqual("testbot", context.star(self._client_context, 1))

    def test_basic_bot_match_as_property(self):

        self._client_context.brain.properties.add_property('firstname', 'testbot')

        self.add_pattern_to_graph(pattern='<bot property="firstname" />', topic="X", that="Y", template="1")

        context = self.match_sentence("testbot", topic="X", that="Y")
        self.assertIsNotNone(context)
        self.assertIsNotNone(context.template_node)
        self.assertEqual("PTEMPLATE [*] [P(0)^(0)#(0)C(0)_(0)*(0)To(0)Th(0)Te(1)]",  context.template_node.to_string())

        self.assertEqual("testbot", context.star(self._client_context, 1))
