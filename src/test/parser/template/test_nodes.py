import xml.etree.ElementTree as ET

from programy.parser.template.nodes import *
from programy.bot import Bot
from programy.brain import Brain
from programy.dialog import Conversation, Question

from test.parser.template.base import TemplateTestsBaseClass
from programy.config import BrainConfiguration, BotConfiguration

######################################################################################################################
#
class TemplateNodeBasicTests(TemplateTestsBaseClass):

    def test_node(self):
        root = TemplateNode()
        self.assertIsNotNone(root)
        self.assertIsNotNone(root.children)
        self.assertEqual(len(root.children), 0)

######################################################################################################################
#
class TemplateWordNodeTests(TemplateTestsBaseClass):

    def test_node(self):
        root = TemplateNode()
        self.assertIsNotNone(root)
        self.assertIsNotNone(root.children)
        self.assertEqual(len(root.children), 0)

        root.append(TemplateWordNode("Hello"))
        root.append(TemplateWordNode("World!"))
        self.assertEqual(len(root.children), 2)

        resolved = root.resolve(self.bot, self.clientid)
        self.assertIsNotNone(resolved)
        self.assertEqual(resolved, "Hello World!")

######################################################################################################################
#
class TemplateRandomNodeTests(TemplateTestsBaseClass):

    def test_node(self):
        root = TemplateNode()
        self.assertIsNotNone(root)
        self.assertIsNotNone(root.children)
        self.assertEqual(len(root.children), 0)

        random1 = TemplateRandomNode()
        random1.append(TemplateWordNode("Test1"))
        random1.append(TemplateWordNode("Test2"))
        random1.append(TemplateWordNode("Test3"))
        self.assertEqual(len(random1.children), 3)

        root.append(random1)

        resolved = root.resolve(self.bot, self.clientid)
        self.assertIsNotNone(resolved)
        self.assertOneOf(resolved, ["Test1", "Test2", "Test3"])

######################################################################################################################
#
class TemplateSRAINodeTests(TemplateTestsBaseClass):

    def test_node(self):
        root = TemplateNode()
        self.assertIsNotNone(root)
        self.assertIsNotNone(root.children)
        self.assertEqual(len(root.children), 0)

        node = TemplateSRAINode()
        self.assertIsNotNone(node)

        root.append(node)
        self.assertEqual(len(root.children), 1)

        node.append(TemplateWordNode("Hello"))
        self.assertEqual(len(node.children), 1)

        self.bot.response = "Hiya"
        self.assertEqual(root.resolve(self.bot, self.clientid), "Hiya")

######################################################################################################################
#
class TemplateSrNodeTests(TemplateTestsBaseClass):

    def test_node(self):
        root = TemplateNode()
        self.assertIsNotNone(root)
        self.assertIsNotNone(root.children)
        self.assertEqual(len(root.children), 0)

        node = TemplateSrNode()
        self.assertIsNotNone(node)

        root.append(node)
        self.assertEqual(len(root.children), 1)


######################################################################################################################
#
class TemplateIndexedNodeTests(TemplateTestsBaseClass):

    def test_node(self):
        root = TemplateNode()
        self.assertIsNotNone(root)
        self.assertIsNotNone(root.children)
        self.assertEqual(len(root.children), 0)

        node = TemplateIndexedNode()
        self.assertIsNotNone(node)

        root.append(node)
        self.assertEqual(len(root.children), 1)

######################################################################################################################
#
class TemplateStarNodeTests(TemplateTestsBaseClass):

    def test_node(self):
        root = TemplateNode()
        self.assertIsNotNone(root)
        self.assertIsNotNone(root.children)
        self.assertEqual(len(root.children), 0)

        node = TemplateStarNode()
        self.assertIsNotNone(node)

        root.append(node)
        self.assertEqual(len(root.children), 1)


