import xml.etree.ElementTree as ET

from programy.parser.template.nodes.base import TemplateNode
from programy.parser.template.nodes.condition import TemplateConditionNode
from programy.parser.template.nodes.condition import TemplateConditionListItemNode
from programy.parser.template.nodes.condition import TemplateConditionVariable
from programytest.parser.template.graph_tests.graph_test_client import TemplateGraphTestClient


class TemplateGraphConditionTests(TemplateGraphTestClient):

    ##################################################################################################################
    # Block
    #

    def test_condition_template_block_global_attributes(self):
        template = ET.fromstring("""
			<template>
				<condition name="aname" value="avalue">
				    X
				    <random>
				        <li>1</li>
				        <li>2</li>
				    </random>
				    Y
				</condition>
			</template>
			""")
        ast = self._graph.parse_template_expression(template)
        self.assertIsNotNone(ast)
        self.assertIsInstance(ast, TemplateNode)
        self.assertIsNotNone(ast.children)

        template_node = ast.children[0]
        self.assertIsNotNone(template_node)
        self.assertIsInstance(template_node, TemplateConditionNode)

        self.assertEqual(template_node.name, "aname")
        self.assertIsInstance(template_node.value, TemplateNode)
        self.assertEqual(template_node.var_type, TemplateConditionVariable.GLOBAL)
        self.assertFalse(template_node.loop)
        self.assertEqual(len(template_node.children), 3)

    def test_condition_template_block_var_attributes(self):
        template = ET.fromstring("""
            <template>
                <condition var="aname" value="avalue">
                    X 
                    <random>
                        <li>1</li>
                        <li>2</li>
                    </random> 
                    Y
                </condition>
            </template>
            """)
        ast = self._graph.parse_template_expression(template)
        self.assertIsNotNone(ast)
        self.assertIsInstance(ast, TemplateNode)
        self.assertIsNotNone(ast.children)

        template_node = ast.children[0]
        self.assertIsNotNone(template_node)
        self.assertIsInstance(template_node, TemplateConditionNode)

        self.assertEqual(template_node.name, "aname")
        self.assertIsInstance(template_node.value, TemplateNode)
        self.assertFalse(template_node.loop)
        self.assertEqual(template_node.var_type, TemplateConditionVariable.LOCAL)
        self.assertEqual(len(template_node.children), 3)

    def test_condition_template_block_bot_attributes(self):
        template = ET.fromstring("""
            <template>
                <condition bot="aname" value="avalue">
                    X 
                    <random>
                        <li>1</li>
                        <li>2</li>
                    </random> 
                    Y
                </condition>
            </template>
            """)
        ast = self._graph.parse_template_expression(template)
        self.assertIsNotNone(ast)
        self.assertIsInstance(ast, TemplateNode)
        self.assertIsNotNone(ast.children)

        template_node = ast.children[0]
        self.assertIsNotNone(template_node)
        self.assertIsInstance(template_node, TemplateConditionNode)

        self.assertEqual(template_node.name, "aname")
        self.assertIsInstance(template_node.value, TemplateNode)
        self.assertFalse(template_node.loop)
        self.assertEqual(template_node.var_type, TemplateConditionVariable.BOT)
        self.assertEqual(len(template_node.children), 3)

    def test_condition_template_block_global_name_attr_val_child(self):
        template = ET.fromstring("""
			<template>
				<condition name="aname">
				    <value>avalue</value>
				    X
				</condition>
			</template>
			""")
        ast = self._graph.parse_template_expression(template)
        self.assertIsNotNone(ast)
        self.assertIsInstance(ast, TemplateNode)
        self.assertIsNotNone(ast.children)

        template_node = ast.children[0]
        self.assertIsNotNone(template_node)
        self.assertIsInstance(template_node, TemplateConditionNode)

        self.assertEqual(template_node.name, "aname")
        self.assertIsInstance(template_node.value, TemplateNode)
        self.assertFalse(template_node.loop)
        self.assertEqual(template_node.var_type, TemplateConditionVariable.GLOBAL)
        self.assertEqual(len(template_node.children), 1)

    def test_condition_template_block_local_name_attr_val_child(self):
        template = ET.fromstring("""
            <template>
                <condition var="aname">
                    <value>avalue</value>
                    X
                </condition>
            </template>
            """)
        ast = self._graph.parse_template_expression(template)
        self.assertIsNotNone(ast)
        self.assertIsInstance(ast, TemplateNode)
        self.assertIsNotNone(ast.children)

        template_node = ast.children[0]
        self.assertIsNotNone(template_node)
        self.assertIsInstance(template_node, TemplateConditionNode)

        self.assertEqual(template_node.name, "aname")
        self.assertIsInstance(template_node.value, TemplateNode)
        self.assertFalse(template_node.loop)
        self.assertEqual(template_node.var_type, TemplateConditionVariable.LOCAL)
        self.assertEqual(len(template_node.children), 1)

    def test_condition_template_block_bot_name_attr_val_child(self):
        template = ET.fromstring("""
            <template>
                <condition bot="aname">
                    <value>avalue</value>
                    X
                </condition>
            </template>
            """)
        ast = self._graph.parse_template_expression(template)
        self.assertIsNotNone(ast)
        self.assertIsInstance(ast, TemplateNode)
        self.assertIsNotNone(ast.children)

        template_node = ast.children[0]
        self.assertIsNotNone(template_node)
        self.assertIsInstance(template_node, TemplateConditionNode)

        self.assertEqual(template_node.name, "aname")
        self.assertIsInstance(template_node.value, TemplateNode)
        self.assertFalse(template_node.loop)
        self.assertEqual(template_node.var_type, TemplateConditionVariable.BOT)
        self.assertEqual(len(template_node.children), 1)

    def test_condition_template_block_global_name_child_val_attr(self):
        template = ET.fromstring("""
			<template>
				<condition value="avalue">
				    <name>aname</name>
				    X
				</condition>
			</template>
			""")
        ast = self._graph.parse_template_expression(template)
        self.assertIsNotNone(ast)
        self.assertIsInstance(ast, TemplateNode)
        self.assertIsNotNone(ast.children)

        template_node = ast.children[0]
        self.assertIsNotNone(template_node)
        self.assertIsInstance(template_node, TemplateConditionNode)

        self.assertEqual(template_node.name, "aname")
        self.assertIsInstance(template_node.value, TemplateNode)
        self.assertFalse(template_node.loop)
        self.assertEqual(template_node.var_type, TemplateConditionVariable.GLOBAL)
        self.assertEqual(len(template_node.children), 1)

    def test_condition_template_block_local_name_child_val_attr(self):
        template = ET.fromstring("""
            <template>
                <condition value="avalue"><var>aname</var>X</condition>
            </template>
            """)
        ast = self._graph.parse_template_expression(template)
        self.assertIsNotNone(ast)
        self.assertIsInstance(ast, TemplateNode)
        self.assertIsNotNone(ast.children)

        template_node = ast.children[0]
        self.assertIsNotNone(template_node)
        self.assertIsInstance(template_node, TemplateConditionNode)

        self.assertEqual(template_node.name, "aname")
        self.assertIsInstance(template_node.value, TemplateNode)
        self.assertFalse(template_node.loop)
        self.assertEqual(template_node.var_type, TemplateConditionVariable.LOCAL)
        self.assertEqual(len(template_node.children), 1)

    def test_condition_template_block_bot_name_child_val_attr(self):
        template = ET.fromstring("""
            <template>
                <condition value="avalue">
                    <bot>aname</bot>
                    X
                </condition>
            </template>
            """)
        ast = self._graph.parse_template_expression(template)
        self.assertIsNotNone(ast)
        self.assertIsInstance(ast, TemplateNode)
        self.assertIsNotNone(ast.children)

        template_node = ast.children[0]
        self.assertIsNotNone(template_node)
        self.assertIsInstance(template_node, TemplateConditionNode)

        self.assertEqual(template_node.name, "aname")
        self.assertIsInstance(template_node.value, TemplateNode)
        self.assertFalse(template_node.loop)
        self.assertEqual(template_node.var_type, TemplateConditionVariable.BOT)
        self.assertEqual(len(template_node.children), 1)

    def test_condition_template_block_global_name_child_val_child(self):
        template = ET.fromstring("""
			<template>
				<condition>
				    <name>aname</name>
				    <value>avalue</value>
				    X
				</condition>
			</template>
			""")
        ast = self._graph.parse_template_expression(template)
        self.assertIsNotNone(ast)
        self.assertIsInstance(ast, TemplateNode)
        self.assertIsNotNone(ast.children)

        template_node = ast.children[0]
        self.assertIsNotNone(template_node)
        self.assertIsInstance(template_node, TemplateConditionNode)

        self.assertEqual(template_node.name, "aname")
        self.assertIsInstance(template_node.value, TemplateNode)
        self.assertFalse(template_node.loop)
        self.assertEqual(template_node.var_type, TemplateConditionVariable.GLOBAL)
        self.assertEqual(len(template_node.children), 1)

    def test_condition_template_block_local_name_child_val_child(self):
        template = ET.fromstring("""
            <template>
                <condition>
                    <var>aname</var>
                    <value>avalue</value>
                    X
                </condition>
            </template>
            """)
        ast = self._graph.parse_template_expression(template)
        self.assertIsNotNone(ast)
        self.assertIsInstance(ast, TemplateNode)
        self.assertIsNotNone(ast.children)

        template_node = ast.children[0]
        self.assertIsNotNone(template_node)
        self.assertIsInstance(template_node, TemplateConditionNode)

        self.assertEqual(template_node.name, "aname")
        self.assertIsInstance(template_node.value, TemplateNode)
        self.assertFalse(template_node.loop)
        self.assertEqual(template_node.var_type, TemplateConditionVariable.LOCAL)
        self.assertEqual(len(template_node.children), 1)

    def test_condition_template_block_bot_name_child_val_child(self):
        template = ET.fromstring("""
            <template>
                <condition>
                    <bot>aname</bot>
                    <value>avalue</value>
                    X
                </condition>
            </template>
            """)
        ast = self._graph.parse_template_expression(template)
        self.assertIsNotNone(ast)
        self.assertIsInstance(ast, TemplateNode)
        self.assertIsNotNone(ast.children)

        template_node = ast.children[0]
        self.assertIsNotNone(template_node)
        self.assertIsInstance(template_node, TemplateConditionNode)

        self.assertEqual(template_node.name, "aname")
        self.assertIsInstance(template_node.value, TemplateNode)
        self.assertFalse(template_node.loop)
        self.assertEqual(template_node.var_type, TemplateConditionVariable.BOT)
        self.assertEqual(len(template_node.children), 1)

    ##################################################################################################################
    # Single
    #

    def test_condition_template_single_global_name_child_value_attrs(self):
        template = ET.fromstring("""
			<template>
				<condition>
					<name>aname</name>
					<li value="a">A</li>
					<li value="b">B</li>
					<li><value>c</value>C</li>
					<li>D</li>
				</condition>
			</template>
			""")
        ast = self._graph.parse_template_expression(template)
        self.assertIsNotNone(ast)
        self.assertIsInstance(ast, TemplateNode)
        self.assertIsNotNone(ast.children)

        template_node = ast.children[0]
        self.assertIsNotNone(template_node)
        self.assertIsInstance(template_node, TemplateConditionNode)
        self.assertEqual(template_node.var_type, TemplateConditionVariable.GLOBAL)
        self.assertEqual(template_node.name, "aname")
        self.assertEqual(len(template_node.children), 4)

        node = template_node.children[0]
        self.assertIsInstance(node, TemplateConditionListItemNode)
        self.assertEqual(node.var_type, TemplateConditionVariable.GLOBAL)
        self.assertFalse(node.loop)
        self.assertIsNone(node.name)
        self.assertIsInstance(node.value, TemplateNode)
        self.assertFalse(node.is_default())
        self.assertEqual(len(node.children), 1)
        self.assertEqual(node.children[0].resolve(self._client_context), "A")

        node = template_node.children[1]
        self.assertIsInstance(node, TemplateConditionListItemNode)
        self.assertEqual(node.var_type, TemplateConditionVariable.GLOBAL)
        self.assertFalse(node.loop)
        self.assertIsNone(node.name)
        self.assertIsInstance(node.value, TemplateNode)
        self.assertFalse(node.is_default())
        self.assertEqual(len(node.children), 1)
        self.assertEqual(node.children[0].resolve(self._client_context), "B")

        node = template_node.children[2]
        self.assertIsInstance(node, TemplateConditionListItemNode)
        self.assertEqual(node.var_type, TemplateConditionVariable.GLOBAL)
        self.assertFalse(node.loop)
        self.assertIsNone(node.name)
        self.assertIsInstance(node.value, TemplateNode)
        self.assertFalse(node.is_default())
        self.assertEqual(len(node.children), 1)
        self.assertEqual(node.children[0].resolve(self._client_context), "C")

        node = template_node.children[3]
        self.assertIsInstance(node, TemplateConditionListItemNode)
        self.assertEqual(node.var_type, TemplateConditionVariable.GLOBAL)
        self.assertFalse(node.loop)
        self.assertIsNone(node.name)
        self.assertIsNone(node.value)
        self.assertTrue(node.is_default())
        self.assertEqual(len(node.children), 1)
        self.assertEqual(node.children[0].resolve(self._client_context), "D")

    def test_condition_template_single_global_name_child_value_attrs_loop(self):
        template = ET.fromstring("""
            <template>
                <condition>
                    <name>aname</name>
                    <li value="a">A <loop /></li>
                    <li value="b">B</li>
                    <li><value>c</value>C</li>
                    <li>D</li>
                </condition>
            </template>
            """)
        ast = self._graph.parse_template_expression(template)
        self.assertIsNotNone(ast)
        self.assertIsInstance(ast, TemplateNode)
        self.assertIsNotNone(ast.children)

        template_node = ast.children[0]
        self.assertIsNotNone(template_node)
        self.assertIsInstance(template_node, TemplateConditionNode)
        self.assertEqual(template_node.var_type, TemplateConditionVariable.GLOBAL)
        self.assertEqual(template_node.name, "aname")
        self.assertEqual(len(template_node.children), 4)

        node = template_node.children[0]
        self.assertIsInstance(node, TemplateConditionListItemNode)
        self.assertEqual(node.var_type, TemplateConditionVariable.GLOBAL)
        self.assertTrue(node.loop)
        self.assertIsNone(node.name)
        self.assertIsInstance(node.value, TemplateNode)
        self.assertFalse(node.is_default())
        self.assertEqual(len(node.children), 1)
        self.assertEqual(node.children[0].resolve(self._client_context), "A")

        node = template_node.children[1]
        self.assertIsInstance(node, TemplateConditionListItemNode)
        self.assertEqual(node.var_type, TemplateConditionVariable.GLOBAL)
        self.assertFalse(node.loop)
        self.assertIsNone(node.name)
        self.assertIsInstance(node.value, TemplateNode)
        self.assertFalse(node.is_default())
        self.assertEqual(len(node.children), 1)
        self.assertEqual(node.children[0].resolve(self._client_context), "B")

        node = template_node.children[2]
        self.assertIsInstance(node, TemplateConditionListItemNode)
        self.assertEqual(node.var_type, TemplateConditionVariable.GLOBAL)
        self.assertFalse(node.loop)
        self.assertIsNone(node.name)
        self.assertIsInstance(node.value, TemplateNode)
        self.assertFalse(node.is_default())
        self.assertEqual(len(node.children), 1)
        self.assertEqual(node.children[0].resolve(self._client_context), "C")

        node = template_node.children[3]
        self.assertIsInstance(node, TemplateConditionListItemNode)
        self.assertEqual(node.var_type, TemplateConditionVariable.GLOBAL)
        self.assertFalse(node.loop)
        self.assertIsNone(node.name)
        self.assertIsNone(node.value)
        self.assertTrue(node.is_default())
        self.assertEqual(len(node.children), 1)
        self.assertEqual(node.children[0].resolve(self._client_context), "D")

    def test_condition_template_single_local_name_child_value_attrs_loop(self):
        template = ET.fromstring("""
            <template>
                <condition>
                    <var>aname</var>
                    <li value="a">A</li>
                    <li value="b">B</li>
                    <li><value>c</value>C</li>
                    <li>D</li>
                </condition>
            </template>
            """)
        ast = self._graph.parse_template_expression(template)
        self.assertIsNotNone(ast)
        self.assertIsInstance(ast, TemplateNode)
        self.assertIsNotNone(ast.children)

        template_node = ast.children[0]
        self.assertIsNotNone(template_node)
        self.assertIsInstance(template_node, TemplateConditionNode)
        self.assertEqual(template_node.var_type, TemplateConditionVariable.LOCAL)
        self.assertEqual(template_node.name, "aname")
        self.assertEqual(len(template_node.children), 4)

        node = template_node.children[0]
        self.assertIsInstance(node, TemplateConditionListItemNode)
        self.assertEqual(node.var_type, TemplateConditionVariable.LOCAL)
        self.assertFalse(node.loop)
        self.assertIsNone(node.name)
        self.assertIsInstance(node.value, TemplateNode)
        self.assertFalse(node.is_default())
        self.assertEqual(len(node.children), 1)
        self.assertEqual(node.children[0].resolve(self._client_context), "A")

        node = template_node.children[1]
        self.assertIsInstance(node, TemplateConditionListItemNode)
        self.assertEqual(node.var_type, TemplateConditionVariable.LOCAL)
        self.assertFalse(node.loop)
        self.assertIsNone(node.name)
        self.assertIsInstance(node.value, TemplateNode)
        self.assertFalse(node.is_default())
        self.assertEqual(len(node.children), 1)
        self.assertEqual(node.children[0].resolve(self._client_context), "B")

        node = template_node.children[2]
        self.assertIsInstance(node, TemplateConditionListItemNode)
        self.assertEqual(node.var_type, TemplateConditionVariable.LOCAL)
        self.assertFalse(node.loop)
        self.assertIsNone(node.name)
        self.assertIsInstance(node.value, TemplateNode)
        self.assertFalse(node.is_default())
        self.assertEqual(len(node.children), 1)
        self.assertEqual(node.children[0].resolve(self._client_context), "C")

        node = template_node.children[3]
        self.assertIsInstance(node, TemplateConditionListItemNode)
        self.assertEqual(node.var_type, TemplateConditionVariable.LOCAL)
        self.assertFalse(node.loop)
        self.assertIsNone(node.name)
        self.assertIsNone(node.value)
        self.assertTrue(node.is_default())
        self.assertEqual(len(node.children), 1)
        self.assertEqual(node.children[0].resolve(self._client_context), "D")

    def test_condition_template_single_global_name_child_value_attrs(self):
        template = ET.fromstring("""
			<template>
				<condition name="aname">
					<li value="a">A</li>
					<li value="b">B</li>
					<li><value>c</value>C</li>
					<li>D</li>
				</condition>
			</template>
			""")
        ast = self._graph.parse_template_expression(template)
        self.assertIsNotNone(ast)
        self.assertIsInstance(ast, TemplateNode)
        self.assertIsNotNone(ast.children)

        template_node = ast.children[0]
        self.assertIsNotNone(template_node)
        self.assertIsInstance(template_node, TemplateConditionNode)
        self.assertEqual(template_node.var_type, TemplateConditionVariable.GLOBAL)
        self.assertEqual(template_node.name, "aname")
        self.assertEqual(len(template_node.children), 4)

        node = template_node.children[0]
        self.assertIsInstance(node, TemplateConditionListItemNode)
        self.assertEqual(node.var_type, TemplateConditionVariable.GLOBAL)
        self.assertFalse(node.loop)
        self.assertIsNone(node.name)
        self.assertIsInstance(node.value, TemplateNode)
        self.assertFalse(node.is_default())
        self.assertEqual(len(node.children), 1)
        self.assertEqual(node.children[0].resolve(self._client_context), "A")

        node = template_node.children[1]
        self.assertIsInstance(node, TemplateConditionListItemNode)
        self.assertEqual(node.var_type, TemplateConditionVariable.GLOBAL)
        self.assertFalse(node.loop)
        self.assertIsNone(node.name)
        self.assertIsInstance(node.value, TemplateNode)
        self.assertFalse(node.is_default())
        self.assertEqual(len(node.children), 1)
        self.assertEqual(node.children[0].resolve(self._client_context), "B")

        node = template_node.children[2]
        self.assertIsInstance(node, TemplateConditionListItemNode)
        self.assertEqual(node.var_type, TemplateConditionVariable.GLOBAL)
        self.assertFalse(node.loop)
        self.assertIsNone(node.name)
        self.assertIsInstance(node.value, TemplateNode)
        self.assertFalse(node.is_default())
        self.assertEqual(len(node.children), 1)
        self.assertEqual(node.children[0].resolve(self._client_context), "C")

        node = template_node.children[3]
        self.assertIsInstance(node, TemplateConditionListItemNode)
        self.assertEqual(node.var_type, TemplateConditionVariable.GLOBAL)
        self.assertFalse(node.loop)
        self.assertIsNone(node.name)
        self.assertIsNone(node.value)
        self.assertTrue(node.is_default())
        self.assertEqual(len(node.children), 1)
        self.assertEqual(node.children[0].resolve(self._client_context), "D")

    def test_condition_template_single_local_name_attr_value_attrs(self):
        template = ET.fromstring("""
            <template>
                <condition var="aname">
                    <li value="a">A</li>
                    <li value="b">B</li>
                    <li><value>c</value>C</li>
                    <li>D</li>
                </condition>
            </template>
            """)
        ast = self._graph.parse_template_expression(template)
        self.assertIsNotNone(ast)
        self.assertIsInstance(ast, TemplateNode)
        self.assertIsNotNone(ast.children)

        template_node = ast.children[0]
        self.assertIsNotNone(template_node)
        self.assertIsInstance(template_node, TemplateConditionNode)
        self.assertEqual(template_node.var_type, TemplateConditionVariable.LOCAL)
        self.assertEqual(template_node.name, "aname")
        self.assertEqual(len(template_node.children), 4)

        node = template_node.children[0]
        self.assertIsInstance(node, TemplateConditionListItemNode)
        self.assertEqual(node.var_type, TemplateConditionVariable.LOCAL)
        self.assertFalse(node.loop)
        self.assertIsNone(node.name)
        self.assertIsInstance(node.value, TemplateNode)
        self.assertFalse(node.is_default())
        self.assertEqual(len(node.children), 1)
        self.assertEqual(node.children[0].resolve(self._client_context), "A")

        node = template_node.children[1]
        self.assertIsInstance(node, TemplateConditionListItemNode)
        self.assertEqual(node.var_type, TemplateConditionVariable.LOCAL)
        self.assertFalse(node.loop)
        self.assertIsNone(node.name)
        self.assertIsInstance(node.value, TemplateNode)
        self.assertFalse(node.is_default())
        self.assertEqual(len(node.children), 1)
        self.assertEqual(node.children[0].resolve(self._client_context), "B")

        node = template_node.children[2]
        self.assertIsInstance(node, TemplateConditionListItemNode)
        self.assertEqual(node.var_type, TemplateConditionVariable.LOCAL)
        self.assertFalse(node.loop)
        self.assertIsNone(node.name)
        self.assertIsInstance(node.value, TemplateNode)
        self.assertFalse(node.is_default())
        self.assertEqual(len(node.children), 1)
        self.assertEqual(node.children[0].resolve(self._client_context), "C")

        node = template_node.children[3]
        self.assertIsInstance(node, TemplateConditionListItemNode)
        self.assertEqual(node.var_type, TemplateConditionVariable.LOCAL)
        self.assertFalse(node.loop)
        self.assertIsNone(node.name)
        self.assertIsNone(node.value)
        self.assertTrue(node.is_default())
        self.assertEqual(len(node.children), 1)
        self.assertEqual(node.children[0].resolve(self._client_context), "D")

    def test_condition_template_single_bot_name_attr_value_attrs(self):
        template = ET.fromstring("""
            <template>
                <condition bot="aname">
                    <li value="a">A</li>
                    <li value="b">B</li>
                    <li><value>c</value>C</li>
                    <li>D</li>
                </condition>
            </template>
            """)
        ast = self._graph.parse_template_expression(template)
        self.assertIsNotNone(ast)
        self.assertIsInstance(ast, TemplateNode)
        self.assertIsNotNone(ast.children)

        template_node = ast.children[0]
        self.assertIsNotNone(template_node)
        self.assertIsInstance(template_node, TemplateConditionNode)
        self.assertEqual(template_node.var_type, TemplateConditionVariable.BOT)
        self.assertEqual(template_node.name, "aname")
        self.assertEqual(len(template_node.children), 4)

        node = template_node.children[0]
        self.assertIsInstance(node, TemplateConditionListItemNode)
        self.assertEqual(node.var_type, TemplateConditionVariable.BOT)
        self.assertFalse(node.loop)
        self.assertIsNone(node.name)
        self.assertIsInstance(node.value, TemplateNode)
        self.assertFalse(node.is_default())
        self.assertEqual(len(node.children), 1)
        self.assertEqual(node.children[0].resolve(self._client_context), "A")

        node = template_node.children[1]
        self.assertIsInstance(node, TemplateConditionListItemNode)
        self.assertEqual(node.var_type, TemplateConditionVariable.BOT)
        self.assertFalse(node.loop)
        self.assertIsNone(node.name)
        self.assertIsInstance(node.value, TemplateNode)
        self.assertFalse(node.is_default())
        self.assertEqual(len(node.children), 1)
        self.assertEqual(node.children[0].resolve(self._client_context), "B")

        node = template_node.children[2]
        self.assertIsInstance(node, TemplateConditionListItemNode)
        self.assertEqual(node.var_type, TemplateConditionVariable.BOT)
        self.assertFalse(node.loop)
        self.assertIsNone(node.name)
        self.assertIsInstance(node.value, TemplateNode)
        self.assertFalse(node.is_default())
        self.assertEqual(len(node.children), 1)
        self.assertEqual(node.children[0].resolve(self._client_context), "C")

        node = template_node.children[3]
        self.assertIsInstance(node, TemplateConditionListItemNode)
        self.assertEqual(node.var_type, TemplateConditionVariable.BOT)
        self.assertFalse(node.loop)
        self.assertIsNone(node.name)
        self.assertIsNone(node.value)
        self.assertTrue(node.is_default())
        self.assertEqual(len(node.children), 1)
        self.assertEqual(node.children[0].resolve(self._client_context), "D")

    ##################################################################################################################
    # Multiple
    #

    def test_condition_template_multi_global_name_value_mixed(self):
        template = ET.fromstring("""
			<template>
				<condition>
					<li name='name1' value="a">Val1</li>
					<li value="b"><name>name2</name>Val2</li>
					<li name="name3"><value>c</value>Val3</li>
					<li><name>name4</name><value>d</value>Val4</li>
					<li>Val5</li>
				</condition>
			</template>
			""")
        ast = self._graph.parse_template_expression(template)
        self.assertIsNotNone(ast)
        self.assertIsInstance(ast, TemplateNode)
        self.assertIsNotNone(ast.children)

        template_node = ast.children[0]

        self.assertIsNotNone(template_node)
        self.assertIsInstance(template_node, TemplateConditionNode)
        self.assertEqual(len(template_node.children), 5)

        node = template_node.children[0]
        self.assertIsInstance(node, TemplateConditionListItemNode)
        self.assertEqual(node.var_type, TemplateConditionVariable.GLOBAL)
        self.assertFalse(node.loop)
        self.assertIsNotNone(node.name)
        self.assertEqual(node.name, "name1")
        self.assertIsNotNone(node.value)
        self.assertIsInstance(node.value, TemplateNode)
        self.assertFalse(node.is_default())
        self.assertEqual(len(node.children), 1)
        self.assertEqual(node.children[0].resolve(self._client_context), "Val1")

        node = template_node.children[1]
        self.assertIsInstance(node, TemplateConditionListItemNode)
        self.assertEqual(node.var_type, TemplateConditionVariable.GLOBAL)
        self.assertFalse(node.loop)
        self.assertIsNotNone(node.name)
        self.assertEqual(node.name, "name2")
        self.assertIsNotNone(node.value)
        self.assertIsInstance(node.value, TemplateNode)
        self.assertFalse(node.is_default())
        self.assertEqual(len(node.children), 1)
        self.assertEqual(node.children[0].resolve(self._client_context), "Val2")

        node = template_node.children[2]
        self.assertIsInstance(node, TemplateConditionListItemNode)
        self.assertEqual(node.var_type, TemplateConditionVariable.GLOBAL)
        self.assertFalse(node.loop)
        self.assertIsNotNone(node.name)
        self.assertEqual(node.name, "name3")
        self.assertIsNotNone(node.value)
        self.assertIsInstance(node.value, TemplateNode)
        self.assertFalse(node.is_default())
        self.assertEqual(len(node.children), 1)
        self.assertEqual(node.children[0].resolve(self._client_context), "Val3")

        node = template_node.children[3]
        self.assertIsInstance(node, TemplateConditionListItemNode)
        self.assertEqual(node.var_type, TemplateConditionVariable.GLOBAL)
        self.assertFalse(node.loop)
        self.assertEqual(node.name, "name4")
        self.assertIsNotNone(node.value)
        self.assertIsInstance(node.value, TemplateNode)
        self.assertFalse(node.is_default())
        self.assertEqual(len(node.children), 1)
        self.assertEqual(node.children[0].resolve(self._client_context), "Val4")

        node = template_node.children[4]
        self.assertIsInstance(node, TemplateConditionListItemNode)
        self.assertEqual(node.var_type, TemplateConditionVariable.DEFAULT)
        self.assertFalse(node.loop)
        self.assertIsNone(node.name)
        self.assertIsNone(node.value)
        self.assertTrue(node.is_default())
        self.assertEqual(len(node.children), 1)
        self.assertEqual(node.children[0].resolve(self._client_context), "Val5")

    def test_condition_template_multi_global_name_value_mixed_loop(self):
        template = ET.fromstring("""
            <template>
                <condition>
                    <li name='name1' value="a">Val1 <loop /></li>
                    <li value="b"><name>name2</name>Val2</li>
                    <li name="name3"><value>c</value>Val3</li>
                    <li><name>name4</name><value>d</value>Val4</li>
                    <li>Val5</li>
                </condition>
            </template>
            """)
        ast = self._graph.parse_template_expression(template)
        self.assertIsNotNone(ast)
        self.assertIsInstance(ast, TemplateNode)
        self.assertIsNotNone(ast.children)

        template_node = ast.children[0]

        self.assertIsNotNone(template_node)
        self.assertIsInstance(template_node, TemplateConditionNode)
        self.assertEqual(len(template_node.children), 5)

        node = template_node.children[0]
        self.assertIsInstance(node, TemplateConditionListItemNode)
        self.assertEqual(node.var_type, TemplateConditionVariable.GLOBAL)
        self.assertTrue(node.loop)
        self.assertIsNotNone(node.name)
        self.assertEqual(node.name, "name1")
        self.assertIsNotNone(node.value)
        self.assertIsInstance(node.value, TemplateNode)
        self.assertFalse(node.is_default())
        self.assertEqual(len(node.children), 1)
        self.assertEqual(node.children[0].resolve(self._client_context), "Val1")

        node = template_node.children[1]
        self.assertIsInstance(node, TemplateConditionListItemNode)
        self.assertEqual(node.var_type, TemplateConditionVariable.GLOBAL)
        self.assertFalse(node.loop)
        self.assertIsNotNone(node.name)
        self.assertEqual(node.name, "name2")
        self.assertIsNotNone(node.value)
        self.assertIsInstance(node.value, TemplateNode)
        self.assertFalse(node.is_default())
        self.assertEqual(len(node.children), 1)
        self.assertEqual(node.children[0].resolve(self._client_context), "Val2")

        node = template_node.children[2]
        self.assertIsInstance(node, TemplateConditionListItemNode)
        self.assertEqual(node.var_type, TemplateConditionVariable.GLOBAL)
        self.assertFalse(node.loop)
        self.assertIsNotNone(node.name)
        self.assertEqual(node.name, "name3")
        self.assertIsNotNone(node.value)
        self.assertIsInstance(node.value, TemplateNode)
        self.assertFalse(node.is_default())
        self.assertEqual(len(node.children), 1)
        self.assertEqual(node.children[0].resolve(self._client_context), "Val3")

        node = template_node.children[3]
        self.assertIsInstance(node, TemplateConditionListItemNode)
        self.assertEqual(node.var_type, TemplateConditionVariable.GLOBAL)
        self.assertFalse(node.loop)
        self.assertEqual(node.name, "name4")
        self.assertIsNotNone(node.value)
        self.assertIsInstance(node.value, TemplateNode)
        self.assertFalse(node.is_default())
        self.assertEqual(len(node.children), 1)
        self.assertEqual(node.children[0].resolve(self._client_context), "Val4")

        node = template_node.children[4]
        self.assertIsInstance(node, TemplateConditionListItemNode)
        self.assertEqual(node.var_type, TemplateConditionVariable.DEFAULT)
        self.assertFalse(node.loop)
        self.assertIsNone(node.name)
        self.assertIsNone(node.value)
        self.assertTrue(node.is_default())
        self.assertEqual(len(node.children), 1)
        self.assertEqual(node.children[0].resolve(self._client_context), "Val5")

    def test_condition_template_multi_local_name_value_mixed(self):
        template = ET.fromstring("""
			<template>
				<condition>
					<li var='name1' value="a">Val1</li>
					<li value="b"><var>name2</var>Val2</li>
					<li var="name3"><value>c</value>Val3</li>
					<li><var>name4</var><value>d</value>Val4</li>
					<li>Val5</li>
				</condition>
			</template>
			""")
        ast = self._graph.parse_template_expression(template)
        self.assertIsNotNone(ast)
        self.assertIsInstance(ast, TemplateNode)
        self.assertIsNotNone(ast.children)

        template_node = ast.children[0]

        self.assertIsNotNone(template_node)
        self.assertIsInstance(template_node, TemplateConditionNode)
        self.assertEqual(len(template_node.children), 5)

        node = template_node.children[0]
        self.assertIsInstance(node, TemplateConditionListItemNode)
        self.assertEqual(node.var_type, TemplateConditionVariable.LOCAL)
        self.assertFalse(node.loop)
        self.assertIsNotNone(node.name)
        self.assertEqual(node.name, "name1")
        self.assertIsNotNone(node.value)
        self.assertIsInstance(node.value, TemplateNode)
        self.assertFalse(node.is_default())
        self.assertEqual(len(node.children), 1)
        self.assertEqual(node.children[0].resolve(self._client_context), "Val1")

        node = template_node.children[1]
        self.assertIsInstance(node, TemplateConditionListItemNode)
        self.assertEqual(node.var_type, TemplateConditionVariable.LOCAL)
        self.assertFalse(node.loop)
        self.assertIsNotNone(node.name)
        self.assertEqual(node.name, "name2")
        self.assertIsNotNone(node.value)
        self.assertIsInstance(node.value, TemplateNode)
        self.assertFalse(node.is_default())
        self.assertEqual(len(node.children), 1)
        self.assertEqual(node.children[0].resolve(self._client_context), "Val2")

        node = template_node.children[2]
        self.assertIsInstance(node, TemplateConditionListItemNode)
        self.assertEqual(node.var_type, TemplateConditionVariable.LOCAL)
        self.assertFalse(node.loop)
        self.assertIsNotNone(node.name)
        self.assertEqual(node.name, "name3")
        self.assertIsNotNone(node.value)
        self.assertIsInstance(node.value, TemplateNode)
        self.assertFalse(node.is_default())
        self.assertEqual(len(node.children), 1)
        self.assertEqual(node.children[0].resolve(self._client_context), "Val3")

        node = template_node.children[3]
        self.assertIsInstance(node, TemplateConditionListItemNode)
        self.assertEqual(node.var_type, TemplateConditionVariable.LOCAL)
        self.assertFalse(node.loop)
        self.assertEqual(node.name, "name4")
        self.assertIsNotNone(node.value)
        self.assertIsInstance(node.value, TemplateNode)
        self.assertFalse(node.is_default())
        self.assertEqual(len(node.children), 1)
        self.assertEqual(node.children[0].resolve(self._client_context), "Val4")

        node = template_node.children[4]
        self.assertIsInstance(node, TemplateConditionListItemNode)
        self.assertEqual(node.var_type, TemplateConditionVariable.DEFAULT)
        self.assertFalse(node.loop)
        self.assertIsNone(node.name)
        self.assertIsNone(node.value)
        self.assertTrue(node.is_default())
        self.assertEqual(len(node.children), 1)
        self.assertEqual(node.children[0].resolve(self._client_context), "Val5")

    def test_condition_template_multi_local_name_value_mixed_loop(self):
        template = ET.fromstring("""
            <template>
                <condition>
                    <li var='name1' value="a">Val1 <loop /></li>
                    <li value="b"><var>name2</var>Val2</li>
                    <li var="name3"><value>c</value>Val3</li>
                    <li><var>name4</var><value>d</value>Val4</li>
                    <li>Val5</li>
                </condition>
            </template>
            """)
        ast = self._graph.parse_template_expression(template)
        self.assertIsNotNone(ast)
        self.assertIsInstance(ast, TemplateNode)
        self.assertIsNotNone(ast.children)

        template_node = ast.children[0]

        self.assertIsNotNone(template_node)
        self.assertIsInstance(template_node, TemplateConditionNode)
        self.assertEqual(len(template_node.children), 5)

        node = template_node.children[0]
        self.assertIsInstance(node, TemplateConditionListItemNode)
        self.assertEqual(node.var_type, TemplateConditionVariable.LOCAL)
        self.assertTrue(node.loop)
        self.assertIsNotNone(node.name)
        self.assertEqual(node.name, "name1")
        self.assertIsNotNone(node.value)
        self.assertIsInstance(node.value, TemplateNode)
        self.assertFalse(node.is_default())
        self.assertEqual(len(node.children), 1)
        self.assertEqual(node.children[0].resolve(self._client_context), "Val1")

        node = template_node.children[1]
        self.assertIsInstance(node, TemplateConditionListItemNode)
        self.assertEqual(node.var_type, TemplateConditionVariable.LOCAL)
        self.assertFalse(node.loop)
        self.assertIsNotNone(node.name)
        self.assertEqual(node.name, "name2")
        self.assertIsNotNone(node.value)
        self.assertIsInstance(node.value, TemplateNode)
        self.assertFalse(node.is_default())
        self.assertEqual(len(node.children), 1)
        self.assertEqual(node.children[0].resolve(self._client_context), "Val2")

        node = template_node.children[2]
        self.assertIsInstance(node, TemplateConditionListItemNode)
        self.assertEqual(node.var_type, TemplateConditionVariable.LOCAL)
        self.assertFalse(node.loop)
        self.assertIsNotNone(node.name)
        self.assertEqual(node.name, "name3")
        self.assertIsNotNone(node.value)
        self.assertIsInstance(node.value, TemplateNode)
        self.assertFalse(node.is_default())
        self.assertEqual(len(node.children), 1)
        self.assertEqual(node.children[0].resolve(self._client_context), "Val3")

        node = template_node.children[3]
        self.assertIsInstance(node, TemplateConditionListItemNode)
        self.assertEqual(node.var_type, TemplateConditionVariable.LOCAL)
        self.assertFalse(node.loop)
        self.assertEqual(node.name, "name4")
        self.assertIsNotNone(node.value)
        self.assertIsInstance(node.value, TemplateNode)
        self.assertFalse(node.is_default())
        self.assertEqual(len(node.children), 1)
        self.assertEqual(node.children[0].resolve(self._client_context), "Val4")

        node = template_node.children[4]
        self.assertIsInstance(node, TemplateConditionListItemNode)
        self.assertEqual(node.var_type, TemplateConditionVariable.DEFAULT)
        self.assertFalse(node.loop)
        self.assertIsNone(node.name)
        self.assertIsNone(node.value)
        self.assertTrue(node.is_default())
        self.assertEqual(len(node.children), 1)
        self.assertEqual(node.children[0].resolve(self._client_context), "Val5")

    def test_condition_template_multi_bot_name_value_mixed(self):
        template = ET.fromstring("""
			<template>
				<condition>
					<li bot='name1' value="a">Val1</li>
					<li value="b"><bot>name2</bot>Val2</li>
					<li bot="name3"><value>c</value>Val3</li>
					<li><bot>name4</bot><value>d</value>Val4</li>
					<li>Val5</li>
				</condition>
			</template>
			""")
        ast = self._graph.parse_template_expression(template)
        self.assertIsNotNone(ast)
        self.assertIsInstance(ast, TemplateNode)
        self.assertIsNotNone(ast.children)

        template_node = ast.children[0]

        self.assertIsNotNone(template_node)
        self.assertIsInstance(template_node, TemplateConditionNode)
        self.assertEqual(len(template_node.children), 5)

        node = template_node.children[0]
        self.assertIsInstance(node, TemplateConditionListItemNode)
        self.assertEqual(node.var_type, TemplateConditionVariable.BOT)
        self.assertFalse(node.loop)
        self.assertIsNotNone(node.name)
        self.assertEqual(node.name, "name1")
        self.assertIsNotNone(node.value)
        self.assertIsInstance(node.value, TemplateNode)
        self.assertFalse(node.is_default())
        self.assertEqual(len(node.children), 1)
        self.assertEqual(node.children[0].resolve(self._client_context), "Val1")

        node = template_node.children[1]
        self.assertIsInstance(node, TemplateConditionListItemNode)
        self.assertEqual(node.var_type, TemplateConditionVariable.BOT)
        self.assertFalse(node.loop)
        self.assertIsNotNone(node.name)
        self.assertEqual(node.name, "name2")
        self.assertIsNotNone(node.value)
        self.assertIsInstance(node.value, TemplateNode)
        self.assertFalse(node.is_default())
        self.assertEqual(len(node.children), 1)
        self.assertEqual(node.children[0].resolve(self._client_context), "Val2")

        node = template_node.children[2]
        self.assertIsInstance(node, TemplateConditionListItemNode)
        self.assertEqual(node.var_type, TemplateConditionVariable.BOT)
        self.assertFalse(node.loop)
        self.assertIsNotNone(node.name)
        self.assertEqual(node.name, "name3")
        self.assertIsNotNone(node.value)
        self.assertIsInstance(node.value, TemplateNode)
        self.assertFalse(node.is_default())
        self.assertEqual(len(node.children), 1)
        self.assertEqual(node.children[0].resolve(self._client_context), "Val3")

        node = template_node.children[3]
        self.assertIsInstance(node, TemplateConditionListItemNode)
        self.assertEqual(node.var_type, TemplateConditionVariable.BOT)
        self.assertFalse(node.loop)
        self.assertEqual(node.name, "name4")
        self.assertIsNotNone(node.value)
        self.assertIsInstance(node.value, TemplateNode)
        self.assertFalse(node.is_default())
        self.assertEqual(len(node.children), 1)
        self.assertEqual(node.children[0].resolve(self._client_context), "Val4")

        node = template_node.children[4]
        self.assertIsInstance(node, TemplateConditionListItemNode)
        self.assertEqual(node.var_type, TemplateConditionVariable.DEFAULT)
        self.assertFalse(node.loop)
        self.assertIsNone(node.name)
        self.assertIsNone(node.value)
        self.assertTrue(node.is_default())
        self.assertEqual(len(node.children), 1)
        self.assertEqual(node.children[0].resolve(self._client_context), "Val5")

    def test_condition_template_multi_local_name_value_mixed_loop(self):
        template = ET.fromstring("""
            <template>
                <condition>
                    <li bot='name1' value="a">Val1 <loop /></li>
                    <li value="b"><bot>name2</bot>Val2</li>
                    <li bot="name3"><value>c</value>Val3</li>
                    <li><bot>name4</bot><value>d</value>Val4</li>
                    <li>Val5</li>
                </condition>
            </template>
            """)
        ast = self._graph.parse_template_expression(template)
        self.assertIsNotNone(ast)
        self.assertIsInstance(ast, TemplateNode)
        self.assertIsNotNone(ast.children)

        template_node = ast.children[0]

        self.assertIsNotNone(template_node)
        self.assertIsInstance(template_node, TemplateConditionNode)
        self.assertEqual(len(template_node.children), 5)

        node = template_node.children[0]
        self.assertIsInstance(node, TemplateConditionListItemNode)
        self.assertEqual(node.var_type, TemplateConditionVariable.BOT)
        self.assertTrue(node.loop)
        self.assertIsNotNone(node.name)
        self.assertEqual(node.name, "name1")
        self.assertIsNotNone(node.value)
        self.assertIsInstance(node.value, TemplateNode)
        self.assertFalse(node.is_default())
        self.assertEqual(len(node.children), 1)
        self.assertEqual(node.children[0].resolve(self._client_context), "Val1")

        node = template_node.children[1]
        self.assertIsInstance(node, TemplateConditionListItemNode)
        self.assertEqual(node.var_type, TemplateConditionVariable.BOT)
        self.assertFalse(node.loop)
        self.assertIsNotNone(node.name)
        self.assertEqual(node.name, "name2")
        self.assertIsNotNone(node.value)
        self.assertIsInstance(node.value, TemplateNode)
        self.assertFalse(node.is_default())
        self.assertEqual(len(node.children), 1)
        self.assertEqual(node.children[0].resolve(self._client_context), "Val2")

        node = template_node.children[2]
        self.assertIsInstance(node, TemplateConditionListItemNode)
        self.assertEqual(node.var_type, TemplateConditionVariable.BOT)
        self.assertFalse(node.loop)
        self.assertIsNotNone(node.name)
        self.assertEqual(node.name, "name3")
        self.assertIsNotNone(node.value)
        self.assertIsInstance(node.value, TemplateNode)
        self.assertFalse(node.is_default())
        self.assertEqual(len(node.children), 1)
        self.assertEqual(node.children[0].resolve(self._client_context), "Val3")

        node = template_node.children[3]
        self.assertIsInstance(node, TemplateConditionListItemNode)
        self.assertEqual(node.var_type, TemplateConditionVariable.BOT)
        self.assertFalse(node.loop)
        self.assertEqual(node.name, "name4")
        self.assertIsNotNone(node.value)
        self.assertIsInstance(node.value, TemplateNode)
        self.assertFalse(node.is_default())
        self.assertEqual(len(node.children), 1)
        self.assertEqual(node.children[0].resolve(self._client_context), "Val4")

        node = template_node.children[4]
        self.assertIsInstance(node, TemplateConditionListItemNode)
        self.assertEqual(node.var_type, TemplateConditionVariable.DEFAULT)
        self.assertFalse(node.loop)
        self.assertIsNone(node.name)
        self.assertIsNone(node.value)
        self.assertTrue(node.is_default())
        self.assertEqual(len(node.children), 1)
        self.assertEqual(node.children[0].resolve(self._client_context), "Val5")
