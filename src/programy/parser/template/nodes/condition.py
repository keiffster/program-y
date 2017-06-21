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

import logging

from programy.parser.template.nodes.base import TemplateNode
from programy.parser.template.nodes.word import TemplateWordNode
from programy.parser.exceptions import ParserException

class TemplateConditionListItemNode(TemplateNode):

    def __init__(self, name=None, value=None, local=False, loop=False):
        TemplateNode.__init__(self)
        self._name = name
        self._value = value
        self._local = local
        self._loop = loop

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        self._name = name

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        self._value = value

    @property
    def local(self):
        return self._local

    @local.setter
    def local(self, local):
        self._local = local

    @property
    def loop(self):
        return self._loop

    @loop.setter
    def loop(self, loop):
        self._loop = loop

    def is_default(self):
        return bool(self.value is None)

    def resolve(self, bot, clientid):
        pass

    def to_string(self):
        if self.name is not None:
            return "[CONDITIONLIST(%s=%s)]" % (self.name, self.value.to_string())
        else:
            if self.value is not None:
                return "[CONDITIONLIST(%s)]" % (self.value.to_string())
            else:
                return "[CONDITIONLIST]"

    def to_xml(self, bot, clientid):
        xml = '<li'
        if self.name is not None:
            if self.local is True:
                xml += ' var="%s"' % self.name
            else:
                xml += ' name="%s"' % self.name
        xml += ">"
        if self.value is not None:
            xml += '<value>'
            xml += self.value.to_xml(bot, clientid)
            xml += '</value>'
        for child in self.children:
            xml += child.to_xml(bot, clientid)
        if self.loop is True:
            xml += "<loop />"
        xml += '</li>'
        return xml

