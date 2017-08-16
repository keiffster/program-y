import xml.etree.ElementTree as ET

from programy.parser.template.nodes.base import TemplateNode
from programy.parser.template.nodes.tuple import TemplateTupleNode

from test.parser.template.graph_tests.graph_test_client import TemplateGraphTestClient

class TemplateGraphTupleTests(TemplateGraphTestClient):

     def test_tuple_simple(self):

        self.test_bot.brain.rdf.add_entity("MONKEY", "legs", "2")
        self.test_bot.brain.rdf.add_entity("MONKEY", "hasFur", "true")
        self.test_bot.brain.rdf.add_entity("ZEBRA", "legs", "4")
        self.test_bot.brain.rdf.add_entity("BIRD", "legs", "2")
        self.test_bot.brain.rdf.add_entity("ELEPHANT", "trunk", "true")

        template = ET.fromstring("""
                <template>
                  <think>
                     <set var="tuples">
                       <select>
                           <vars>?x</vars>
                           <q><subj>?x</subj><pred>legs</pred><obj>2</obj></q>
                       </select>
                     </set>
                     <set var="head">
                        <first>
                           <get var="tuples"/>
                        </first>
                     </set>
                  </think>
                  <tuple>
                     <get var="head"/>
                  </tuple>
                </template>
                """)

        ast = self.parser.parse_template_expression(template)
        self.assertIsNotNone(ast)

        result = ast.resolve(self.test_bot, self.test_clientid)
        self.assertIsNotNone(result)
        self.assertEquals("", result)
