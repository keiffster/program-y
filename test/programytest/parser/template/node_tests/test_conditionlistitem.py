from programy.parser.template.nodes.condition import TemplateConditionListItemNode
from programy.parser.template.nodes.word import TemplateWordNode
from programytest.parser.base import ParserTestsBaseClass


class TemplateConditionListItemNodeTests(ParserTestsBaseClass):

    def test_init_defaults(self):
        var = TemplateConditionListItemNode()
        self.assertIsNotNone(var)
        self.assertIsNone(var.name)
        self.assertIsNone(var.value)
        self.assertEqual(var.var_type, TemplateConditionListItemNode.GLOBAL)
        self.assertFalse(var.loop)
        self.assertTrue(var.is_default())
        self.assertEqual("[CONDITIONLIST]", var.to_string())
        self.assertEqual("<li></li>", var.to_xml(self._client_context))

    def test_init_global_as_default(self):
        var = TemplateConditionListItemNode(name="var1", value=TemplateWordNode("value1"))
        self.assertIsNotNone(var)
        self.assertEqual(var.name, "var1")
        self.assertEqual(var.value.word, "value1")
        self.assertEqual(var.var_type, TemplateConditionListItemNode.GLOBAL)
        self.assertFalse(var.loop)
        self.assertFalse(var.is_default())
        self.assertEqual("[CONDITIONLIST(var1=[WORD]value1)]", var.to_string())
        self.assertEqual('<li name="var1"><value>value1</value></li>', var.to_xml(self._client_context))

    def test_init_global_as_default_no_value(self):
        var = TemplateConditionListItemNode(value=TemplateWordNode("value1"))
        self.assertIsNotNone(var)
        self.assertIsNone(var.name)
        self.assertEqual(var.value.word, "value1")
        self.assertEqual(var.var_type, TemplateConditionListItemNode.GLOBAL)
        self.assertFalse(var.loop)
        self.assertFalse(var.is_default())
        self.assertEqual("[CONDITIONLIST([WORD]value1)]", var.to_string())
        self.assertEqual('<li><value>value1</value></li>', var.to_xml(self._client_context))

    def test_init_global_as_default_no_name(self):
        var = TemplateConditionListItemNode(name="var1")
        self.assertIsNotNone(var)
        self.assertEqual(var.name, "var1")
        self.assertEqual(var.var_type, TemplateConditionListItemNode.GLOBAL)
        self.assertFalse(var.loop)
        self.assertTrue(var.is_default())
        self.assertEqual("[CONDITIONLIST(var1)]", var.to_string())
        self.assertEqual('<li name="var1"></li>', var.to_xml(self._client_context))

    def test_init_global(self):
        var = TemplateConditionListItemNode(name="var1", value=TemplateWordNode("value1"), var_type=TemplateConditionListItemNode.GLOBAL)
        self.assertIsNotNone(var)
        self.assertEqual(var.name, "var1")
        self.assertEqual(var.value.word, "value1")
        self.assertEqual(var.var_type, TemplateConditionListItemNode.GLOBAL)
        self.assertFalse(var.loop)
        self.assertFalse(var.is_default())
        self.assertEqual("[CONDITIONLIST(var1=[WORD]value1)]", var.to_string())
        self.assertEqual('<li name="var1"><value>value1</value></li>', var.to_xml(self._client_context))

    def test_init_global_with_loop(self):
        var = TemplateConditionListItemNode(name="var1", value=TemplateWordNode("value1"), var_type=TemplateConditionListItemNode.GLOBAL,loop=True)
        self.assertIsNotNone(var)
        self.assertEqual(var.name, "var1")
        self.assertEqual(var.value.word, "value1")
        self.assertEqual(var.var_type, TemplateConditionListItemNode.GLOBAL)
        self.assertTrue(var.loop)
        self.assertFalse(var.is_default())
        self.assertEqual("[CONDITIONLIST(var1=[WORD]value1)]", var.to_string())
        self.assertEqual('<li name="var1"><value>value1</value><loop /></li>', var.to_xml(self._client_context))

    def test_init_local(self):
        var = TemplateConditionListItemNode(name="var1", value=TemplateWordNode("value1"), var_type=TemplateConditionListItemNode.LOCAL)
        self.assertIsNotNone(var)
        self.assertEqual(var.name, "var1")
        self.assertEqual(var.value.word, "value1")
        self.assertEqual(var.var_type, TemplateConditionListItemNode.LOCAL)
        self.assertFalse(var.loop)
        self.assertFalse(var.is_default())
        self.assertEqual("[CONDITIONLIST(var1=[WORD]value1)]", var.to_string())
        self.assertEqual('<li var="var1"><value>value1</value></li>', var.to_xml(self._client_context))

    def test_init_local_with_loop(self):
        var = TemplateConditionListItemNode(name="var1", value=TemplateWordNode("value1"), var_type=TemplateConditionListItemNode.LOCAL, loop=True)
        self.assertIsNotNone(var)
        self.assertEqual(var.name, "var1")
        self.assertEqual(var.value.word, "value1")
        self.assertEqual(var.var_type, TemplateConditionListItemNode.LOCAL)
        self.assertTrue(var.loop)
        self.assertFalse(var.is_default())
        self.assertEqual("[CONDITIONLIST(var1=[WORD]value1)]", var.to_string())
        self.assertEqual('<li var="var1"><value>value1</value><loop /></li>', var.to_xml(self._client_context))

    def test_init_bot(self):
        var = TemplateConditionListItemNode(name="var1", value=TemplateWordNode("value1"), var_type=TemplateConditionListItemNode.BOT)
        self.assertIsNotNone(var)
        self.assertEqual(var.name, "var1")
        self.assertEqual(var.value.word, "value1")
        self.assertEqual(var.var_type, TemplateConditionListItemNode.BOT)
        self.assertFalse(var.loop)
        self.assertFalse(var.is_default())
        self.assertEqual("[CONDITIONLIST(var1=[WORD]value1)]", var.to_string())
        self.assertEqual('<li bot="var1"><value>value1</value></li>', var.to_xml(self._client_context))

    def test_init_bot_with_loop(self):
        var = TemplateConditionListItemNode(name="var1", value=TemplateWordNode("value1"), var_type=TemplateConditionListItemNode.BOT, loop=True)
        self.assertIsNotNone(var)
        self.assertEqual(var.name, "var1")
        self.assertEqual(var.value.word, "value1")
        self.assertEqual(var.var_type, TemplateConditionListItemNode.BOT)
        self.assertTrue(var.loop)
        self.assertFalse(var.is_default())
        self.assertEqual("[CONDITIONLIST(var1=[WORD]value1)]", var.to_string())
        self.assertEqual('<li bot="var1"><value>value1</value><loop /></li>', var.to_xml(self._client_context))

    def test_init_default(self):
        var = TemplateConditionListItemNode(name="var1", value=TemplateWordNode("value1"), var_type=TemplateConditionListItemNode.DEFAULT)
        self.assertIsNotNone(var)
        self.assertEqual(var.name, "var1")
        self.assertEqual(var.value.word, "value1")
        self.assertEqual(var.var_type, TemplateConditionListItemNode.DEFAULT)
        self.assertFalse(var.loop)
        self.assertFalse(var.is_default())
        self.assertEqual("[CONDITIONLIST(var1=[WORD]value1)]", var.to_string())
        self.assertEqual('<li default="var1"><value>value1</value></li>', var.to_xml(self._client_context))

    def test_init_default_with_loop(self):
        var = TemplateConditionListItemNode(name="var1", value=TemplateWordNode("value1"), var_type=TemplateConditionListItemNode.DEFAULT, loop=True)
        self.assertIsNotNone(var)
        self.assertEqual(var.name, "var1")
        self.assertEqual(var.value.word, "value1")
        self.assertEqual(var.var_type, TemplateConditionListItemNode.DEFAULT)
        self.assertTrue(var.loop)
        self.assertFalse(var.is_default())
        self.assertEqual("[CONDITIONLIST(var1=[WORD]value1)]", var.to_string())
        self.assertEqual('<li default="var1"><value>value1</value><loop /></li>', var.to_xml(self._client_context))

    def test_init_unknown(self):
        var = TemplateConditionListItemNode(name="var1", value=TemplateWordNode("value1"),
                                            var_type="Unknown")
        self.assertIsNotNone(var)
        self.assertEqual(var.name, "var1")
        self.assertEqual(var.value.word, "value1")
        self.assertEqual(var.var_type, "Unknown")
        self.assertFalse(var.loop)
        self.assertFalse(var.is_default())
        self.assertEqual("[CONDITIONLIST(var1=[WORD]value1)]", var.to_string())
        self.assertEqual('<li unknown="var1"><value>value1</value></li>', var.to_xml(self._client_context))

    def test_init_unknown_with_loop(self):
        var = TemplateConditionListItemNode(name="var1", value=TemplateWordNode("value1"),
                                            var_type="Unknown", loop=True)
        self.assertIsNotNone(var)
        self.assertEqual(var.name, "var1")
        self.assertEqual(var.value.word, "value1")
        self.assertEqual(var.var_type, "Unknown")
        self.assertTrue(var.loop)
        self.assertFalse(var.is_default())
        self.assertEqual("[CONDITIONLIST(var1=[WORD]value1)]", var.to_string())
        self.assertEqual('<li unknown="var1"><value>value1</value><loop /></li>', var.to_xml(self._client_context))

    def test_to_xml_global_with_loop(self):
        var = TemplateConditionListItemNode(name="var1", value=TemplateWordNode("value1"), var_type=TemplateConditionListItemNode.GLOBAL, loop=True)
        self.assertEquals('<li name="var1"><value>value1</value><loop /></li>', var.to_xml(self._client_context))

    def test_to_xml_global_without_loop(self):
        var = TemplateConditionListItemNode(name="var1", value=TemplateWordNode("value1"), var_type=TemplateConditionListItemNode.GLOBAL, loop=False)
        self.assertEquals('<li name="var1"><value>value1</value></li>', var.to_xml(self._client_context))

    def test_to_xml_local_with_loop(self):
        var = TemplateConditionListItemNode(name="var1", value=TemplateWordNode("value1"), var_type=TemplateConditionListItemNode.LOCAL, loop=True)
        self.assertEquals('<li var="var1"><value>value1</value><loop /></li>', var.to_xml(self._client_context))

    def test_to_xml_local_without_loop(self):
        var = TemplateConditionListItemNode(name="var1", value=TemplateWordNode("value1"), var_type=TemplateConditionListItemNode.LOCAL, loop=False)
        self.assertEquals('<li var="var1"><value>value1</value></li>', var.to_xml(self._client_context))

    def test_to_xml_bot_with_loop(self):
        var = TemplateConditionListItemNode(name="var1", value=TemplateWordNode("value1"), var_type=TemplateConditionListItemNode.BOT, loop=True)
        self.assertEquals('<li bot="var1"><value>value1</value><loop /></li>', var.to_xml(self._client_context))

    def test_to_xml_bot_without_loop(self):
        var = TemplateConditionListItemNode(name="var1", value=TemplateWordNode("value1"), var_type=TemplateConditionListItemNode.BOT, loop=False)
        self.assertEquals('<li bot="var1"><value>value1</value></li>', var.to_xml(self._client_context))

    def test_to_xml_default_with_loop(self):
        var = TemplateConditionListItemNode(name="var1", value=TemplateWordNode("value1"), var_type=TemplateConditionListItemNode.DEFAULT, loop=True)
        self.assertEquals('<li default="var1"><value>value1</value><loop /></li>', var.to_xml(self._client_context))

    def test_to_xml_default_without_loop(self):
        var = TemplateConditionListItemNode(name="var1", value=TemplateWordNode("value1"), var_type=TemplateConditionListItemNode.DEFAULT, loop=False)
        self.assertEquals('<li default="var1"><value>value1</value></li>', var.to_xml(self._client_context))

    def test_to_xml_unknown_with_loop(self):
        var = TemplateConditionListItemNode(name="var1", value=TemplateWordNode("value1"), var_type="Unknown", loop=True)
        self.assertEquals('<li unknown="var1"><value>value1</value><loop /></li>', var.to_xml(self._client_context))

    def test_to_xml_unknown_without_loop(self):
        var = TemplateConditionListItemNode(name="var1", value=TemplateWordNode("value1"), var_type="Unknown", loop=False)
        self.assertEquals('<li unknown="var1"><value>value1</value></li>', var.to_xml(self._client_context))