######################################################################################################################
#
class TemplateGetNodeTests(TemplateTestsBaseClass):

    def test_local_get(self):
        root = TemplateNode()
        self.assertIsNotNone(root)
        self.assertIsNotNone(root.children)
        self.assertEqual(len(root.children), 0)

        node = TemplateGetNode()
        node.name = TemplateWordNode("name")
        node.local = True
        node.append(TemplateWordNode("Fred"))
        self.assertIsNotNone(node)

        root.append(node)
        self.assertEqual(len(root.children), 1)

        conversation = self.bot.get_conversation(self.clientid)
        self.assertIsNotNone(conversation)
        question = Question.create_from_text("Hello")
        conversation.record_dialog(question)
        self.assertIsNotNone(conversation.current_question())
        question.current_sentence().set_predicate("name", "keith")

        result = root.resolve(self.bot, self.clientid)
        self.assertIsNotNone(result)
        self.assertEqual("keith", result)

    def test_local_no_value(self):
        root = TemplateNode()
        self.assertIsNotNone(root)
        self.assertIsNotNone(root.children)
        self.assertEqual(len(root.children), 0)

        node = TemplateGetNode()
        node.name = TemplateWordNode("name")
        node.local = True
        node.append(TemplateWordNode("Fred"))
        self.assertIsNotNone(node)

        root.append(node)
        self.assertEqual(len(root.children), 1)

        self.bot.brain.properties.add_property("default-get", "unknown")

        conversation = self.bot.get_conversation(self.clientid)
        self.assertIsNotNone(conversation)
        question = Question.create_from_text("Hello")
        conversation.record_dialog(question)

        result = root.resolve(self.bot, self.clientid)
        self.assertIsNotNone(result)
        self.assertEqual("unknown", result)

    def test_global_get(self):
        root = TemplateNode()
        self.assertIsNotNone(root)
        self.assertIsNotNone(root.children)
        self.assertEqual(len(root.children), 0)

        node = TemplateGetNode()
        node.name = TemplateWordNode("name")
        node.local = False
        node.append(TemplateWordNode("Fred"))
        self.assertIsNotNone(node)

        root.append(node)
        self.assertEqual(len(root.children), 1)

        conversation = self.bot.get_conversation(self.clientid)
        self.assertIsNotNone(conversation)
        question = Question.create_from_text("Hello")
        conversation.record_dialog(question)
        self.assertIsNotNone(conversation.current_question())
        conversation.set_predicate("name", "keith")

        result = root.resolve(self.bot, self.clientid)
        self.assertIsNotNone(result)
        self.assertEqual("keith", result)

    def test_global_get_no_value(self):
        root = TemplateNode()
        self.assertIsNotNone(root)
        self.assertIsNotNone(root.children)
        self.assertEqual(len(root.children), 0)

        node = TemplateGetNode()
        node.name = TemplateWordNode("name")
        node.local = False
        node.append(TemplateWordNode("Fred"))
        self.assertIsNotNone(node)

        root.append(node)
        self.assertEqual(len(root.children), 1)

        self.bot.brain.properties.add_property("default-get", "unknown")

        result = root.resolve(self.bot, self.clientid)
        self.assertIsNotNone(result)
        self.assertEqual("unknown", result)

######################################################################################################################
#
class TemplateSetNodeTests(TemplateTestsBaseClass):

    def test_local_set(self):
        root = TemplateNode()
        self.assertIsNotNone(root)
        self.assertIsNotNone(root.children)
        self.assertEqual(len(root.children), 0)

        node = TemplateSetNode()
        self.assertIsNotNone(node)
        node.name = TemplateWordNode("name")
        node.local = True
        node.append(TemplateWordNode("keith"))

        root.append(node)
        self.assertEqual(len(root.children), 1)

        conversation = self.bot.get_conversation(self.clientid)
        self.assertIsNotNone(conversation)
        question = Question.create_from_text("Hello")
        conversation.record_dialog(question)
        self.assertIsNotNone(conversation.current_question())

        result = node.resolve(self.bot, self.clientid)
        self.assertIsNotNone(result)
        self.assertEqual("keith", result)

        self.assertEqual("keith", question.current_sentence().predicate("name"))

    def test_global_set(self):
        root = TemplateNode()
        self.assertIsNotNone(root)
        self.assertIsNotNone(root.children)
        self.assertEqual(len(root.children), 0)

        node = TemplateSetNode()
        self.assertIsNotNone(node)
        node.name = TemplateWordNode("name")
        node.local = False
        node.append(TemplateWordNode("keith"))

        root.append(node)
        self.assertEqual(len(root.children), 1)

        conversation = self.bot.get_conversation(self.clientid)
        self.assertIsNotNone(conversation)
        question = Question.create_from_text("Hello")
        conversation.record_dialog(question)
        self.assertIsNotNone(conversation.current_question())

        result = node.resolve(self.bot, self.clientid)
        self.assertIsNotNone(result)
        self.assertEqual("keith", result)

        self.assertEqual("keith", conversation.predicate("name"))

