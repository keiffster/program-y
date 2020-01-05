"""
Copyright (c) 2016-2020 Keith Sterling http://www.keithsterling.com

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
import re
from programy.utils.parsing.linenumxml import LineNumberingParser
import xml.etree.ElementTree as ET  # pylint: disable=wrong-import-order
from programy.utils.logging.ylogger import YLogger
from programy.storage.entities.store import Store
from programy.parser.exceptions import ParserException
from programy.parser.exceptions import DuplicateGrammarException
from programy.utils.text.text import TextUtils


class CategoryReadOnlyStore(Store):
    WHITESPACE = re.compile('[\n\t\r+]')

    def __init__(self):
        Store.__init__(self)

    def load_all(self, collector):
        raise NotImplementedError("load_all missing from Category Store")  # pragma: no cover

    def load(self, collector, name=None):
        raise NotImplementedError("load missing from Category Store")  # pragma: no cover

    @staticmethod
    def extract_content(name, element):
        content = ET.tostring(element, encoding='utf-8', method='xml').decode('utf-8')
        content = CategoryReadOnlyStore.WHITESPACE.sub('', content)
        content = content.replace('<br>', '<br />')
        content = re.sub(r'\s+', ' ', content)
        start = '<%s>' % name
        end = '</%s>' % name
        firstpos = content.find(start)
        lastpos = content.rfind(end)

        if firstpos == -1 or lastpos == -1:
            return None

        return content[firstpos + len(start):lastpos]

    def find_all(self, element, name, namespace=None):
        if namespace is not None:
            search = "%s:%s"%(list(namespace.keys())[0], name)
            return element.findall(search, namespaces=namespace)
        return element.findall(name)

    def find_element_str(self, name, xml, namespace=None):
        elements = self.find_all(xml, name, namespace)
        if len(elements) > 1:
            raise Exception("Multiple <%s> nodes found in category" % name)

        elif len(elements) == 1:
            return CategoryReadOnlyStore.extract_content(name, elements[0])

        return "*"

    def _load_category(self, groupid, pattern, topic, that, template, parser):

        text = """
<category>
    <pattern>%s</pattern>
    <topic>%s</topic>
    <that>%s</that>
    <template>%s</template>
</category>""" % (pattern, topic, that, template)

        xml = None
        try:
            xml = ET.fromstring(text)
            parser.parse_category(xml, None)

        except DuplicateGrammarException as dupe_excep:
            parser.handle_aiml_duplicate(dupe_excep, groupid, xml)

        except ParserException as parser_excep:
            parser.handle_aiml_error(parser_excep, groupid, xml)

        except Exception as excep:
            YLogger.exception_nostack(self, "Error loading category from db", excep)


class CategoryReadWriteStore(CategoryReadOnlyStore):

    def __init__(self):
        CategoryReadOnlyStore.__init__(self)

    def _parse_topic_expression(self, expression, namespace, groupname, count, success):
        topic = expression.attrib['name']
        for topic_expression in expression:
            that = self.find_element_str("that", topic_expression, namespace)
            pattern = self.find_element_str("pattern", topic_expression, namespace)
            template = self.find_element_str("template", topic_expression, namespace)
            if self.store_category(groupname, "*", topic, that, pattern, template) is True:
                success += 1
            count += 1
        return count, success

    def _parse_category_expression(self, expression, namespace, groupname, count, success):
        topic = self.find_element_str("topic", expression, namespace)
        that = self.find_element_str("that", expression, namespace)
        pattern = self.find_element_str("pattern", expression, namespace)
        template = self.find_element_str("template", expression, namespace)
        if self.store_category(groupname, "*", topic, that, pattern, template) is True:
            success += 1
        count += 1
        return count, success

    def _upload(self, filename):
        count = 0
        success = 0
        groupname = Store.get_just_filename_from_filepath(filename)

        tree = ET.parse(filename, parser=LineNumberingParser())
        aiml = tree.getroot()

        for expression in aiml:
            tag_name, namespace = TextUtils.tag_and_namespace_from_text(expression.tag)

            if tag_name == 'topic':
                count, success = self._parse_topic_expression(expression, namespace, groupname, count, success)

            elif tag_name == 'category':
                count, success = self._parse_category_expression(expression, namespace, groupname, count, success)

            else:
                YLogger.error(self, "Invalid aiml tag type [%s]", tag_name)
                count += 1

        return count, success

    def upload_from_file(self, filename, fileformat=Store.XML_FORMAT, commit=True, verbose=False):
        try:
            return self._upload(filename)

        except Exception as excep:
            YLogger.exception(self, "Failed to load contents of AIML file from [%s]",
                              excep, filename)  # pragma: no cover

        return 0, 0

    def store_category(self, groupid, userid, topic, that, pattern, template):
        raise NotImplementedError("store_category missing from Category Store")  # pragma: no cover
