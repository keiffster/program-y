from programy.parser.template.nodes.condition import TemplateConditionVariable
from programy.parser.template.nodes.word import TemplateWordNode
from programytest.parser.base import ParserTestsBaseClass


class TemplateConditionVariableTests(ParserTestsBaseClass):

    def test_init_defaults(self):
        var = TemplateConditionVariable()
        self.assertIsNotNone(var)
        self.assertIsNone(var.name)
        self.assertIsNone(var.value)
        self.assertEqual(var.var_type, TemplateConditionVariable.GLOBAL)
        self.assertFalse(var.loop)
        self.assertEquals("[NODE]", var.to_string())

    def test_init_global_name_and_value(self):
        var = TemplateConditionVariable(name="var1", value=TemplateWordNode("value1"))
        self.assertIsNotNone(var)
        self.assertEqual(var.name, "var1")
        self.assertEqual(var.value.word, "value1")
        self.assertEqual(var.var_type, TemplateConditionVariable.GLOBAL)
        self.assertFalse(var.loop)
        self.assertEquals("[NODE]", var.to_string())

    def test_init_global_name_only(self):
        var = TemplateConditionVariable(name="var1")
        self.assertIsNotNone(var)
        self.assertEqual(var.name, "var1")
        self.assertIsNone(var.value)
        self.assertEqual(var.var_type, TemplateConditionVariable.GLOBAL)
        self.assertFalse(var.loop)
        self.assertEquals("[NODE]", var.to_string())

    def test_init_global_value_only(self):
        var = TemplateConditionVariable(value=TemplateWordNode("value1"))
        self.assertIsNotNone(var)
        self.assertIsNone(var.name)
        self.assertEqual(var.value.word, "value1")
        self.assertEqual(var.var_type, TemplateConditionVariable.GLOBAL)
        self.assertFalse(var.loop)
        self.assertEquals("[NODE]", var.to_string())

    def test_init_global(self):
        var = TemplateConditionVariable(name="var1", value=TemplateWordNode("value1"), var_type=TemplateConditionVariable.GLOBAL)
        self.assertIsNotNone(var)
        self.assertEqual(var.name, "var1")
        self.assertEqual(var.value.word, "value1")
        self.assertEqual(var.var_type, TemplateConditionVariable.GLOBAL)
        self.assertFalse(var.loop)

    def test_init_global_with_loop(self):
        var = TemplateConditionVariable(name="var1", value=TemplateWordNode("value1"), var_type=TemplateConditionVariable.GLOBAL,loop=True)
        self.assertIsNotNone(var)
        self.assertEqual(var.name, "var1")
        self.assertEqual(var.value.word, "value1")
        self.assertEqual(var.var_type, TemplateConditionVariable.GLOBAL)
        self.assertTrue(var.loop)

    def test_init_local(self):
        var = TemplateConditionVariable(name="var1", value=TemplateWordNode("value1"), var_type=TemplateConditionVariable.LOCAL)
        self.assertIsNotNone(var)
        self.assertEqual(var.name, "var1")
        self.assertEqual(var.value.word, "value1")
        self.assertEqual(var.var_type, TemplateConditionVariable.LOCAL)
        self.assertFalse(var.loop)

    def test_init_local_with_loop(self):
        var = TemplateConditionVariable(name="var1", value=TemplateWordNode("value1"), var_type=TemplateConditionVariable.LOCAL, loop=True)
        self.assertIsNotNone(var)
        self.assertEqual(var.name, "var1")
        self.assertEqual(var.value.word, "value1")
        self.assertEqual(var.var_type, TemplateConditionVariable.LOCAL)
        self.assertTrue(var.loop)

    def test_init_bot(self):
        var = TemplateConditionVariable(name="var1", value=TemplateWordNode("value1"), var_type=TemplateConditionVariable.BOT)
        self.assertIsNotNone(var)
        self.assertEqual(var.name, "var1")
        self.assertEqual(var.value.word, "value1")
        self.assertEqual(var.var_type, TemplateConditionVariable.BOT)
        self.assertFalse(var.loop)

    def test_init_bot_with_loop(self):
        var = TemplateConditionVariable(name="var1", value=TemplateWordNode("value1"), var_type=TemplateConditionVariable.BOT, loop=True)
        self.assertIsNotNone(var)
        self.assertEqual(var.name, "var1")
        self.assertEqual(var.value.word, "value1")
        self.assertEqual(var.var_type, TemplateConditionVariable.BOT)
        self.assertTrue(var.loop)