class TemplateConditionNode(TemplateNode):

    def __init__(self, name=None, value=None, local=None, type=1):
        TemplateNode.__init__(self)
        self._name = name
        self._value = value
        self._local = local
        self._type = type

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        self._name = name

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        self._value = value

    @property
    def local(self):
        return self._local

    @local.setter
    def local(self, local):
        self._local = local

    def get_default(self):
        for child in self.children:
            if child.is_default() is True:
                return child
        return None

    def _get_predicate_value(self, bot, clientid, name, local):

        if local is False:
            value = bot.conversation(clientid).predicate(name)
        else:
            value = bot.conversation(clientid).current_question().predicate(name)

        if value is None:
            value = bot.brain.properties.property("default-get")
            if value is None:
                logging.error("No value for default-get defined, empty string returned")
                value = ""
        return value

    #######################################################################################################
    # CONDITION_ITEM_COMPONENT ::== <name>TEMPLATE_EXPRESSION</name> | <value>TEMPLATE_EXPRESSION</value> | <loop/> | TEMPLATE_EXPRESSION
    # CONDITION_ITEM_EXPRESSION ::== <li( CONDITION_ATTRIBUTES)*>(CONDITION_ITEM_COMPONENT)*</li>
    # CONDITION_ATTRIBUTES ::== (name="NAME") | (value="NORMALIZED_TEXT")
    # CONDITION_EXPRESSION ::== <condition( CONDITION_ATTRIBUTES)>(CONDITION_ITEM_EXPRESSION)*</condition>
    #

    def parse_condition_attributes(expression):
        name = None
        value = None

        if 'name' in expression.attrib:
            name = expression['name']
        if 'value' in expression.attrib:
            value = expression['value']

        return name, value

    def get_condition_name(self, condition):
        if 'name' in condition.attrib:
            return condition.attrib['name'], False
        elif 'var' in condition.attrib:
            return condition.attrib['var'], True
        else:
            names = condition.findall('name')
            variables = condition.findall('var')
            if len(names) == 0 and len(variables) == 0:
                return None, False
            elif len(names) > 1:
                raise ParserException("Error, condition element has multiple name elements", xml_element=condition)
            elif len(variables) > 1:
                raise ParserException("Error, condition element has multiple var elements", xml_element=condition)
            else:
                if len(names) == 1:
                    name_text = self.get_text_from_element(condition.find('name'))
                    return name_text, False
                else:
                    var_text = self.get_text_from_element(condition.find('var'))
                    return var_text, True

    def get_condition_value(self, graph, condition):
        if 'value' in condition.attrib:
            value_node = graph.get_base_node()
            value_node.append(graph.get_word_node(condition.attrib['value']))
            return value_node
        else:
            values = condition.findall('value')
            if len(values) == 0:
                return None
            elif len(values) > 1:
                raise ParserException("Error, element has multiple value elements", xml_element=condition)
            else:
                value_node = graph.get_base_node()
                value_node.parse_template_node(graph, values[0])
                return value_node

    # Type 1
    # <condition name="predicate" value="v">X</condition>,
    # <condition name="predicate"><value>v</value>X</condition>,
    # <condition value="v"><name>predicate</name>X</condition>, and
    # <condition><name>predicate</name><value>v</value>X</condition>
    #

    # Type 2
    # <condition name="predicate">...</condition>
    # <condition><name>predicate</name>...</condition>
    # 	<li value="a">X</li>
    # 	<li value="b">Y</li>
    # 	<li>Z</li>				<- Default value if no condition met
    #

    # Type 3
    #  <condition>
    # 	<li name='1' value="a">X</li>
    # 	<li value="b"><name>1</name>Y</li>
    # 	<li name="1"><value>b</value>Z</li>
    # 	<li><name>1</name><value>b</value>Z</li>
    # 	<li>Z<l/i>				<- Default value if no condition met
    #  </condition>
    #

    def parse_expression(self, graph, expression):

        name, local = self.get_condition_name(expression)
        value = self.get_condition_value(graph, expression)

        if name is not None:
            self.name = name
            self.local = local
            if value is not None:
                self._type = 1
                self.value = value
                self.parse_type1_condition(graph, expression)
            else:
                self._type = 2
                self.parse_type2_condition(graph, expression)
        else:
            self._type = 3
            self.parse_type3_condition(graph, expression)

    def parse_type1_condition(self, graph, expression):
        self.parse_text(graph, self.get_text_from_element(expression))

        for child in expression:
            if child.tag == 'name':
                pass

            elif child.tag == 'var':
                pass

            elif child.tag == 'value':
                pass

            elif child.tag == 'li':
                raise ParserException("Error, li element not allowed as child of condition element",
                                      xml_element=expression)

            elif child.tag == 'loop':
                raise ParserException("Error, this type of condition cannot have <loop /> element",
                                      xml_element=expression)

            else:
                graph.parse_tag_expression(child, self)

            tail_text = self.get_tail_from_element(child)
            self.parse_text(graph, tail_text)

    def parse_type2_condition(self, graph, expression):

        for child in expression:
            if child.tag == 'name':
                # Pass on this attribute as we have already pulled it from the get_condition_name above
                pass

            elif child.tag == 'var':
                # Pass on this attribute as we have already pulled it from the get_condition_name above
                pass

            elif child.tag == 'li':

                list_item = TemplateConditionListItemNode()

                list_item.value = self.get_condition_value(graph, child)
                list_item.local = self.local

                self.children.append(list_item)
                list_item.parse_text(graph, self.get_text_from_element(child))

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
                        graph.parse_tag_expression(sub_pattern, list_item)

                    tail_text = self.get_tail_from_element(sub_pattern)
                    list_item.parse_text(graph, tail_text)

            else:
                raise ParserException("Error, invalid element <%s> in condition element" % (child.tag),
                                      xml_element=expression)

    def parse_type3_condition(self, graph, expression):
        for child in expression:

            if child.tag == 'name':
                pass

            elif child.tag == 'var':
                pass

            elif child.tag == 'li':
                list_item = TemplateConditionListItemNode()

                response = self.get_condition_name(child)
                list_item.name = response[0]
                list_item.local = response[1]

                list_item.value = self.get_condition_value(graph, child)

                self.children.append(list_item)

                list_item.parse_text(graph, self.get_text_from_element(child))

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
                        graph.parse_tag_expression(sub_pattern, list_item)

                    tail_text = self.get_tail_from_element(sub_pattern)
                    list_item.parse_text(graph, tail_text)

            else:
                raise ParserException("Error, invalid element <%s> in condition element" % (child.tag), xml_element=expression)


    def to_string(self):
        text = "[CONDITION"
        if self.name is not None:
            text += " name=%s"%(self.name)
        if self.name is not None:
            text += " value=%s" % (self.value)
        text += "]"
        return text

    def to_xml(self, bot, clientid):
        xml = "<condition"

        if self.name is not None:
            if self.local is True:
                xml += ' var="%s"' % self.name
            else:
                xml += ' name="%s"' % self.name

        xml += ">"

        if self.value is not None:
            xml += '<value>'
            xml += self.value.to_xml(bot, clientid)
            xml += '</value>'

        for child in self.children:
            xml += child.to_xml(bot, clientid)

        xml += "</condition>"

        return xml


    def resolve(self, bot, clientid):
        if self._type == 1:
            return self.resolve_type1_condition(bot, clientid)
        elif self._type == 2:
            return self.resolve_type2_condition(bot, clientid)
        elif self._type == 3:
            return self.resolve_type3_condition(bot, clientid)
        else:
            return None

    def resolve_type1_condition(self, bot, clientid):
        try:
            value = self._get_predicate_value(bot, clientid, self.name, self.local)

            # Condition comparison is always case insensetive
            if value.upper() == self.value.resolve(bot, clientid).upper():
                resolved = " ".join([child.resolve(bot, clientid) for child in self.children])
            else:
                resolved = ""

            logging.debug("[%s] resolved to [%s]", self.to_string(), resolved)
            return resolved
        except Exception as excep:
            logging.exception(excep)
            return ""

    def resolve_type2_condition(self, bot, clientid):
        try:
            value = self._get_predicate_value(bot, clientid, self.name, self.local)

            for condition in self.children:
                if condition.is_default() is False:
                    condition_value = condition.value.resolve(bot, clientid)

                    # Condition comparison is always case insensetive
                    if value.upper() == condition_value.upper():
                        resolved = " ".join([child_node.resolve(bot, clientid) for child_node in condition.children])
                        logging.debug("[%s] resolved to [%s]", self.to_string(), resolved)

                        if condition.loop is True:
                            resolved = resolved.strip() + " " + self.resolve(bot, clientid)

                        return resolved

            default = self.get_default()
            if default is not None:
                resolved = " ".join([child_node.resolve(bot, clientid) for child_node in default.children])

                if default.loop is True:
                    resolved = resolved.strip() + " " + self.resolve(bot, clientid)
            else:
                resolved = ""

            logging.debug("[%s] resolved to [%s]", self.to_string(), resolved)
            return resolved

        except Exception as excep:
            logging.exception(excep)
            return ""

    def resolve_type3_condition(self, bot, clientid):
        try:
            for condition in self.children:
                value = self._get_predicate_value(bot, clientid, condition.name, condition.local)
                if condition.value is not None:
                    condition_value = condition.value.resolve(bot, clientid)

                    # Condition comparison is always case insensetive
                    if value.upper() == condition_value.upper():
                        resolved = " ".join([child_node.resolve(bot, clientid) for child_node in condition.children])
                        logging.debug("[%s] resolved to [%s]", self.to_string(), resolved)

                        if condition.loop is True:
                            resolved = resolved.strip() + " " + self.resolve(bot, clientid).strip()

                        return resolved

            default = self.get_default()
            if default is not None:
                resolved = " ".join([child_node.resolve(bot, clientid) for child_node in default.children])

                if default.loop is True:
                    resolved = resolved.strip() + " " + self.resolve(bot, clientid).strip()

            else:
                resolved = ""

            logging.debug("[%s] resolved to [%s]", self.to_string(), resolved)
            return resolved

        except Exception as excep:
            logging.exception(excep)
            return ""



