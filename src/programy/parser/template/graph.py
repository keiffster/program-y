"""
Copyright (c) 2016 Keith Sterling

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated
documentation files (the "Software"), to deal in the Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software,
and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO
THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""

from programy.utils.parsing.linenumxml import LineNumberingParser
import xml.etree.ElementTree as ET

import logging

from programy.parser.exceptions import ParserException
from programy.parser.template.nodes.base import TemplateNode
from programy.parser.template.nodes.word import TemplateWordNode
from programy.parser.template.nodes.rand import TemplateRandomNode
from programy.parser.template.nodes.condtype1 import TemplateType1ConditionNode
from programy.parser.template.nodes.condtype2 import TemplateType2ConditionNode
from programy.parser.template.nodes.condtype3 import TemplateType3ConditionNode
from programy.parser.template.nodes.condlistitem import TemplateConditionListItemNode
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

class TemplateGraph(object):

    def __init__(self, aiml_parser=None):
        self._aiml_parser = aiml_parser

    #
    # TEMPLATE_EXPRESSION ::== TEXT | TAG_EXPRESSION | (TEMPLATE_EXPRESSION)*
    #
    def parse_template_expression(self, pattern):
        node = TemplateNode()
        self.parse_template_node(pattern, node)
        return node

    def parse_template_node(self, pattern, current_branch):

        head_text = self.get_text_from_element(pattern)
        head_result = self.parse_text(head_text, current_branch)

        found_sub = False
        for sub_pattern in pattern:
            self.parse_tag_expression(sub_pattern, current_branch)

            tail_text = self.get_tail_from_element(sub_pattern)
            self.parse_text(tail_text, current_branch)

            found_sub = True

        if head_result is False and found_sub is False:
            if hasattr(pattern, '_end_line_number'):
                logging.warning("No context in template tag at [line(%d), column(%d)]" %
                                                            (pattern._end_line_number,
                                                             pattern._end_column_number))
            else:
                logging.warning("No context in template tag")

    def parse_text(self, text, branch):
        if text is not None:
            string = text.strip()
            if len(string) > 0:
                words = string.split(" ")
                for word in words:
                    if word is not None and len(word) > 0:
                        branch.children.append(TemplateWordNode(word.strip()))
                return True
        return False

    def get_text_from_element(self, element):
        text = element.text
        if text is not None:
            text = text.strip()
            return text
        return None

    def get_tail_from_element(self, element):
        text = element.tail
        if text is not None:
            text = text.strip()
            if text == "":
                return None
            return text
        return None

    def parse_tag_expression(self, expression, branch):
        if expression.tag == 'random':
            self.parse_random_expression(expression, branch)
        elif expression.tag == 'condition':
            self.parse_condition_expression(expression, branch)
        elif expression.tag == 'srai':
            self.parse_srai_expression(expression, branch)
        elif expression.tag == 'sraix':
            self.parse_sraix_expression(expression, branch)
        elif expression.tag == 'get':
            self.parse_get_expression(expression, branch)
        elif expression.tag == 'set':
            self.parse_set_expression(expression, branch)
        elif expression.tag == 'map':
            self.parse_map_expression(expression, branch)
        elif expression.tag == 'bot':
            self.parse_bot_expression(expression, branch)
        elif expression.tag == 'date':
            self.parse_date_expression(expression, branch)
        elif expression.tag == 'interval':
            self.parse_interval_expression(expression, branch)
        elif expression.tag == 'think':
            self.parse_think_expression(expression, branch)
        elif expression.tag == 'normalize':
            self.parse_normalize_expression(expression, branch)
        elif expression.tag == 'denormalize':
            self.parse_denormalize_expression(expression, branch)
        elif expression.tag == 'person':
            self.parse_person_expression(expression, branch)
        elif expression.tag == 'person2':
            self.parse_person2_expression(expression, branch)
        elif expression.tag == 'gender':
            self.parse_gender_expression(expression, branch)
        elif expression.tag == 'system':
            self.parse_system_expression(expression, branch)
        elif expression.tag == 'star':
            self.parse_star_expression(expression, branch)
        elif expression.tag == 'that':
            self.parse_that_expression(expression, branch)
        elif expression.tag == 'thatstar':
            self.parse_thatstar_expression(expression, branch)
        elif expression.tag == 'topicstar':
            self.parse_topicstar_expression(expression, branch)
        elif expression.tag == 'input':
            self.parse_input_expression(expression, branch)
        elif expression.tag == 'request':
            self.parse_request_expression(expression, branch)
        elif expression.tag == 'response':
            self.parse_response_expression(expression, branch)
        elif expression.tag == 'learn':
            self.parse_learn_expression(expression, branch)
        elif expression.tag == 'learnf':
            self.parse_learnf_expression(expression, branch)
        elif expression.tag == 'sr':
            self.parse_sr_expression(expression, branch)
        elif expression.tag == 'id':
            self.parse_id_expression(expression, branch)
        elif expression.tag == 'vocabulary':
            self.parse_vocabulary_expression(expression, branch)
        elif expression.tag == 'program':
            self.parse_program_expression(expression, branch)
        elif expression.tag == 'implode':
            self.parse_implode_expression(expression, branch)
        elif expression.tag == 'explode':
            self.parse_explode_expression(expression, branch)
        elif expression.tag == 'formal':
            self.parse_formal_expression(expression, branch)
        elif expression.tag == 'lowercase':
            self.parse_lowercase_expression(expression, branch)
        elif expression.tag == 'uppercase':
            self.parse_uppercase_expression(expression, branch)
        elif expression.tag == 'sentence':
            self.parse_sentence_expression(expression, branch)
        elif expression.tag == 'eval':
            self.parse_eval_expression(expression, branch)
        elif expression.tag == 'size':
            self.parse_size_expression(expression, branch)
        elif expression.tag == 'oob':
            self.parse_oob_expression(expression, branch)
        elif expression.tag == 'first':
            self.parse_first_expression(expression, branch)
        elif expression.tag == 'rest':
            self.parse_rest_expression(expression, branch)

        # Tags found in Program-A reference implementation, but not documented in the spec !!! ffs
        # addtriple
        # deletetriple
        # select
        # uniq
        # resetlearnf
        # resetlearn
        # search

        # This is tag not AIML 2.0 compliant
        elif expression.tag == 'extension':
            self.parse_extension_expression(expression, branch)
        # This is tag not AIML 2.0 compliant
        elif expression.tag == 'log':
            self.parse_log_expression(expression, branch)

        else:
            self.parse_unknown_as_text_node(expression, branch)
            #raise ParserException("Error, unknown expression tag: <%s>" % (expression.tag), xml_element=expression)

    #######################################################################################################
    # 	UNKNONWN NODE
    #   When its a node we don't know, add it as a text node. This deals with html nodes creeping into the text

    def parse_unknown_as_text_node(self, expression, branch):
        value = ET.tostring(expression, encoding="utf-8", method='xml').decode("utf-8")
        text_node = TemplateWordNode(word=value.strip())
        branch.children.append(text_node)

    #######################################################################################################
    # 	RANDOM_EXPRESSION ::== <random>(<li>TEMPLATE_EXPRESSION</li>)+</random>

    def parse_random_expression(self, expression, branch):
        random_node = TemplateRandomNode()
        branch.children.append(random_node)

        li_found = False
        for child in expression:
            if child.tag == 'li':
                li_found = True
                li_node = TemplateNode()
                random_node.children.append(li_node)
                self.parse_template_node(child, li_node)
            else:
                raise ParserException("Error, unsupported random child tag: %s" % (child.tag), xml_element=expression)

        if li_found is False:
            raise ParserException("Error, no li children of random element!", xml_element=expression)

    #######################################################################################################
    # CONDITION_ITEM_COMPONENT ::== <name>TEMPLATE_EXPRESSION</name> | <value>TEMPLATE_EXPRESSION</value> | <loop/> | TEMPLATE_EXPRESSION
    # CONDITION_ITEM_EXPRESSION ::== <li( CONDITION_ATTRIBUTES)*>(CONDITION_ITEM_COMPONENT)*</li>
    # CONDITION_ATTRIBUTES ::== (name="NAME") | (value="NORMALIZED_TEXT")
    # CONDITION_EXPRESSION ::== <condition( CONDITION_ATTRIBUTES)>(CONDITION_ITEM_EXPRESSION)*</condition>
    #
    def parse_condition_attributes(self, expression):
        name = None
        value = None

        if 'name' in expression.attrib:
            name = expression['name']
        if 'value' in expression.attrib:
            value = expression['value']

        return name, value

    def parse_condition_expression(self, expression, branch):

        lis = expression.findall('li')
        if len(lis) == 0:
            self.parse_type1_condition(expression, branch)
        elif 'name' in expression.attrib or len(expression.findall('name')) > 0:
            self.parse_type2_condition(expression, branch)
        elif 'var' in expression.attrib or len(expression.findall('var')) > 0:
            self.parse_type2_condition(expression, branch)
        else:
            self.parse_type3_condition(expression, branch)

    def get_condition_name(self, condition, raise_on_missing=True):
        if 'name' in condition.attrib:
            return (condition.attrib['name'], False)
        elif 'var' in condition.attrib:
            return (condition.attrib['var'], True)
        else:
            names = condition.findall('name')
            variables = condition.findall('var')
            if len(names) == 0 and len(variables) == 0:
                if raise_on_missing is True:
                    raise ParserException("Error, condition element has no name or var", xml_element=condition)
                else:
                    return (None, False)
            elif len(names) > 1:
                if raise_on_missing is True:
                    raise ParserException("Error, condition element has multiple name elements", xml_element=condition)
                else:
                    return (None, False)
            elif len(variables) > 1:
                if raise_on_missing is True:
                    raise ParserException("Error, condition element has multiple var elements", xml_element=condition)
                else:
                    return (None, False)
            else:
                if len(names) == 1:
                    name_text = self.get_text_from_element(condition.find('name'))
                    return (name_text, False)
                else:
                    var_text = self.get_text_from_element(condition.find('var'))
                    return (var_text, True)

    def get_condition_value(self, condition, raise_on_missing=True):
        if 'value' in condition.attrib:
            value_node = TemplateNode()
            value_node.append(TemplateWordNode(condition.attrib['value']))
            return value_node
            #return condition.attrib['value']
        else:
            values = condition.findall('value')
            if len(values) == 0:
                if raise_on_missing is True:
                    raise ParserException("Error, element has no value", xml_element=condition)
                else:
                    return None
            elif len(values) > 1:
                if raise_on_missing is True:
                    raise ParserException("Error, element has multiple value elements", xml_element=condition)
                else:
                    return None
            else:
                value_node = TemplateNode()
                self.parse_template_node(values[0], value_node)
                return value_node
                #return self.get_text_from_element(condition.find('value'))

    # Type 1
    # <condition name="predicate" value="v">X</condition>,
    # <condition name="predicate"><value>v</value>X</condition>,
    # <condition value="v"><name>predicate</name>X</condition>, and
    # <condition><name>predicate</name><value>v</value>X</condition>
    #
    def parse_type1_condition(self, expression, branch):

        response = self.get_condition_name(expression)

        name = response[0]
        local = response[1]
        value = self.get_condition_value(expression)

        condition = TemplateType1ConditionNode(name=name, value=value, local=local)
        branch.append(condition)

        self.parse_text(self.get_text_from_element(expression), condition)

        for child in expression:
            if child.tag == 'name':
                pass

            elif child.tag == 'var':
                pass

            elif child.tag == 'value':
                pass

            elif child.tag == 'li':
                raise ParserException("Error, li element not allowed as child of condition element", xml_element=expression)

            elif child.tag == 'loop':
                raise ParserException("Error, this type of condition cannot have <loop /> element", xml_element=expression)

            else:
                self.parse_tag_expression(child, condition)
            tail_text = self.get_tail_from_element(child)
            self.parse_text(tail_text, condition)

    # Type 2
    # <condition name="predicate">...</condition>
    # <condition><name>predicate</name>...</condition>
    # 	<li value="a">X</li>
    # 	<li value="b">Y</li>
    # 	<li>Z</li>				<- Default value if no condition met
    #
    def parse_type2_condition(self, expression, branch):
        response = self.get_condition_name(expression)
        name = response[0]
        local = response[1]

        condition = TemplateType2ConditionNode(name=name, local=local)

        branch.append(condition)

        for child in expression:
            if child.tag == 'name':
                # Pass on this attribute as we have already pulled it from the get_condition_name above
                pass

            elif child.tag == 'var':
                # Pass on this attribute as we have already pulled it from the get_condition_name above
                pass

            elif child.tag == 'li':

                list_item = TemplateConditionListItemNode()

                list_item.value = self.get_condition_value(child, False)
                list_item.local = condition.local

                condition.children.append(list_item)
                self.parse_text(self.get_text_from_element(child), list_item)

                for sub_pattern in child:

                    if sub_pattern.tag == 'name':
                        pass

                    elif sub_pattern.tag == 'var':
                        pass

                    elif sub_pattern.tag == 'value':
                        pass

                    elif sub_pattern.tag == 'loop':
                        list_item.loop = True

                    else:
                        self.parse_tag_expression(sub_pattern, list_item)

                    tail_text = self.get_tail_from_element(sub_pattern)
                    self.parse_text(tail_text, list_item)

            else:
                raise ParserException("Error, invalid element <%s> in condition element" % (child.tag), xml_element=expression)

    # Type 3
    #  <condition>
    # 	<li name='1' value="a">X</li>
    # 	<li value="b"><name>1</name>Y</li>
    # 	<li name="1"><value>b</value>Z</li>
    # 	<li><name>1</name><value>b</value>Z</li>
    # 	<li>Z<l/i>				<- Default value if no condition met
    #  </condition>
    #
    def parse_type3_condition(self, expression, branch):
        condition = TemplateType3ConditionNode()
        branch.append(condition)

        for child in expression:

            if child.tag == 'name':
                pass

            elif child.tag == 'var':
                pass

            elif child.tag == 'li':
                list_item = TemplateConditionListItemNode()

                response = self.get_condition_name(child, False)
                list_item.name = response[0]
                list_item.local = response[1]

                list_item.value = self.get_condition_value(child, False)

                condition.append(list_item)

                self.parse_text(self.get_text_from_element(child), list_item)

                for sub_pattern in child:
                    if sub_pattern.tag == 'name':
                        pass

                    elif sub_pattern.tag == 'var':
                        pass

                    elif sub_pattern.tag == 'value':
                        pass

                    elif sub_pattern.tag == 'loop':
                        list_item.loop = True

                    else:
                        self.parse_tag_expression(sub_pattern, list_item)

                    tail_text = self.get_tail_from_element(sub_pattern)
                    self.parse_text(tail_text, list_item)

            else:
                raise ParserException("Error, invalid element <%s> in condition element" % (child.tag), xml_element=expression)

    #######################################################################################################
    # SRAI_EXPRESSION ::== <srai>TEMPLATE_EXPRESSION</srai>

    def parse_srai_expression(self, expression, branch):
        self._parse_node(TemplateSRAINode(), expression, branch)

    #######################################################################################################
    # SRAIX_ATTRIBUTES ::= host="HOSTNAME" | botid="BOTID" | hint="TEXT" | apikey="APIKEY" | service="SERVICE"
    # SRAIX_ATTRIBUTE_TAGS ::= <host>TEMPLATE_EXPRESSION</host> | <botid>TEMPLATE_EXPRESSION</botid> | <hint>TEMPLATE_EXPRESSION</hint> | <apikey>TEMPLATE_EXPRESSION</apikey> | <service>TEMPLATE_EXPRESSION</service>
    # SRAIX_EXPRESSION ::== <sraix( SRAIX_ATTRIBUTES)*>TEMPLATE_EXPRESSION</sraix> |

    def parse_sraix_expression(self, expression, branch):

        sraix_node = TemplateSRAIXNode()
        branch.children.append(sraix_node)

        if 'host' in expression.attrib:
            logging.warning("'host' attrib not supported in sraix, moved to config, see documentation")
        if 'botid' in expression.attrib:
            logging.warning("'botid' attrib not supported in sraix, moved to config, see documentation")
        if 'hint' in expression.attrib:
            logging.warning("'hint' attrib not supported in sraix, moved to config, see documentation")
        if 'apikey' in expression.attrib:
            logging.warning("'apikey' attrib not supported in sraix, moved to config, see documentation")

        if 'service' in expression.attrib:
            sraix_node.service = expression.attrib['service']

        head_text = self.get_text_from_element(expression)
        self.parse_text(head_text, sraix_node)

        for child in expression:
            if child.tag == 'host':
                logging.warning("'host' element not supported in sraix, moved to config, see documentation")
            elif child.tag == 'botid':
                logging.warning("'botid' element not supported in sraix, moved to config, see documentation")
            elif child.tag == 'hint':
                logging.warning("'hint' element not supported in sraix, moved to config, see documentation")
            elif child.tag == 'apikey':
                logging.warning("'apikey' element not supported in sraix, moved to config, see documentation")
            elif child.tag == 'service':
                sraix_node.service = self.get_text_from_element(child)
            else:
                self.parse_tag_expression(child, sraix_node)

            tail_text = self.get_tail_from_element(child)
            self.parse_text(tail_text, sraix_node)

        if sraix_node.service is None:
            logging.warning("SRAIX node, service missing !")

    # ######################################################################################################
    # GET_PREDICATE_EXPRESSION ::==
    # <get name="WORD"/> |
    # <get><name>TEMPLATE_EXPRESSION</name></get> |
    # <get var=”WORD”> |
    # <get><var>WORD</var></get>

    def parse_get_expression(self, expression, branch):

        get_node = TemplateGetNode()
        branch.children.append(get_node)

        name_found = False
        var_found = False

        if 'name' in expression.attrib:
            node = TemplateNode()
            name_node = TemplateWordNode(expression.attrib['name'])
            node.append(name_node)
            get_node.local = False
            name_found = True
            get_node.name = node

        if 'var' in expression.attrib:
            node = TemplateNode()
            var_node = TemplateWordNode(expression.attrib['var'])
            node.append(var_node)
            get_node.local = True
            var_found = True
            get_node.name = node

        for child in expression:

            if child.tag == 'name':
                node = TemplateNode()

                self.parse_text(self.get_text_from_element(child), node)
                for sub_child in child:
                    self.parse_tag_expression(sub_child, node)
                    self.parse_text(self.get_text_from_element(child), node)

                get_node.name = node
                get_node.local = False
                name_found = True

            elif child.tag == 'var':
                node = TemplateNode()

                self.parse_text(self.get_text_from_element(child), node)
                for sub_child in child:
                    self.parse_tag_expression(sub_child, node)
                    self.parse_text(self.get_text_from_element(child), node)

                get_node.name = node
                get_node.local = True
                var_found = True

            else:
                raise ParserException("Error, invalid get", xml_element=expression)

        if name_found is True and var_found is True:
            raise ParserException("Error, get node has both name AND var values", xml_element=expression)

    # ######################################################################################################
    # SET_PREDICATE_EXPRESSION ::==
    # <set name="WORD">TEMPLATE_EXPRESSION</set> |
    # <set><name>TEMPLATE_EXPRESSION</name>TEMPLATE_EXPRESSION</set> |
    # <set var="WORD">TEMPLATE_EXPRESSION</set> |
    # <set><var>TEMPLATE_EXPRESSION</var>TEMPLATE_EXPRESSION</set>

    def parse_set_expression(self, expression, branch):

        set_node = TemplateSetNode()
        branch.children.append(set_node)

        name_found = False
        var_found = False

        if 'name' in expression.attrib:
            node = TemplateNode()
            name_node = TemplateWordNode(expression.attrib['name'])
            node.append(name_node)
            set_node.local = False
            name_found = True
            set_node.name = node

        if 'var' in expression.attrib:
            node = TemplateNode()
            name_node = TemplateWordNode(expression.attrib['var'])
            node.append(name_node)
            set_node.local = True
            var_found = True
            set_node.name = node

        self.parse_text(self.get_text_from_element(expression), set_node)

        for child in expression:

            if child.tag == 'name':
                node = TemplateNode()

                self.parse_text(self.get_text_from_element(child), node)
                for sub_child in child:
                    self.parse_tag_expression(sub_child, node)
                    self.parse_text(self.get_text_from_element(child), node)

                set_node.name = node
                set_node.local = False
                name_found = True

            elif child.tag == 'var':
                node = TemplateNode()

                self.parse_text(self.get_text_from_element(child), node)
                for sub_child in child:
                    self.parse_tag_expression(sub_child, node)
                    self.parse_text(self.get_text_from_element(child), node)

                set_node.name = node
                set_node.local = True
                var_found = True

            else:
                self.parse_tag_expression(child, set_node)

            self.parse_text(self.get_tail_from_element(child), set_node)

        if name_found is True and var_found is True:
            raise ParserException("Error, set node has both name AND var values", xml_element=expression)

        if name_found is False and var_found is False:
            raise ParserException("Error, set node has both name AND var values", xml_element=expression)

    # ######################################################################################################
    # MAP_EXPRESSION ::=
    # <map name="WORD">TEMPLATE_EXPRESSION</map> |
    # <map><name>TEMPLATE_EXPRESSION</name>TEMPLATE_EXPRESSION</map>

    def parse_map_expression(self, expression, branch):

        map_node = TemplateMapNode()
        branch.children.append(map_node)

        name_found = False

        if 'name' in expression.attrib:
            node = TemplateNode()
            name_node = TemplateWordNode(expression.attrib['name'])
            node.append(name_node)
            name_found = True
            map_node.name = node

        self.parse_text(self.get_text_from_element(expression), map_node)

        for child in expression:

            if child.tag == 'name':
                node = TemplateNode()

                self.parse_text(self.get_text_from_element(child), node)
                for sub_child in child:
                    self.parse_tag_expression(sub_child, node)
                    self.parse_text(self.get_text_from_element(child), node)

                map_node.name = node
                name_found = True

            else:
                self.parse_tag_expression(child, map_node)

            self.parse_text(self.get_tail_from_element(child), map_node)

        if name_found is False:
            raise ParserException("Error, name not found", xml_element=expression)

    # ######################################################################################################
    # BOT_PROPERTY_EXPRESSION ::==
    # <bot name="PROPERTY"/> |
    # <bot><name>TEMPLATE_EXPRESSION</name></bot>

    def parse_bot_expression(self, expression, branch):

        bot_node = TemplateBotNode()
        branch.children.append(bot_node)

        name_found = False

        if 'name' in expression.attrib:
            node = TemplateNode()
            name_node = TemplateWordNode(expression.attrib['name'])
            node.append(name_node)
            name_found = True
            bot_node.name = node

        self.parse_text(self.get_text_from_element(expression), bot_node)

        for child in expression:

            if child.tag == 'name':
                node = TemplateNode()
                self.parse_text(self.get_text_from_element(child), node)
                for sub_child in child:
                    self.parse_tag_expression(sub_child, node)
                    self.parse_text(self.get_text_from_element(child), node)

                bot_node.name = node
                name_found = True

            else:
                self.parse_tag_expression(child, bot_node)

            self.parse_text(self.get_tail_from_element(child), bot_node)

        if name_found is False:
            raise ParserException("Error, name not found", xml_element=expression)

    #######################################################################################################

    def _parse_node(self, node, expression, branch):
        branch.children.append(node)

        expression_text = self.parse_text(self.get_text_from_element(expression), node)

        expression_children = False
        for child in expression:
            self.parse_tag_expression(child, node)
            self.parse_text(self.get_tail_from_element(child), node)
            expression_children = True

        if expression_text is None and expression_children is False:
            # No content in node, default to <star/>
            logging.debug ("Node has no content (text or children), default to <star/>")
            node.append(TemplateStarNode())

    #######################################################################################################
    # THINK_EXPRESSION ::== <think>TEMPLATE_EXPRESSION</think>

    def parse_think_expression(self, expression, branch):
        self._parse_node(TemplateThinkNode(), expression, branch)

    #######################################################################################################
    # NORMALIZE_EXPRESSION ::== <normalize>TEMPLATE_EXPRESSION</normalize>

    def parse_normalize_expression(self, expression, branch):
        self._parse_node(TemplateNormalizeNode(), expression, branch)

    #######################################################################################################
    # DENORMALIZE_EXPRESSION ::== <denormalize>TEMPLATE_EXPRESSION</denormalize>

    def parse_denormalize_expression(self, expression, branch):
        self._parse_node(TemplateDenormalizeNode(), expression, branch)

    #######################################################################################################
    # PERSON_EXPRESSION ::== <person>TEMPLATE_EXPRESSION</person>

    def parse_person_expression(self, expression, branch):
        self._parse_node(TemplatePersonNode(), expression, branch)

    #######################################################################################################
    # PERSON2_EXPRESSION ::== <person2>TEMPLATE_EXPRESSION</person2>

    def parse_person2_expression(self, expression, branch):
        self._parse_node(TemplatePerson2Node(), expression, branch)

    #######################################################################################################
    # GENDER_EXPRESSION ::== <gender>TEMPLATE_EXPRESSION</gender>

    def parse_gender_expression(self, expression, branch):
        self._parse_node(TemplateGenderNode(), expression, branch)

    #######################################################################################################
    # <sr/> |

    def parse_sr_expression(self, expression, branch):
        self._parse_node(TemplateSrNode(), expression, branch)

    #######################################################################################################
    # <id/> |

    def parse_id_expression(self, expression, branch):
        self._parse_node(TemplateIdNode(), expression, branch)

    #######################################################################################################
    # <vocabulary/> |

    def parse_vocabulary_expression(self, expression, branch):
        self._parse_node(TemplateVocabularyNode(), expression, branch)

    #######################################################################################################
    # <size/> |

    def parse_size_expression(self, expression, branch):
        self._parse_node(TemplateSizeNode(), expression, branch)

    #######################################################################################################
    # <program/>	'''

    def parse_program_expression(self, expression, branch):
        self._parse_node(TemplateProgramNode(), expression, branch)

    #######################################################################################################
    # <explode>ABC</explode>

    def parse_explode_expression(self, expression, branch):
        self._parse_node(TemplateExplodeNode(), expression, branch)

    #######################################################################################################
    # <implode>ABC</implode>

    def parse_implode_expression(self, expression, branch):
        self._parse_node(TemplateImplodeNode(), expression, branch)

    #######################################################################################################
    # <lowercase>ABC</lowercase>

    def parse_lowercase_expression(self, expression, branch):
        self._parse_node(TemplateLowercaseNode(), expression, branch)

    #######################################################################################################
    # <uppercase>ABC</uppercase>

    def parse_uppercase_expression(self, expression, branch):
        self._parse_node(TemplateUppercaseNode(), expression, branch)

    #######################################################################################################
    # <formal>ABC</formal>

    def parse_formal_expression(self, expression, branch):
        self._parse_node(TemplateFormalNode(), expression, branch)

    #######################################################################################################
    # <sentence>ABC</sentence>

    def parse_sentence_expression(self, expression, branch):
        self._parse_node(TemplateSentenceNode(), expression, branch)


    #######################################################################################################
    # <explode>ABC</explode>

    def parse_first_expression(self, expression, branch):
        self._parse_node(TemplateFirstNode(), expression, branch)

    #######################################################################################################
    # <implode>ABC</implode>

    def parse_rest_expression(self, expression, branch):
        self._parse_node(TemplateRestNode(), expression, branch)

    #######################################################################################################

    def _parse_node_with_attrib(self, node, expression, branch, attrib_name, default_value=None):

        branch.children.append(node)

        attrib_found = True
        if attrib_name in expression.attrib:
            #logging.debug("Attrib [%s] found as part of node attributes" % attrib_name)
            node.set_attrib(attrib_name, expression.attrib[attrib_name])

        self.parse_text(self.get_text_from_element(expression), node)

        for child in expression:

            if child.tag == attrib_name:
                #logging.debug("Attrib [%s] found as part of child nodes" % attrib_name)
                node.set_attrib(attrib_name, self.get_text_from_element(child))
            else:
                self.parse_tag_expression(child, node)

            self.parse_text(self.get_tail_from_element(child), node)

        if attrib_found is False:
            logging.debug("Setting default value for attrib [%s]", attrib_name)
            node.set_attrib(attrib_name, default_value)

    #######################################################################################################
    # INDEX_ATTRIBUTE ::== index="NUMBER"
    # STAR_EXPRESSION ::== <star( INDEX_ATTRIBUTE)/> | <star><index>TEMPLATE_EXPRESSION</index></star>

    def parse_star_expression(self, expression, branch):
        self._parse_node_with_attrib(TemplateStarNode(), expression, branch, "index", "1")

    #######################################################################################################
    # THAT_EXPRESSION ::== <that( INDEX_ATTRIBUTE)/> | <that><index></index></that>

    def parse_that_expression(self, expression, branch):
        self._parse_node_with_attrib(TemplateThatNode(), expression, branch, "index", "1")

    #######################################################################################################
    # THATSTAR_EXPRESSION ::== <thatstar( INDEX_ATTRIBUTE)/> | <thatstar><index>TEMPLATE_EXPRESSION</index></thatstar>

    def parse_thatstar_expression(self, expression, branch):
        self._parse_node_with_attrib(TemplateThatStarNode(), expression, branch, "index", "1")

    #######################################################################################################
    # TOPICSTAR_EXPRESSION ::== <topicstar( INDEX_ATTRIBUTE)/> | <topicstar><index>TEMPLATE_EXPRESSION</index></topicstar>

    def parse_topicstar_expression(self, expression, branch):
        self._parse_node_with_attrib(TemplateTopicStarNode(), expression, branch, "index", "1")

    #######################################################################################################
    # INPUT_EXPRESSION ::== <input( INDEX_ATTRIBUTE)/> | <input><index>TEMPLATE_EXPRESSION</index></input>

    def parse_input_expression(self, expression, branch):
        self._parse_node_with_attrib(TemplateInputNode(), expression, branch, "index", "1")

    #######################################################################################################
    # REQUEST_EXPRESSION ::== <request( INDEX_ATTRIBUTE)/> | <request><index>TEMPLATE_EXPRESSION</index></request>

    def parse_request_expression(self, expression, branch):
        self._parse_node_with_attrib(TemplateRequestNode(), expression, branch, "index", "1")

    #######################################################################################################
    # RESPONSE_EXPRESSION ::== <response( INDEX_ATTRIBUTE)/> | <response><index>TEMPLATE_EXPRESSION</index></response>

    def parse_response_expression(self, expression, branch):
        self._parse_node_with_attrib(TemplateResponseNode(), expression, branch, "index", "1")

    #######################################################################################################
    # DATE_ATTRIBUTES ::== (format="LISP_DATE_FORMAT") | (jformat="JAVA DATE FORMAT")
    # DATE_ATTRIBUTE_TAG ::== <format>TEMPLATE_EXPRESSION</format> | <jformat>TEMPLATE_EXPRESSION</jformat>
    # DATE_EXPRESSION ::== <date( DATE_ATTRIBUTES)*/> | <date>(DATE_ATTRIBUTE_TAG)</date>
    # Pandorabots supports three extension attributes to the date element in templates:
    #     	locale
    #       format
    #       timezone

    def parse_date_expression(self, expression, branch):
        self._parse_node_with_attrib(TemplateDateNode(), expression, branch, "format", "%c")

    #######################################################################################################
    # SYSTEM_EXPRESSION ::==
    # 		<system( TIMEOUT_ATTRIBUTE)>TEMPLATE_EXPRESSION</system> |
    #  		<system><timeout>TEMPLATE_EXPRESSION</timeout></system>
    # TIMEOUT_ATTRIBUTE :== timeout=”NUMBER”

    def parse_system_expression(self, expression, branch):
        self._parse_node_with_attrib(TemplateSystemNode(), expression, branch, "timeout", "0")

    #######################################################################################################
    # INTERVAL_EXPRESSION ::== <interval>
    # 							(DATE_ATTRIBUTE_TAGS)
    # 							<style>(TEMPLATE_EXPRESSION)</style>
    # 							<from>(TEMPLATE_EXPRESSION)</from>
    # 							<to>(TEMPLATE_EXPRESSION)</to>
    # 						</interval>

    def parse_interval_expression(self, expression, branch):
        # TemplateInternalNode
        # aise ParserException ("Error, interval not implemented!")

        interval_node = TemplateIntervalNode()
        branch.children.append(interval_node)

        if 'format' in expression.attrib:
            interval_node.format = TemplateWordNode(expression.attrib['format'])

        head_text = self.get_text_from_element(expression)
        self.parse_text(head_text, interval_node)

        for child in expression:
            if child.tag == 'format':
                interval_node.format = TemplateWordNode(self.get_text_from_element(child))
            elif child.tag == 'style':
                node = TemplateNode()

                self.parse_text(self.get_text_from_element(child), node)
                for sub_child in child:
                    self.parse_tag_expression(sub_child, node)
                    self.parse_text(self.get_text_from_element(child), node)

                interval_node.style = node
            elif child.tag == 'from':
                node = TemplateNode()

                self.parse_text(self.get_text_from_element(child), node)
                for sub_child in child:
                    self.parse_tag_expression(sub_child, node)
                    self.parse_text(self.get_text_from_element(child), node)

                interval_node.interval_from = node
            elif child.tag == 'to':
                node = TemplateNode()

                self.parse_text(self.get_text_from_element(child), node)
                for sub_child in child:
                    self.parse_tag_expression(sub_child, node)
                    self.parse_text(self.get_text_from_element(child), node)

                interval_node.interval_to = node
            else:
                self.parse_tag_expression(child, interval_node)

            tail_text = self.get_tail_from_element(child)
            self.parse_text(tail_text, interval_node)

        if interval_node.format is None:
            logging.warning("Interval node, format missing !")
        if interval_node.style is None:
            logging.warning("style node, format missing !")
        if interval_node.interval_from is None:
            logging.warning("interval_from node, format missing !")
        if interval_node.interval_to is None:
            logging.warning("interval_to node, format missing !")

    #######################################################################################################
    # EXTENSION_EXPRESSION ::== <extension>
    #                               <path>programy.etension.SomeModule</path>
    #                               parameters
    # 						</extension>

    def parse_extension_expression(self, expression, branch):

        extension_node = TemplateExtensionNode()
        branch.children.append(extension_node)

        if 'path' in expression.attrib:
            extension_node.path = expression.attrib['path']

        head_text = self.get_text_from_element(expression)
        self.parse_text(head_text, extension_node)

        for child in expression:
            if child.tag == 'path':
                extension_node.path = self.get_text_from_element(child)
            else:
                self.parse_tag_expression(child, extension_node)

            tail_text = self.get_tail_from_element(child)
            self.parse_text(tail_text, extension_node)

    #######################################################################################################
    # EXTENSION_EXPRESSION ::== <log>Message</log>
    #                           <log level="error|warning|debug|info">Message</log>
    #

    def parse_log_expression(self, expression, branch):
        self._parse_node_with_attrib(TemplateLogNode(), expression, branch, "level", "debug")

    #######################################################################################################
    # EVAL_EXPRESSION ::== <eval>TEMPLATE_EXPRESSION</eval>
    #
    # LEARN_PATTERN_EXPRESSION ::== PATTERN_EXPRESSION | EVAL_EXPRESSION
    # LEARN_PATTERN_EXPRESSION ::== (LEARN_PATTERN_EXPRESSION)+
    #
    # LEARN_TEMPLATE_EXPRESSION ::== TEXT | TAG_EXPRESSION | EVAL_EXPRESSION
    #
    # LEARN_TEMPLATE_EXPRESSION ::== (LEARN_TEMPLATE_EXPRESSION)*
    #
    # LEARN_CATEGORY_EXPRESSION ::==
    # 						<category>
    # 							<pattern>LEARN_PATTERN_EXPRESSION</pattern>
    # 							(<that>LEARN_PATTERN_EXPRESSION</that>)
    # 							(<topic>LEARN_PATTERN_EXPRESSION</topic>)
    # 							<template>LEARN_TEMPLATE_EXPRESSION</template>
    # 						</category>
    #
    # LEARN_EXPRESSION ::== 	<learn>LEARN_CATEGORY_EXPRESSION</learn> |
    # 						<learnf>LEARN_CATEGORY_EXPRESSION</learnf>

    def parse_eval_expression(self, expression, branch):

        eval_node = TemplateEvalNode()
        branch.children.append(eval_node)

        head_text = self.get_text_from_element(expression)
        self.parse_text(head_text, eval_node)

        for child in expression:
            self.parse_tag_expression(child, eval_node)

            tail_text = self.get_tail_from_element(child)
            self.parse_text(tail_text, eval_node)

    def parse_learn_expression(self, expression, branch):

        for child in expression:
            if child.tag == 'category':
                learn_node = TemplateLearnNode()

                parsed = self._aiml_parser.parse_category(child, add_to_graph=False)
                learn_node.pattern = parsed[0]
                learn_node.topic = parsed[1]
                learn_node.that = parsed[2]
                learn_node.template = parsed[3]

                branch.children.append(learn_node)

    def parse_learnf_expression(self, expression, branch):

        for child in expression:
            if child.tag == 'category':
                learn_node = TemplateLearnfNode()

                parsed = self._aiml_parser.parse_category(child, add_to_graph=False)
                learn_node.pattern = parsed[0]
                learn_node.topic = parsed[1]
                learn_node.that = parsed[2]
                learn_node.template = parsed[3]

                branch.children.append(learn_node)

    def parse_oob_expression(self, expression, branch):
        raise ParserException("Error, oob not implemented yet!", xml_element=expression)
