import unittest
import os

from programy.parser.template.factory import TemplateNodeFactory
from programy.parser.template.nodes.word import TemplateWordNode
from programy.parser.template.nodes.rand import TemplateRandomNode
from programy.parser.template.nodes.condition import TemplateConditionNode
from programy.parser.template.nodes.srai import TemplateSRAINode
from programy.parser.template.nodes.sraix import TemplateSRAIXNode
from programy.parser.template.nodes.get import TemplateGetNode
from programy.parser.template.nodes.set import TemplateSetNode
from programy.parser.template.nodes.map import TemplateMapNode
from programy.parser.template.nodes.bot import TemplateBotNode
from programy.parser.template.nodes.think import TemplateThinkNode
from programy.parser.template.nodes.normalise import TemplateNormalizeNode
from programy.parser.template.nodes.denormalise import TemplateDenormalizeNode
from programy.parser.template.nodes.person import TemplatePersonNode
from programy.parser.template.nodes.person2 import TemplatePerson2Node
from programy.parser.template.nodes.gender import TemplateGenderNode
from programy.parser.template.nodes.sr import TemplateSrNode
from programy.parser.template.nodes.id import TemplateIdNode
from programy.parser.template.nodes.size import TemplateSizeNode
from programy.parser.template.nodes.vocabulary import TemplateVocabularyNode
from programy.parser.template.nodes.eval import TemplateEvalNode
from programy.parser.template.nodes.explode import TemplateExplodeNode
from programy.parser.template.nodes.implode import TemplateImplodeNode
from programy.parser.template.nodes.program import TemplateProgramNode
from programy.parser.template.nodes.lowercase import TemplateLowercaseNode
from programy.parser.template.nodes.uppercase import TemplateUppercaseNode
from programy.parser.template.nodes.sentence import TemplateSentenceNode
from programy.parser.template.nodes.formal import TemplateFormalNode
from programy.parser.template.nodes.that import TemplateThatNode
from programy.parser.template.nodes.thatstar import TemplateThatStarNode
from programy.parser.template.nodes.topicstar import TemplateTopicStarNode
from programy.parser.template.nodes.star import TemplateStarNode
from programy.parser.template.nodes.input import TemplateInputNode
from programy.parser.template.nodes.request import TemplateRequestNode
from programy.parser.template.nodes.response import TemplateResponseNode
from programy.parser.template.nodes.date import TemplateDateNode
from programy.parser.template.nodes.interval import TemplateIntervalNode
from programy.parser.template.nodes.system import TemplateSystemNode
from programy.parser.template.nodes.extension import TemplateExtensionNode
from programy.parser.template.nodes.learn import TemplateLearnNode
from programy.parser.template.nodes.learnf import TemplateLearnfNode
from programy.parser.template.nodes.first import TemplateFirstNode
from programy.parser.template.nodes.rest import TemplateRestNode
from programy.parser.template.nodes.log import TemplateLogNode

class TemplateFactoryTests(unittest.TestCase):

    def test_init(self):
        factory = TemplateNodeFactory()
        self.assertIsNotNone(factory)
        self.assertEqual({}, factory._nodes_config)
        self.assertEqual("Template", factory._type)

    def assert_node(self, factory, name, cls, *args):
        self.assertTrue(name in factory._nodes_config)
        instance = factory._nodes_config[name]
        if len(args) == 1 :
            if args[0] is None:
                new_node = instance()
            else:
                new_node = instance(args[0])
        elif len(args) == 2 :
            new_node = instance(args[0], args[1])
        self.assertIsInstance(new_node, cls)

    def assert_nodes(self, factory):
        self.assertEqual(66, len(factory._nodes_config))

        self.assert_node(factory, 'random', TemplateRandomNode, None)
        self.assert_node(factory, 'condition', TemplateConditionNode, "name", "value")
        self.assert_node(factory, 'srai', TemplateSRAINode, None)
        self.assert_node(factory, 'sraix', TemplateSRAIXNode, None)
        self.assert_node(factory, 'get', TemplateGetNode, None)
        self.assert_node(factory, 'set', TemplateSetNode, None)
        self.assert_node(factory, 'map', TemplateMapNode, None)
        self.assert_node(factory, 'bot', TemplateBotNode, None)
        self.assert_node(factory, 'think', TemplateThinkNode, None)
        self.assert_node(factory, 'normalize', TemplateNormalizeNode, None)
        self.assert_node(factory, 'denormalize', TemplateDenormalizeNode, None)
        self.assert_node(factory, 'person', TemplatePersonNode, None)
        self.assert_node(factory, 'person2', TemplatePerson2Node, None)
        self.assert_node(factory, 'gender', TemplateGenderNode, None)
        self.assert_node(factory, 'sr', TemplateSrNode, None)
        self.assert_node(factory, 'id', TemplateIdNode, None)
        self.assert_node(factory, 'size', TemplateSizeNode, None)
        self.assert_node(factory, 'vocabulary', TemplateVocabularyNode, None)
        self.assert_node(factory, 'eval', TemplateEvalNode, None)
        self.assert_node(factory, 'explode', TemplateExplodeNode, None)
        self.assert_node(factory, 'implode', TemplateImplodeNode, None)
        self.assert_node(factory, 'program', TemplateProgramNode, None)
        self.assert_node(factory, 'lowercase', TemplateLowercaseNode, None)
        self.assert_node(factory, 'uppercase', TemplateUppercaseNode, None)
        self.assert_node(factory, 'sentence', TemplateSentenceNode, None)
        self.assert_node(factory, 'formal', TemplateFormalNode, None)
        self.assert_node(factory, 'that', TemplateThatNode, None)
        self.assert_node(factory, 'thatstar', TemplateThatStarNode, None)
        self.assert_node(factory, 'topicstar', TemplateTopicStarNode, None)
        self.assert_node(factory, 'star', TemplateStarNode, None)
        self.assert_node(factory, 'input', TemplateInputNode, None)
        self.assert_node(factory, 'request', TemplateRequestNode, None)
        self.assert_node(factory, 'response', TemplateResponseNode, None)
        self.assert_node(factory, 'date', TemplateDateNode, None)
        self.assert_node(factory, 'interval', TemplateIntervalNode, None)
        self.assert_node(factory, 'system', TemplateSystemNode, None)
        self.assert_node(factory, 'extension', TemplateExtensionNode, None)
        self.assert_node(factory, 'learn', TemplateLearnNode, None)
        self.assert_node(factory, 'learnf', TemplateLearnfNode, None)
        self.assert_node(factory, 'first', TemplateFirstNode, None)
        self.assert_node(factory, 'rest', TemplateRestNode, None)
        self.assert_node(factory, 'log', TemplateLogNode, None)

