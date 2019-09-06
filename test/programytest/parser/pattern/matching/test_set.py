from programytest.parser.pattern.matching.base import PatternMatcherBaseClass


class PatternMatcherSetTests(PatternMatcherBaseClass):

    def test_basic_set_match_as_text(self):

        if self._client_context.brain.sets.contains("SEX") is False:
            self._client_context.brain._sets_collection.add_set("SEX",
                                                                {"MAN": [["MAN"]], "WOMAN": [["WOMAN"]]},
                                                                "teststore")

        self.add_pattern_to_graph(pattern="I AM A <set>sex</set>", topic="X", that="Y", template="1")

        context = self.match_sentence("I AM A MAN", topic="X", that="Y")
        self.assertIsNotNone(context)
        self.assertIsNotNone(context.template_node)
        self.assertEqual("PTEMPLATE [*] [P(0)^(0)#(0)C(0)_(0)*(0)To(0)Th(0)Te(1)]",  context.template_node.to_string())
        self.assertEqual("MAN", context.star(self._client_context, 1))

        context = self.match_sentence("I AM A WOMAN", topic="X", that="Y")
        self.assertIsNotNone(context)
        self.assertIsNotNone(context.template_node)
        self.assertEqual("PTEMPLATE [*] [P(0)^(0)#(0)C(0)_(0)*(0)To(0)Th(0)Te(1)]",  context.template_node.to_string())
        self.assertEqual("WOMAN", context.star(self._client_context, 1))

    def test_basic_set_match_as_name(self):

        if self._client_context.brain.sets.contains("SEX") is False:
            self._client_context.brain._sets_collection.add_set("SEX",
                                                                {"MAN": [["MAN"]], "WOMAN": [["WOMAN"]]},
                                                                "teststore")

        self.add_pattern_to_graph(pattern='I AM A <set name="sex" />', topic="X", that="Y", template="1")

        context = self.match_sentence("I AM A MAN", topic="X", that="Y")
        self.assertIsNotNone(context)
        self.assertIsNotNone(context.template_node)
        self.assertEqual("PTEMPLATE [*] [P(0)^(0)#(0)C(0)_(0)*(0)To(0)Th(0)Te(1)]",  context.template_node.to_string())
        self.assertEqual("MAN", context.star(self._client_context, 1))

        context = self.match_sentence("I AM A WOMAN", topic="X", that="Y")
        self.assertIsNotNone(context)
        self.assertIsNotNone(context.template_node)
        self.assertEqual("PTEMPLATE [*] [P(0)^(0)#(0)C(0)_(0)*(0)To(0)Th(0)Te(1)]",  context.template_node.to_string())
        self.assertEqual("WOMAN", context.star(self._client_context, 1))

    def test_multi_word_set_match(self):

        self._client_context.brain._sets_collection.add_set("COLOR", {"RED": [["RED"],
                                                                              ["RED", "AMBER"],
                                                                              ["RED", "BURNT", "OAK"],
                                                                              ["RED", "ORANGE"]
                                                                              ]}, "teststore")

        self.add_pattern_to_graph(pattern="I LIKE <set>color</set> *", topic="*", that="*", template="1")

        context = self.match_sentence("I LIKE RED PAINT", topic="*", that="*")
        self.assertIsNotNone(context)
        self.assertIsNotNone(context.template_node)
        self.assertEqual("PTEMPLATE [*] [P(0)^(0)#(0)C(0)_(0)*(0)To(0)Th(0)Te(1)]",  context.template_node.to_string())
        self.assertEqual("RED", context.star(self._client_context, 1))
        self.assertEqual("PAINT", context.star(self._client_context, 2))

        context = self.match_sentence("I LIKE RED AMBER CARS", topic="*", that="*")
        self.assertIsNotNone(context)
        self.assertIsNotNone(context.template_node)
        self.assertEqual("PTEMPLATE [*] [P(0)^(0)#(0)C(0)_(0)*(0)To(0)Th(0)Te(1)]",  context.template_node.to_string())
        self.assertEqual("RED AMBER", context.star(self._client_context, 1))
        self.assertEqual("CARS", context.star(self._client_context, 2))

        context = self.match_sentence("I LIKE RED BURNT OAK MOTOR BIKES", topic="*", that="*")
        self.assertIsNotNone(context)
        self.assertIsNotNone(context.template_node)
        self.assertEqual("PTEMPLATE [*] [P(0)^(0)#(0)C(0)_(0)*(0)To(0)Th(0)Te(1)]",  context.template_node.to_string())
        self.assertEqual("RED BURNT OAK", context.star(self._client_context, 1))
        self.assertEqual("MOTOR BIKES", context.star(self._client_context, 2))

    def test_basic_set_number_match(self):
        self._client_context.brain.dynamics.add_dynamic_set('number', "programy.dynamic.sets.numeric.IsNumeric", None)

        self.add_pattern_to_graph(pattern="I AM <set>number</set> YEARS OLD", topic="X", that="Y", template="1")

        context = self.match_sentence("I AM 49 YEARS OLD", topic="X", that="Y")
        self.assertIsNotNone(context)
        self.assertIsNotNone(context.template_node)
        self.assertEqual("PTEMPLATE [*] [P(0)^(0)#(0)C(0)_(0)*(0)To(0)Th(0)Te(1)]",  context.template_node.to_string())

        self.assertEqual("49", context.star(self._client_context, 1))

    def test_basic_set_synset_match(self):
        self._client_context.brain.dynamics.add_dynamic_set('synset', "programy.dynamic.sets.synsets.IsSynset", None)

        self.add_pattern_to_graph(pattern='I AM A <set name="synset" similar="hack" />', topic="*", that="*", template="OK")

        context = self.match_sentence("I AM A CHOP", topic="X", that="Y")
        self.assertIsNotNone(context)
        self.assertIsNotNone(context.template_node)

        context = self.match_sentence("I AM A FISH", topic="X", that="Y")
        self.assertIsNone(context)