######################################################################################################################
#
class TemplateBotNodeTests(TemplateTestsBaseClass):

    def test_node(self):
        root = TemplateNode()
        self.assertIsNotNone(root)
        self.assertIsNotNone(root.children)
        self.assertEqual(len(root.children), 0)

        node = TemplateBotNode()
        self.assertIsNotNone(node)
        node.name = TemplateWordNode("location")
        root.append(node)
        self.assertEqual(len(root.children), 1)

        self.bot.brain.properties.add_property("location", "Scotland")

        result = node.resolve(self.bot, self.clientid)
        self.assertIsNotNone(result)
        self.assertEqual("Scotland", result)

    def test_node_no_value(self):
        root = TemplateNode()
        self.assertIsNotNone(root)
        self.assertIsNotNone(root.children)
        self.assertEqual(len(root.children), 0)

        node = TemplateBotNode()
        self.assertIsNotNone(node)
        node.name = TemplateWordNode("location")
        root.append(node)
        self.assertEqual(len(root.children), 1)

        self.bot.brain.properties.add_property("default-property", "unknown")

        result = node.resolve(self.bot, self.clientid)
        self.assertIsNotNone(result)
        self.assertEqual("unknown", result)


######################################################################################################################
#
class TemplateConditionNodeTests(TemplateTestsBaseClass):

    def test_node(self):
        root = TemplateNode()
        self.assertIsNotNone(root)
        self.assertIsNotNone(root.children)
        self.assertEqual(len(root.children), 0)

        node = TemplateConditionNode()
        self.assertIsNotNone(node)

        root.append(node)
        self.assertEqual(len(root.children), 1)


class TemplateType1ConditionNodeTests(TemplateTestsBaseClass):

    def test_node(self):
        root = TemplateNode()
        self.assertIsNotNone(root)
        self.assertIsNotNone(root.children)
        self.assertEqual(len(root.children), 0)

        node = TemplateType1ConditionNode()
        self.assertIsNotNone(node)

        root.append(node)
        self.assertEqual(len(root.children), 1)


class TemplateType2ConditionNodeTests(TemplateTestsBaseClass):

    def test_node(self):
        root = TemplateNode()
        self.assertIsNotNone(root)
        self.assertIsNotNone(root.children)
        self.assertEqual(len(root.children), 0)

        node = TemplateType2ConditionNode()
        self.assertIsNotNone(node)

        root.append(node)
        self.assertEqual(len(root.children), 1)


class TemplateType3ConditionNodeTests(TemplateTestsBaseClass):

    def test_node(self):
        root = TemplateNode()
        self.assertIsNotNone(root)
        self.assertIsNotNone(root.children)
        self.assertEqual(len(root.children), 0)

        node = TemplateType3ConditionNode()
        self.assertIsNotNone(node)

        root.append(node)
        self.assertEqual(len(root.children), 1)


class TemplateConditionListItemNodeTests(TemplateTestsBaseClass):

    def test_node(self):
        root = TemplateNode()
        self.assertIsNotNone(root)
        self.assertIsNotNone(root.children)
        self.assertEqual(len(root.children), 0)

        node = TemplateConditionListItemNode()
        self.assertIsNotNone(node)

        root.append(node)
        self.assertEqual(len(root.children), 1)


######################################################################################################################
#
class TemplateSRAIXNodeTests(TemplateTestsBaseClass):

    def test_node(self):
        root = TemplateNode()
        self.assertIsNotNone(root)
        self.assertIsNotNone(root.children)
        self.assertEqual(len(root.children), 0)

        node = TemplateSRAIXNode()
        self.assertIsNotNone(node)

        root.append(node)
        self.assertEqual(len(root.children), 1)

######################################################################################################################
#
class TemplateMapNodeTests(TemplateTestsBaseClass):

    def test_node(self):
        root = TemplateNode()
        self.assertIsNotNone(root)
        self.assertIsNotNone(root.children)
        self.assertEqual(len(root.children), 0)

        node = TemplateMapNode()
        self.assertIsNotNone(node)

        root.append(node)
        self.assertEqual(len(root.children), 1)


######################################################################################################################
#
class TemplateThinkNodeTests(TemplateTestsBaseClass):

    def test_node(self):
        root = TemplateNode()
        self.assertIsNotNone(root)
        self.assertIsNotNone(root.children)
        self.assertEqual(len(root.children), 0)

        node = TemplateThinkNode()
        self.assertIsNotNone(node)

        root.append(node)
        self.assertEqual(len(root.children), 1)


######################################################################################################################
#
class TemplateLowercaseNodeTests(TemplateTestsBaseClass):

    def test_node(self):
        root = TemplateNode()
        self.assertIsNotNone(root)
        self.assertIsNotNone(root.children)
        self.assertEqual(len(root.children), 0)

        node = TemplateLowercaseNode()
        self.assertIsNotNone(node)

        root.append(node)
        self.assertEqual(len(root.children), 1)

        word = TemplateWordNode("This is a Sentence")
        node.append(word)

        self.assertEqual(root.resolve(self.bot, self.clientid), "this is a sentence")

