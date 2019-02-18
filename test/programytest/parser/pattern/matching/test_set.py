
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
        self.assertIsNotNone(context.template_node())
        self.assertEqual("1", context.template_node().template.word)
        self.assertEqual("MAN", context.star(1))

        context = self.match_sentence("I AM A WOMAN", topic="X", that="Y")
        self.assertIsNotNone(context)
        self.assertIsNotNone(context.template_node())
        self.assertEqual("1", context.template_node().template.word)
        self.assertEqual("WOMAN", context.star(1))

    def test_basic_set_match_as_name(self):

        if self._client_context.brain.sets.contains("SEX") is False:
            self._client_context.brain._sets_collection.add_set("SEX",
                                                                {"MAN": [["MAN"]], "WOMAN": [["WOMAN"]]},
                                                                "teststore")

        self.add_pattern_to_graph(pattern='I AM A <set name="sex" />', topic="X", that="Y", template="1")

        context = self.match_sentence("I AM A MAN", topic="X", that="Y")
        self.assertIsNotNone(context)
        self.assertIsNotNone(context.template_node())
        self.assertEqual("1", context.template_node().template.word)
        self.assertEqual("MAN", context.star(1))

        context = self.match_sentence("I AM A WOMAN", topic="X", that="Y")
        self.assertIsNotNone(context)
        self.assertIsNotNone(context.template_node())
        self.assertEqual("1", context.template_node().template.word)
        self.assertEqual("WOMAN", context.star(1))

    def test_multi_word_set_match(self):

        self._client_context.brain._sets_collection.add_set("COLOR", {"RED": [["RED"],
                                                                              ["RED", "AMBER"],
                                                                              ["RED", "BURNT", "OAK"],
                                                                              ["RED", "ORANGE"]
                                                                              ]}, "teststore")

        self.add_pattern_to_graph(pattern="I LIKE <set>color</set> *", topic="*", that="*", template="1")

        context = self.match_sentence("I LIKE RED PAINT", topic="*", that="*")
        self.assertIsNotNone(context)
        self.assertIsNotNone(context.template_node())
        self.assertEqual("1", context.template_node().template.word)
        self.assertEqual("RED", context.star(1))
        self.assertEqual("PAINT", context.star(2))

        context = self.match_sentence("I LIKE RED AMBER CARS", topic="*", that="*")
        self.assertIsNotNone(context)
        self.assertIsNotNone(context.template_node())
        self.assertEqual("1", context.template_node().template.word)
        self.assertEqual("RED AMBER", context.star(1))
        self.assertEqual("CARS", context.star(2))

        context = self.match_sentence("I LIKE RED BURNT OAK MOTOR BIKES", topic="*", that="*")
        self.assertIsNotNone(context)
        self.assertIsNotNone(context.template_node())
        self.assertEqual("1", context.template_node().template.word)
        self.assertEqual("RED BURNT OAK", context.star(1))
        self.assertEqual("MOTOR BIKES", context.star(2))

    def test_basic_set_number_match(self):
        self._client_context.brain.dynamics.add_dynamic_set('number', "programy.dynamic.sets.numeric.IsNumeric", None)

        self.add_pattern_to_graph(pattern="I AM <set>number</set> YEARS OLD", topic="X", that="Y", template="1")

        context = self.match_sentence("I AM 49 YEARS OLD", topic="X", that="Y")
        self.assertIsNotNone(context)
        self.assertIsNotNone(context.template_node())
        self.assertEqual("1", context.template_node().template.word)

        self.assertEqual("49", context.star(1))
