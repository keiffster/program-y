
from test.parser.pattern.matching.base import PatternMatcherBaseClass

class PatternMatcherBotTests(PatternMatcherBaseClass):

    def test_basic_bot_match(self):

        PatternMatcherBaseClass.bot.brain.properties.add_property('firstname', 'testbot')

        self.add_pattern_to_graph(pattern="<bot>firstname</bot>", topic="X", that="Y", template="1")

        context = self.match_sentence("testbot", topic="X", that="Y")
        self.assertIsNotNone(context)
        self.assertIsNotNone(context.template_node())
        self.assertEqual("1", context.template_node().template.word)

        self.assertEqual("testbot", context.star(1))