######################################################################################################################
#
class TemplateUppercaseNodeTests(TemplateTestsBaseClass):

    def test_node(self):
        root = TemplateNode()
        self.assertIsNotNone(root)
        self.assertIsNotNone(root.children)
        self.assertEqual(len(root.children), 0)

        node = TemplateUppercaseNode()
        self.assertIsNotNone(node)

        root.append(node)
        self.assertEqual(len(root.children), 1)

        word = TemplateWordNode("This is a Sentence")
        node.append(word)

        self.assertEqual(root.resolve(self.bot, self.clientid), "THIS IS A SENTENCE")


######################################################################################################################
#
class TemplateFormalNodeTests(TemplateTestsBaseClass):

    def test_node(self):
        root = TemplateNode()
        self.assertIsNotNone(root)
        self.assertIsNotNone(root.children)
        self.assertEqual(len(root.children), 0)

        node = TemplateFormalNode()
        self.assertIsNotNone(node)

        root.append(node)
        self.assertEqual(len(root.children), 1)

        word = TemplateWordNode("This is a Sentence")
        node.append(word)

        self.assertEqual(root.resolve(self.bot, self.clientid), "This Is A Sentence")


######################################################################################################################
#
class TemplateSentenceNodeTests(TemplateTestsBaseClass):

    def test_node(self):
        root = TemplateNode()
        self.assertIsNotNone(root)
        self.assertIsNotNone(root.children)
        self.assertEqual(len(root.children), 0)

        node = TemplateSentenceNode()
        self.assertIsNotNone(node)

        root.append(node)
        self.assertEqual(len(root.children), 1)

        word = TemplateWordNode("this is a sentence")
        node.append(word)

        self.assertEqual(root.resolve(self.bot, self.clientid), "This is a sentence")


######################################################################################################################
#
class TemplateNormalizeNodeTests(TemplateTestsBaseClass):

    def test_node(self):
        root = TemplateNode()
        self.assertIsNotNone(root)
        self.assertIsNotNone(root.children)
        self.assertEqual(len(root.children), 0)

        node = TemplateNormalizeNode()
        self.assertIsNotNone(node)

        root.append(node)
        self.assertEqual(len(root.children), 1)

        node.append(TemplateWordNode(" shouldnt "))
        self.bot.brain.normals.process_splits([" shouldnt "," should not "])

        self.assertEqual(root.resolve(self.bot, self.clientid), "should not")


######################################################################################################################
#
class TemplateDenormalizeNodeTests(TemplateTestsBaseClass):

    def test_node(self):
        root = TemplateNode()
        self.assertIsNotNone(root)
        self.assertIsNotNone(root.children)
        self.assertEqual(len(root.children), 0)

        node = TemplateDenormalizeNode()
        self.assertIsNotNone(node)

        root.append(node)
        self.assertEqual(len(root.children), 1)

        node.append(TemplateWordNode(" dot uk "))
        self.bot.brain.denormals.process_splits([" dot uk ",".uk"])

        self.assertEqual(root.resolve(self.bot, self.clientid), ".uk")


######################################################################################################################
#
class TemplatePersonNodeTests(TemplateTestsBaseClass):

    def test_node(self):
        root = TemplateNode()
        self.assertIsNotNone(root)
        self.assertIsNotNone(root.children)
        self.assertEqual(len(root.children), 0)

        node = TemplatePersonNode()
        self.assertIsNotNone(node)

        root.append(node)
        self.assertEqual(len(root.children), 1)

        node.append(TemplateWordNode(" me "))
        self.bot.brain.persons.process_splits([" me "," you "])

        self.assertEqual(root.resolve(self.bot, self.clientid), "you")

######################################################################################################################
#
class TemplatePerson2NodeTests(TemplateTestsBaseClass):

    def test_node(self):
        root = TemplateNode()
        self.assertIsNotNone(root)
        self.assertIsNotNone(root.children)
        self.assertEqual(len(root.children), 0)

        node = TemplatePerson2Node()
        self.assertIsNotNone(node)

        root.append(node)
        self.assertEqual(len(root.children), 1)

        node.append(TemplateWordNode(" me "))
        self.bot.brain.person2s.process_splits([" me "," him or her "])

        self.assertEqual(root.resolve(self.bot, self.clientid), "him or her")


