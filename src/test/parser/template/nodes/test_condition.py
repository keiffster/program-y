import xml.etree.ElementTree as ET

from programy.dialog import Question

from programy.parser.template.nodes.condition import TemplateConditionNode

from test.parser.template.base import TemplateTestsBaseClass

class TemplateConditionNodeTests(TemplateTestsBaseClass):

    def test_get_predicate_value(self):
        node = TemplateConditionNode()
        self.assertIsNotNone(node)

        self.bot.conversation(self.clientid)._predicates['name1'] = "value1"

        value = node._get_predicate_value(self.bot, self.clientid, "name1", False)
        self.assertEqual(value, "value1")

        question = Question.create_from_text("Hello")
        self.bot.conversation(self.clientid).record_dialog(question)
        self.bot.conversation(self.clientid).current_question().set_predicate("var1", "value2")

        value = node._get_predicate_value(self.bot, self.clientid, "var1", True)
        self.assertEqual(value, "value2")

        value = node._get_predicate_value(self.bot, self.clientid, "unknown", True)
        self.assertEqual(value, "")

        self.bot.brain.properties.add_property("default-get", "Unknown")
        value = node._get_predicate_value(self.bot, self.clientid, "name3", False)
        self.assertEqual(value, "Unknown")

