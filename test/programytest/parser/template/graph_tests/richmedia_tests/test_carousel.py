import xml.etree.ElementTree as ET

from programy.parser.template.nodes.base import TemplateNode
from programy.parser.template.nodes.richmedia.carousel import TemplateCarouselNode
from programy.parser.template.nodes.richmedia.card import TemplateCardNode

from programytest.parser.template.graph_tests.graph_test_client import TemplateGraphTestClient


class TemplateGraphCarouselTests(TemplateGraphTestClient):

    def test_carousel_node_from_xml(self):
        template = ET.fromstring("""
			<template>
			    <carousel>
                    <card>
                        <image>http://www.servusai.com/aiml.png</image>
                        <title>Servusai.com</title>
                        <subtitle>The home of ProgramY</subtitle>
                        <button>
                            <text>Servusai.com</text>
                            <url>http://www.servusai.com</url>
                        </button>
                        <button>
                            <text>ProgramY</text>
                            <url>http://github.io/keiffster</url>
                        </button>
                    </card>
                </carousel>
			</template>
			""")
        root = self._graph.parse_template_expression(template)
        self.assertIsNotNone(root)
        self.assertIsInstance(root, TemplateNode)
        self.assertIsNotNone(root.children)
        self.assertEqual(len(root.children), 1)

        node = root.children[0]
        self.assertIsNotNone(node)
        self.assertIsInstance(node, TemplateCarouselNode)

        self.assertEqual(1, len(node._cards))