######################################################################################################################
#
class TemplateGenderNodeTests(TemplateTestsBaseClass):

    def test_node(self):
        root = TemplateNode()
        self.assertIsNotNone(root)
        self.assertIsNotNone(root.children)
        self.assertEqual(len(root.children), 0)

        node = TemplateGenderNode()
        self.assertIsNotNone(node)

        root.append(node)
        self.assertEqual(len(root.children), 1)

        node.append(TemplateWordNode(" to him "))
        self.bot.brain.genders.process_splits([" to him "," to her "])

        self.assertEqual(root.resolve(self.bot, self.clientid), "to her")


######################################################################################################################
#
class TemplateIdNodeTests(TemplateTestsBaseClass):

    def test_node(self):
        root = TemplateNode()
        self.assertIsNotNone(root)
        self.assertIsNotNone(root.children)
        self.assertEqual(len(root.children), 0)

        node = TemplateIdNode()
        self.assertIsNotNone(node)

        root.append(node)
        self.assertEqual(len(root.children), 1)

        self.assertEqual(root.resolve(None, "clientid"), "clientid")


######################################################################################################################
#
class TemplateVocabularyNodeTests(TemplateTestsBaseClass):

    def test_node(self):
        test_bot = Bot(Brain(BrainConfiguration()), BotConfiguration())

        topic_element = ET.fromstring('<topic>*</topic>')
        that_element = ET.fromstring('<that>*</that>')
        pattern_element = ET.fromstring("<pattern>hello world</pattern>")
        test_bot.brain._aiml_parser.pattern_parser.add_pattern_to_graph(pattern_element, topic_element, that_element, None)

        test_bot.brain._sets_collection.add_set("testset", ["val1", "val2", "val3"])

        root = TemplateNode()
        self.assertIsNotNone(root)
        self.assertIsNotNone(root.children)
        self.assertEqual(len(root.children), 0)

        node = TemplateVocabularyNode()
        self.assertIsNotNone(node)

        root.append(node)
        self.assertEqual(len(root.children), 1)

        self.assertEquals(root.resolve(test_bot, "testid"), '5')


######################################################################################################################
#
class TemplateProgramNodeTests(TemplateTestsBaseClass):

    def test_node(self):
        test_bot = Bot(Brain(BrainConfiguration()), BotConfiguration())

        root = TemplateNode()
        self.assertIsNotNone(root)
        self.assertIsNotNone(root.children)
        self.assertEqual(len(root.children), 0)

        node = TemplateProgramNode()
        self.assertIsNotNone(node)

        root.append(node)
        self.assertEqual(len(root.children), 1)

        test_bot.brain.properties.add_property("fullname", "testbot")
        test_bot.brain.properties.add_property("version", "1.0.0")

        self.assertEqual(root.resolve(test_bot, "testid"), "testbot 1.0.0")


######################################################################################################################
#
class TemplateExplodeNodeTests(TemplateTestsBaseClass):

    def test_node(self):
        root = TemplateNode()
        self.assertIsNotNone(root)
        self.assertIsNotNone(root.children)
        self.assertEqual(len(root.children), 0)

        node = TemplateExplodeNode()
        self.assertIsNotNone(node)

        root.append(node)
        self.assertEqual(len(root.children), 1)

        node.append(TemplateWordNode("Hello World"))
        self.assertEqual(root.resolve(self.bot, self.clientid), "H e l l o W o r l d")


######################################################################################################################
#
class TemplateImplodeNodeTests(TemplateTestsBaseClass):

    def test_node(self):
        root = TemplateNode()
        self.assertIsNotNone(root)
        self.assertIsNotNone(root.children)
        self.assertEqual(len(root.children), 0)

        node = TemplateImplodeNode()
        self.assertIsNotNone(node)

        root.append(node)
        self.assertEqual(len(root.children), 1)

        node.append(TemplateWordNode("H e l l o W o r l d"))
        self.assertEqual(root.resolve(self.bot, self.clientid), "HelloWorld")


#####################################################################################################################
#
class TemplateThatNodeTests(TemplateTestsBaseClass):

    def test_node(self):
        root = TemplateNode()
        self.assertIsNotNone(root)
        self.assertIsNotNone(root.children)
        self.assertEqual(len(root.children), 0)

        node = TemplateThatNode()
        self.assertIsNotNone(node)

        root.append(node)
        self.assertEqual(len(root.children), 1)


#####################################################################################################################
#
class TemplateThatStarNodeTests(TemplateTestsBaseClass):

    def test_node(self):
        root = TemplateNode()
        self.assertIsNotNone(root)
        self.assertIsNotNone(root.children)
        self.assertEqual(len(root.children), 0)

        node = TemplateThatStarNode()
        self.assertIsNotNone(node)

        root.append(node)
        self.assertEqual(len(root.children), 1)


