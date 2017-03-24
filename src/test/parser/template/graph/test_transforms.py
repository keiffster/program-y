import unittest
import xml.etree.ElementTree as ET


from test.parser.template.graph.test_graph_client import TemplateGraphTestClient


class TemplateGraphTransformsTests(TemplateGraphTestClient):

    def test_lowercase(self):
        template = ET.fromstring("""
            <template>
                <lowercase>This is a Sentence</lowercase>
            </template>
            """)
        ast = self.parser.parse_template_expression(template)
        self.assertIsNotNone(ast)
        self.assertEqual(ast.resolve(None, None), "this is a sentence")

    def test_uppercase(self):
        template = ET.fromstring("""
            <template>
                <uppercase>This is a Sentence</uppercase>
            </template>
            """)
        ast = self.parser.parse_template_expression(template)
        self.assertIsNotNone(ast)
        self.assertEqual(ast.resolve(None, None), "THIS IS A SENTENCE")

    def test_formal(self):
        template = ET.fromstring("""
            <template>
                <formal>This is a Sentence</formal>
            </template>
            """)
        ast = self.parser.parse_template_expression(template)
        self.assertIsNotNone(ast)
        self.assertEqual(ast.resolve(None, None), "This Is A Sentence")

    def test_sentence(self):
        template = ET.fromstring("""
            <template>
                <sentence>This is a Sentence</sentence>
            </template>
            """)
        ast = self.parser.parse_template_expression(template)
        self.assertIsNotNone(ast)
        self.assertEqual(ast.resolve(None, None), "This is a sentence")

    def test_normalize(self):
        template = ET.fromstring("""
			<template>
				<normalize>XYZ</normalize>
			</template>
			""")
        ast = self.parser.parse_template_expression(template)

    def test_denormalize(self):
        template = ET.fromstring("""
			<template>
				<denormalize>XYZ</denormalize>
			</template>
			""")
        ast = self.parser.parse_template_expression(template)

    def test_person(self):
        template = ET.fromstring("""
			<template>
				<person>XYZ</person>
			</template>
			""")
        ast = self.parser.parse_template_expression(template)

    def test_person2(self):
        template = ET.fromstring("""
			<template>
				<person2>XYZ</person2>
			</template>
			""")
        ast = self.parser.parse_template_expression(template)

    def test_gender(self):
        template = ET.fromstring("""
			<template>
				<gender>XYZ</gender>
			</template>
			""")
        ast = self.parser.parse_template_expression(template)

    def test_sr(self):
        template = ET.fromstring("""
			<template>
				<sr>XYZ</sr>
			</template>
			""")
        ast = self.parser.parse_template_expression(template)

    def test_id(self):
        template = ET.fromstring("""
			<template>
				<id />
			</template>
			""")
        ast = self.parser.parse_template_expression(template)
        self.assertIsNotNone(ast)
        self.assertEqual(ast.resolve(None, "clientid"), "clientid")

    def test_vocabulary(self):
        template = ET.fromstring("""
			<template>
				<vocabulary>XYZ</vocabulary>
			</template>
			""")
        ast = self.parser.parse_template_expression(template)

    def test_program(self):
        template = ET.fromstring("""
			<template>
				<program>XYZ</program>
			</template>
			""")
        ast = self.parser.parse_template_expression(template)

    def test_explode(self):
        template = ET.fromstring("""
			<template>
				<explode>XYZ</explode>
			</template>
			""")
        ast = self.parser.parse_template_expression(template)
        self.assertIsNotNone(ast)
        self.assertEqual(ast.resolve(None, None), "X Y Z")

    def test_implode(self):
        template = ET.fromstring("""
			<template>
				<implode>X Y Z</implode>
			</template>
			""")
        ast = self.parser.parse_template_expression(template)
        self.assertIsNotNone(ast)
        self.assertEqual(ast.resolve(None, None), "XYZ")

if __name__ == '__main__':
    unittest.main()
