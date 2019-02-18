"""
Copyright (c) 2016-2019 Keith Sterling http://www.keithsterling.com

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated
documentation files (the "Software"), to deal in the Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software,
and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the
Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO
THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""

from programy.utils.logging.ylogger import YLogger

from programy.parser.template.nodes.base import TemplateNode
from programy.parser.template.nodes.get import TemplateGetNode
from programy.parser.template.nodes.bot import TemplateBotNode
from programy.parser.exceptions import ParserException
from programy.utils.text.text import TextUtils

class TemplateConditionVariable(TemplateNode):

    DEFAULT = 0
    GLOBAL = 1
    LOCAL = 2
    BOT = 3

    def __init__(self, name=None, value=None, var_type=GLOBAL, loop=False):
        TemplateNode.__init__(self)
        self._name = name
        self._value = value
        self._var_type = var_type
        self._loop = loop

    @property
    def name(self):
        return self._name

    @property
    def value(self):
        return self._value

    @property
    def var_type(self):
        return self._var_type

    @property
    def loop(self):
        return self._loop

    @loop.setter
    def loop(self, loop):
        self._loop = loop


class TemplateConditionListItemNode(TemplateConditionVariable):

    def __init__(self, name=None, value=None, var_type=TemplateConditionVariable.GLOBAL, loop=False):
        TemplateConditionVariable.__init__(self, name, value, var_type, loop)

    def is_default(self):
        return bool(self.value is None)

    def to_string(self):
        if self.name is not None:
            return "[CONDITIONLIST(%s=%s)]" % (self.name, self.value.to_string())
        if self.value is not None:
            return "[CONDITIONLIST(%s)]" % (self.value.to_string())
        return "[CONDITIONLIST]"

    def to_xml(self, client_context):

        xml = '<li'
        if self.name is not None:
            if self.var_type == TemplateConditionListItemNode.GLOBAL:
                xml += ' name="%s"' % self.name
            elif self.var_type == TemplateConditionListItemNode.LOCAL:
                xml += ' var="%s"' % self.name
            elif self.var_type == TemplateConditionListItemNode.BOT:
                xml += ' bot="%s"' % self.name
            elif self.var_type == TemplateConditionListItemNode.DEFAULT:
                xml += ' default="%s"' % self.name
            else:
                xml += ' unknown="%s"' % self.name
        xml += ">"

        if self.value is not None:
            xml += '<value>'
            xml += self.value.to_xml(client_context)
            xml += '</value>'

        xml += self.children_to_xml(client_context)

        if self.loop is True:
            xml += "<loop />"

        xml += '</li>'

        return xml


class TemplateConditionNode(TemplateConditionVariable):

    BLOCK = 1
    SINGLE = 2
    MULTIPLE = 3

    def __init__(self, name=None, value=None, var_type=TemplateConditionVariable.GLOBAL, loop=False, condition_type=BLOCK):
        TemplateConditionVariable.__init__(self, name, value, var_type, loop)
        self._condition_type = condition_type

    def get_default(self):
        for child in self.children:
            if child.is_default() is True:
                return child
        return None

    #######################################################################################################
    # CONDITION_ITEM_COMPONENT ::== <name>TEMPLATE_EXPRESSION</name> | <value>TEMPLATE_EXPRESSION</value> | <loop/> | TEMPLATE_EXPRESSION
    # CONDITION_ITEM_EXPRESSION ::== <li( CONDITION_ATTRIBUTES)*>(CONDITION_ITEM_COMPONENT)*</li>
    # CONDITION_ATTRIBUTES ::== (name="NAME") | (value="NORMALIZED_TEXT")
    # CONDITION_EXPRESSION ::== <condition( CONDITION_ATTRIBUTES)>(CONDITION_ITEM_EXPRESSION)*</condition>
    #

    def get_condition_name(self, condition):

        if 'name' in condition.attrib:
            return condition.attrib['name'], TemplateConditionVariable.GLOBAL

        elif 'var' in condition.attrib:
            return condition.attrib['var'], TemplateConditionVariable.LOCAL

        elif 'bot' in condition.attrib:
            return condition.attrib['bot'], TemplateConditionVariable.BOT

        else:
            names = condition.findall('name')
            if names:
                if len(names) > 1:
                    raise ParserException("Condition element has multiple name elements", xml_element=condition)
                name_text = self.get_text_from_element(condition.find('name'))
                return name_text, TemplateConditionVariable.GLOBAL

            vars = condition.findall('var')
            if vars:
                if len(vars) > 1:
                    raise ParserException("Condition element has multiple var elements", xml_element=condition)
                var_text = self.get_text_from_element(condition.find('var'))
                return var_text, TemplateConditionVariable.LOCAL

            bots = condition.findall('bot')
            if bots:
                if len(bots) > 1:
                    raise ParserException("Condition element has multiple bot elements", xml_element=condition)
                bot_text = self.get_text_from_element(condition.find('bot'))
                return bot_text, TemplateConditionVariable.BOT

        return None, TemplateConditionVariable.DEFAULT

    def get_condition_value(self, graph, condition):

        if 'value' in condition.attrib:
            value_node = graph.get_base_node()
            value_node.append(graph.get_word_node(condition.attrib['value']))
            return value_node
        else:
            values = condition.findall('value')
            if not values:
                return None
            elif len(values) > 1:
                raise ParserException("Element has multiple value elements", xml_element=condition)
            value_node = graph.get_base_node()
            value_node.parse_template_node(graph, values[0])
            return value_node

    # Type 1
    # <condition name="property" value="v">X</condition>,
    # <condition name="property"><value>v</value>X</condition>,
    # <condition value="v"><name>property</name>X</condition>, and
    # <condition><name>property</name><value>v</value>X</condition>
    #

    # Type 2
    # <condition name="property">
    # 	<li value="a">X</li>
    # 	<li value="b">Y</li>
    # 	<li>Z</li>				        <- Optional default value if no condition met
    # </ condition>
    # <condition name="property">
    # 	<li value="a">X</li>
    # 	<li value="b">Y</li>
    # 	<loop />				        <- Loop if no condition met
    # </ condition>
    # <condition name="property">
    # 	<li value="a">X</li>
    # 	<li value="b">Y <loop /></li>   <- Loop if condition set
    # </ condition>
    # or
    #
    # <condition>
    #   <name>property</name>
    # 	<li value="a">X</li>
    # 	<li value="b">Y</li>
    # 	<li>Z</li>				        <- Optional default value if no condition met
    # </ condition>
    #

    # Type 3
    #  <condition>
    # 	<li name='1' value="a">X</li>
    # 	<li value="b"><name>1</name>Y</li>
    # 	<li name="1"><value>b</value>Z</li>
    # 	<li><name>1</name><value>b</value>Z</li>
    # 	<li>Z<l/i>				        <- Optional default value if no condition met
    #  </condition>
    #

    def parse_expression(self, graph, expression):

        name, var_type = self.get_condition_name(expression)
        value = self.get_condition_value(graph, expression)

        if name is not None:
            self._name = name
            self._var_type = var_type
            if value is not None:
                self._condition_type = TemplateConditionNode.BLOCK
                self._value = value
                self.parse_type1_condition(graph, expression)
            else:
                self._condition_type = TemplateConditionNode.SINGLE
                self.parse_type2_condition(graph, expression)
        else:
            self._condition_type = TemplateConditionNode.MULTIPLE
            self.parse_type3_condition(graph, expression)

    def parse_type1_condition(self, graph, expression):
        self.parse_text(graph, self.get_text_from_element(expression))

        for child in expression:
            tag_name = TextUtils.tag_from_text(child.tag)

            if tag_name in ['name', 'var', 'bot', 'value']:
                pass

            elif tag_name == 'li':
                raise ParserException("li element not allowed as child of condition element",
                                      xml_element=expression)

            elif tag_name == 'loop':
                raise ParserException("This type of condition cannot have <loop /> element",
                                      xml_element=expression)

            else:
                graph.parse_tag_expression(child, self)

            tail_text = self.get_tail_from_element(child)
            self.parse_text(graph, tail_text)

    def parse_type2_condition(self, graph, expression):

        for child in expression:
            tag_name = TextUtils.tag_from_text(child.tag)

            if tag_name in ['name', 'var', 'bot']:
                pass

            elif tag_name == 'li':

                list_item = TemplateConditionListItemNode()

                list_item._value = self.get_condition_value(graph, child)
                list_item._var_type = self._var_type

                self.children.append(list_item)
                list_item.parse_text(graph, self.get_text_from_element(child))

                for sub_pattern in child:

                    if sub_pattern.tag in ['name', 'var', 'bot', 'value']:
                        pass

                    elif sub_pattern.tag == 'loop':
                        list_item.loop = True

                    else:
                        graph.parse_tag_expression(sub_pattern, list_item)

                    tail_text = self.get_tail_from_element(sub_pattern)
                    list_item.parse_text(graph, tail_text)

            else:
                raise ParserException("Invalid element <%s> in condition element" % (tag_name),
                                      xml_element=expression)

    def parse_type3_condition(self, graph, expression):
        for child in expression:
            tag_name = TextUtils.tag_from_text(child.tag)

            if tag_name in ['name', 'var', 'bot']:
                pass

            elif tag_name == 'li':
                list_item = TemplateConditionListItemNode()

                name, var_type = self.get_condition_name(child)
                list_item._name = name
                list_item._var_type = var_type

                list_item._value = self.get_condition_value(graph, child)

                self.children.append(list_item)

                list_item.parse_text(graph, self.get_text_from_element(child))

                for sub_pattern in child:
                    if sub_pattern.tag in ['name', 'var', 'bot', 'value']:
                        pass

                    elif sub_pattern.tag == 'loop':
                        list_item.loop = True

                    else:
                        graph.parse_tag_expression(sub_pattern, list_item)

                    tail_text = self.get_tail_from_element(sub_pattern)
                    list_item.parse_text(graph, tail_text)

            else:
                raise ParserException("Invalid element <%s> in condition element" % (tag_name), xml_element=expression)


    def to_string(self):
        text = "[CONDITION"
        if self.var_type == TemplateConditionListItemNode.GLOBAL:
            text += ' name="%s"' % self.name
        elif self.var_type == TemplateConditionListItemNode.LOCAL:
            text += ' var="%s"' % self.name
        elif self.var_type == TemplateConditionListItemNode.BOT:
            text += ' bot="%s"' % self.name
        else:
            text += ' unknown="%s"' % self.name
        if self.value is not None:
            text += " value=%s" % (self.value)
        text += "]"
        return text

    def to_xml(self, client_context):
        xml = "<condition"

        if self.name is not None:
            if self.var_type == TemplateConditionListItemNode.GLOBAL:
                xml += ' name="%s"' % self.name
            elif self.var_type == TemplateConditionListItemNode.LOCAL:
                xml += ' var="%s"' % self.name
            elif self.var_type == TemplateConditionListItemNode.BOT:
                xml += ' bot="%s"' % self.name
            else:
                xml += ' unknown="%s"' % self.name

        xml += ">"

        if self.value is not None:
            xml += '<value>'
            xml += self.value.to_xml(client_context)
            xml += '</value>'

        xml += self.children_to_xml(client_context)

        xml += "</condition>"

        return xml

    def resolve(self, client_context):
        if self._condition_type == TemplateConditionNode.BLOCK:
            return self.resolve_type1_condition(client_context)
        elif self._condition_type == TemplateConditionNode.SINGLE:
            return self.resolve_type2_condition(client_context)
        elif self._condition_type == TemplateConditionNode.MULTIPLE:
            return self.resolve_type3_condition(client_context)
        return None

    def get_condition_variable_value(self, client_context, var_type, name):
        if var_type == TemplateConditionVariable.GLOBAL:
            return TemplateGetNode.get_property_value(client_context, False, name)
        elif var_type == TemplateConditionVariable.LOCAL:
            return TemplateGetNode.get_property_value(client_context, True, name)
        elif var_type == TemplateConditionVariable.BOT:
            return TemplateBotNode.get_bot_variable(client_context, name)
        else:
            return"unknown"

    def resolve_type1_condition(self, client_context):
        try:
            value = self.get_condition_variable_value(client_context, self.var_type, self.name)
            condition_value = self.value.resolve(client_context).upper()

            # Condition comparison is always case insensetive
            if value.upper() == condition_value:
                resolved = client_context.brain.tokenizer.words_to_texts([child.resolve(client_context) for child in self.children])
            else:
                resolved = ""

            YLogger.debug(client_context, "[%s] resolved to [%s]", self.to_string(), resolved)
            return resolved

        except Exception as excep:
            YLogger.exception(client_context, "Failed to resolve type1 condition", excep)
            return ""

    def resolve_type2_condition(self, client_context):
        try:
            value = self.get_condition_variable_value(client_context, self.var_type, self.name)

            for condition in self.children:
                if condition.is_default() is False:
                    condition_value = condition.value.resolve(client_context)

                    # Condition comparison is always case insensetive
                    if client_context.brain.tokenizer.compare(value.upper(), condition_value.upper()):
                        resolved = client_context.brain.tokenizer.words_to_texts([child_node.resolve(client_context) for child_node in condition.children])
                        YLogger.debug(client_context, "[%s] resolved to [%s]", self.to_string(), resolved)

                        if condition.loop is True:
                            resolved = resolved.strip() + " " + self.resolve(client_context)

                        return resolved

            default = self.get_default()
            if default is not None:
                resolved = client_context.brain.tokenizer.words_to_texts([child_node.resolve(client_context) for child_node in default.children])

                if default.loop is True:
                    resolved = resolved.strip() + " " + self.resolve(client_context)
            else:
                resolved = ""

            YLogger.debug(client_context, "[%s] resolved to [%s]", self.to_string(), resolved)
            return resolved

        except Exception as excep:
            YLogger.exception(client_context, "Failed to resolve type2 condition", excep)
            return ""

    def resolve_type3_condition(self, client_context):
        try:
            for condition in self.children:
                value = self.get_condition_variable_value(client_context, condition.var_type, condition.name)
                if condition.value is not None:
                    condition_value = condition.value.resolve(client_context)

                    # Condition comparison is always case insensetive
                    if value.upper() == condition_value.upper():
                        resolved = client_context.brain.tokenizer.words_to_texts([child_node.resolve(client_context) for child_node in condition.children])
                        YLogger.debug(client_context, "[%s] resolved to [%s]", self.to_string(), resolved)

                        if condition.loop is True:
                            resolved = resolved.strip() + " " + self.resolve(client_context).strip()

                        return resolved

            default = self.get_default()
            if default is not None:
                resolved = client_context.brain.tokenizer.words_to_texts([child_node.resolve(client_context) for child_node in default.children])

                if default.loop is True:
                    resolved = resolved.strip() + " " + self.resolve(client_context).strip()

            else:
                resolved = ""

            YLogger.debug(client_context, "[%s] resolved to [%s]", self.to_string(), resolved)
            return resolved

        except Exception as excep:
            YLogger.exception(client_context, "Failed to resolve type3 condition", excep)
            return ""