#####################################################################################################################
#
class TemplateTopicStarNodeTests(TemplateTestsBaseClass):

    def test_node(self):
        root = TemplateNode()
        self.assertIsNotNone(root)
        self.assertIsNotNone(root.children)
        self.assertEqual(len(root.children), 0)

        node = TemplateTopicStarNode()
        self.assertIsNotNone(node)

        root.append(node)
        self.assertEqual(len(root.children), 1)



#####################################################################################################################
#
class TemplateInputNodeTests(TemplateTestsBaseClass):

    def test_node(self):
        root = TemplateNode()
        self.assertIsNotNone(root)
        self.assertIsNotNone(root.children)
        self.assertEqual(len(root.children), 0)

        node = TemplateInputNode()
        self.assertIsNotNone(node)

        root.append(node)
        self.assertEqual(len(root.children), 1)

        conversation = Conversation("testid", self.bot)
        question = Question.create_from_text("Hello world")
        question.current_sentence()._response = "Hello matey"
        conversation._questions.append(question)
        self.bot._conversations["testid"] = conversation

        response = root.resolve(self.bot, "testid")
        self.assertIsNotNone(response)
        self.assertEqual(response, "Hello world")


#####################################################################################################################
#
class TemplateRequestNodeTests(TemplateTestsBaseClass):

    def test_node(self):
        root = TemplateNode()
        self.assertIsNotNone(root)
        self.assertIsNotNone(root.children)
        self.assertEqual(len(root.children), 0)

        node = TemplateRequestNode()
        self.assertIsNotNone(node)

        root.append(node)
        self.assertEqual(len(root.children), 1)

        conversation = Conversation("testid", self.bot)
        question = Question.create_from_text("Hello world")
        question.current_sentence()._response = "Hello matey"
        conversation._questions.append(question)
        self.bot._conversations["testid"] = conversation

        response = root.resolve(self.bot, "testid")
        self.assertIsNotNone(response)
        self.assertEqual(response, "Hello world")


#####################################################################################################################
#
class TemplateResponseNodeTests(TemplateTestsBaseClass):

    def test_node(self):
        root = TemplateNode()
        self.assertIsNotNone(root)
        self.assertIsNotNone(root.children)
        self.assertEqual(len(root.children), 0)

        node = TemplateResponseNode()
        self.assertIsNotNone(node)

        root.append(node)
        self.assertEqual(len(root.children), 1)

        conversation = Conversation("testid", self.bot)
        question = Question.create_from_text("Hello world")
        question.current_sentence()._response = "Hello Matey"
        conversation._questions.append(question)
        self.bot._conversations["testid"] = conversation

        response = root.resolve(self.bot, "testid")
        self.assertIsNotNone(response)
        self.assertEqual(response, "Hello Matey")


#####################################################################################################################
#
class TemplateDateNodeTests(TemplateTestsBaseClass):

    DEFAULT_DATETIME_REGEX = "^.{3}\s*.{3}\s*\d{1,}\s\d{2}:\d{2}:\d{2}\s\d{4}"

    def test_node_default_format(self):
        root = TemplateNode()
        self.assertIsNotNone(root)
        self.assertIsNotNone(root.children)
        self.assertEqual(len(root.children), 0)

        node = TemplateDateNode()
        self.assertIsNotNone(node)

        root.append(node)
        self.assertEqual(len(root.children), 1)
        self.assertRegex(root.resolve(self.bot, self.clientid), TemplateDateNodeTests.DEFAULT_DATETIME_REGEX)

    def test_node_custom_format(self):
        root = TemplateNode()
        self.assertIsNotNone(root)
        self.assertIsNotNone(root.children)
        self.assertEqual(len(root.children), 0)

        node = TemplateDateNode()
        self.assertIsNotNone(node)

        root.append(node)
        self.assertEqual(len(root.children), 1)
        self.assertRegex(root.resolve(self.bot, self.clientid), TemplateDateNodeTests.DEFAULT_DATETIME_REGEX)


