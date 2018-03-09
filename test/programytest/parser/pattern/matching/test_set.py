
from programytest.parser.pattern.matching.base import PatternMatcherBaseClass

from programy.mappings.sets import SetLoader

class PatternMatcherSetTests(PatternMatcherBaseClass):

    def test_basic_set_match_as_text(self):

        loader = SetLoader()

        if self._client_context.brain.sets.contains("SEX") is False:
            self._client_context.brain.sets.add_set("SEX", loader.load_from_text("""
            Man
            Woman
            """))

        self.add_pattern_to_graph(pattern="I AM A <set>sex</set>", topic="X", that="Y", template="1")

        context = self.match_sentence("I AM A MAN", topic="X", that="Y")
        self.assertIsNotNone(context)
        self.assertIsNotNone(context.template_node())
        self.assertEqual("1", context.template_node().template.word)
        self.assertEqual("Man", context.star(1))

        context = self.match_sentence("I AM A WOMAN", topic="X", that="Y")
        self.assertIsNotNone(context)
        self.assertIsNotNone(context.template_node())
        self.assertEqual("1", context.template_node().template.word)
        self.assertEqual("Woman", context.star(1))

    def test_basic_set_match_as_name(self):

        loader = SetLoader()

        if self._client_context.brain.sets.contains("SEX") is False:
            self._client_context.brain.sets.add_set("SEX", loader.load_from_text("""
            Man
            Woman
            """))

        self.add_pattern_to_graph(pattern='I AM A <set name="sex" />', topic="X", that="Y", template="1")

        context = self.match_sentence("I AM A MAN", topic="X", that="Y")
        self.assertIsNotNone(context)
        self.assertIsNotNone(context.template_node())
        self.assertEqual("1", context.template_node().template.word)
        self.assertEqual("Man", context.star(1))

        context = self.match_sentence("I AM A WOMAN", topic="X", that="Y")
        self.assertIsNotNone(context)
        self.assertIsNotNone(context.template_node())
        self.assertEqual("1", context.template_node().template.word)
        self.assertEqual("Woman", context.star(1))

    def test_multi_word_set_match(self):
        loader = SetLoader()

        self._client_context.brain.sets.add_set("COLOR", loader.load_from_text("""
        RED
        RED AMBER
        RED BURNT OAK
        RED ORANGE
        """))

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