#####################################################################################################################
#
class TemplateIntervalNodeTests(TemplateTestsBaseClass):

    def test_node_years(self):
        root = TemplateNode()
        self.assertIsNotNone(root)
        self.assertIsNotNone(root.children)
        self.assertEqual(len(root.children), 0)

        node = TemplateIntervalNode()
        node._format = TemplateWordNode("%c")
        node._style = TemplateWordNode("years")
        node._from = TemplateWordNode("Thu Oct  6 16:35:11 2014")
        node._to = TemplateWordNode("Fri Oct  7 16:35:11 2016")

        self.assertIsNotNone(node)

        root.append(node)
        self.assertEqual(len(root.children), 1)

        response = root.resolve(self.bot, self.clientid)
        self.assertIsNotNone(response)
        self.assertEqual(response, "2")

    def test_node_months(self):
        root = TemplateNode()
        self.assertIsNotNone(root)
        self.assertIsNotNone(root.children)
        self.assertEqual(len(root.children), 0)

        node = TemplateIntervalNode()
        node._format = TemplateWordNode("%c")
        node._style = TemplateWordNode("months")
        node._from = TemplateWordNode("Thu Jul  6 16:35:11 2014")
        node._to = TemplateWordNode("Fri Oct  7 16:35:11 2016")

        self.assertIsNotNone(node)

        root.append(node)
        self.assertEqual(len(root.children), 1)

        response = root.resolve(self.bot, self.clientid)
        self.assertIsNotNone(response)
        self.assertEqual(response, "3")

    def test_node_weeks(self):
        root = TemplateNode()
        self.assertIsNotNone(root)
        self.assertIsNotNone(root.children)
        self.assertEqual(len(root.children), 0)

        node = TemplateIntervalNode()
        node._format = TemplateWordNode("%c")
        node._style = TemplateWordNode("weeks")
        node._from = TemplateWordNode("Thu Oct  1 16:35:11 2016")
        node._to = TemplateWordNode("Fri Oct  14 16:35:11 2016")

        self.assertIsNotNone(node)

        root.append(node)
        self.assertEqual(len(root.children), 1)

        response = root.resolve(self.bot, self.clientid)
        self.assertIsNotNone(response)
        self.assertEqual(response, "1")

    def test_node_days(self):
        root = TemplateNode()
        self.assertIsNotNone(root)
        self.assertIsNotNone(root.children)
        self.assertEqual(len(root.children), 0)

        node = TemplateIntervalNode()
        node._format = TemplateWordNode("%c")
        node._style = TemplateWordNode("days")
        node._from = TemplateWordNode("Thu Oct  6 16:35:11 2016")
        node._to = TemplateWordNode("Fri Oct  7 16:35:11 2016")

        self.assertIsNotNone(node)

        root.append(node)
        self.assertEqual(len(root.children), 1)

        response = root.resolve(self.bot, self.clientid)
        self.assertIsNotNone(response)
        self.assertEqual(response, "1")

    def test_node_hours(self):
        root = TemplateNode()
        self.assertIsNotNone(root)
        self.assertIsNotNone(root.children)
        self.assertEqual(len(root.children), 0)

        node = TemplateIntervalNode()
        node._format = TemplateWordNode("%c")
        node._style = TemplateWordNode("hours")
        node._from = TemplateWordNode("Thu Oct  7 12:35:11 2016")
        node._to = TemplateWordNode("Fri Oct  7 16:35:11 2016")

        self.assertIsNotNone(node)

        root.append(node)
        self.assertEqual(len(root.children), 1)

        response = root.resolve(self.bot, self.clientid)
        self.assertIsNotNone(response)
        self.assertEqual(response, "4")

    def test_node_minutes(self):
        root = TemplateNode()
        self.assertIsNotNone(root)
        self.assertIsNotNone(root.children)
        self.assertEqual(len(root.children), 0)

        node = TemplateIntervalNode()
        node._format = TemplateWordNode("%c")
        node._style = TemplateWordNode("minutes")
        node._from = TemplateWordNode("Thu Oct 7 16:33:09 2016")
        node._to = TemplateWordNode("Fri Oct 7 16:35:11 2016")

        self.assertIsNotNone(node)

        root.append(node)
        self.assertEqual(len(root.children), 1)

        response = root.resolve(self.bot, self.clientid)
        self.assertIsNotNone(response)
        self.assertEqual(response, "2")

    def test_node_seconds(self):
        root = TemplateNode()
        self.assertIsNotNone(root)
        self.assertIsNotNone(root.children)
        self.assertEqual(len(root.children), 0)

        node = TemplateIntervalNode()
        node._format = TemplateWordNode("%c")
        node._style = TemplateWordNode("seconds")
        node._from = TemplateWordNode("Thu Oct 7 16:35:09 2016")
        node._to = TemplateWordNode("Fri Oct 7 16:35:11 2016")

        self.assertIsNotNone(node)

        root.append(node)
        self.assertEqual(len(root.children), 1)

        response = root.resolve(self.bot, self.clientid)
        self.assertIsNotNone(response)
        self.assertEqual(response, "2")

    def test_node_ymdhms(self):
        root = TemplateNode()
        self.assertIsNotNone(root)
        self.assertIsNotNone(root.children)
        self.assertEqual(len(root.children), 0)

        node = TemplateIntervalNode()
        node._format = TemplateWordNode("%c")
        node._style = TemplateWordNode("ymdhms")
        node._from = TemplateWordNode("Thu Jul 14 16:33:09 2014")
        node._to = TemplateWordNode("Fri Oct 7 16:35:11 2016")

        self.assertIsNotNone(node)

        root.append(node)
        self.assertEqual(len(root.children), 1)

        response = root.resolve(self.bot, self.clientid)
        self.assertIsNotNone(response)
        self.assertEqual(response, "2 years, 2 months, 23 days, 0 hours, 2 minutes, 2 seconds")


#####################################################################################################################
#
class TemplateSystemNodeTests(TemplateTestsBaseClass):

    def test_node(self):
        root = TemplateNode()
        self.assertIsNotNone(root)
        self.assertIsNotNone(root.children)
        self.assertEqual(len(root.children), 0)

        node = TemplateSystemNode()
        self.assertIsNotNone(node)
        node.append(TemplateWordNode('echo "Hello World"'))

        root.append(node)
        self.assertEqual(len(root.children), 1)

        response = root.resolve(self.bot, self.clientid)
        self.assertIsNotNone(response)
        self.assertEqual(response, "Hello World")


#####################################################################################################################
#
class TemplateSizeNodeTests(TemplateTestsBaseClass):

    def test_node(self):
        root = TemplateNode()
        self.assertIsNotNone(root)
        self.assertIsNotNone(root.children)
        self.assertEqual(len(root.children), 0)

        node = TemplateSizeNode()
        self.assertIsNotNone(node)

        root.append(node)
        self.assertEqual(len(root.children), 1)

        response = root.resolve(self.bot, self.clientid)
        self.assertIsNotNone(response)
        self.assertEqual(response, "0")


######################################################################################################################
#
class TemplateNodeMixedTests(TemplateTestsBaseClass):

    def test_multirandom(self):
        root = TemplateNode()
        self.assertIsNotNone(root)

        random1 = TemplateRandomNode()
        random1.append(TemplateWordNode("Test1"))
        random1.append(TemplateWordNode("Test2"))
        self.assertEqual(len(random1.children), 2)

        random2 = TemplateRandomNode()
        random2.append(TemplateWordNode("Test3"))
        random2.append(TemplateWordNode("Test4"))
        self.assertEqual(len(random1.children), 2)

        root.append(random1)
        root.append(random2)

        resolved = root.resolve(self.bot, self.clientid)
        self.assertIsNotNone(resolved)
        self.assertOneOf(resolved, ["Test1 Test3",
                                    "Test1 Test4",
                                    "Test2 Test3",
                                    "Test2 Test4"])

    def test_nestedrandom(self):
        root = TemplateNode()
        self.assertIsNotNone(root)

        random1 = TemplateRandomNode()
        random1.append(TemplateWordNode("Test1"))
        random1.append(TemplateWordNode("Test2"))
        self.assertEqual(len(random1.children), 2)

        random2 = TemplateRandomNode()
        random2.append(TemplateWordNode("Test3"))
        random2.append(TemplateWordNode("Test4"))
        self.assertEqual(len(random1.children), 2)

        random3 = TemplateRandomNode()
        random3.append(random1)
        random3.append(random1)
        random3.append(random2)

        root.append(random3)

        resolved = root.resolve(self.bot, self.clientid)
        self.assertIsNotNone(resolved)
        self.assertOneOf(resolved, ["Test1",
                                    "Test2",
                                    "Test3",
                                    "Test4"])

    def test_mixednodes(self):
        root = TemplateNode()
        self.assertIsNotNone(root)

        random1 = TemplateRandomNode()
        random1.append(TemplateWordNode("Test1"))
        random1.append(TemplateWordNode("Test2"))
        random1.append(TemplateWordNode("Test3"))
        self.assertEqual(len(random1.children), 3)

        root.append(TemplateWordNode("Hello"))
        root.append(random1)
        root.append(TemplateWordNode("World!"))

        self.assertEqual(len(root.children), 3)

        resolved = root.resolve(self.bot, self.clientid)
        self.assertIsNotNone(resolved)
        self.assertOneOf(resolved, ["Hello Test1 World!", "Hello Test2 World!", "Hello Test3 World!"])
