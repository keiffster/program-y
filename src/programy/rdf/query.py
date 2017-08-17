"""
Copyright (c) 2016-17 Keith Sterling http://www.keithsterling.com

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


from programy.rdf.resultset import RDFQueryResultSet

class RDFQuery(object):

    QUERY = 1
    NOT_QUERY = 2

    def __init__(self, subject, predicate, object, query_type=QUERY):
        self._subject_node = subject
        self._predicate_node = predicate
        self._object_node = object
        self._query_type = query_type

    @property
    def subject(self):
        return self._subject_node

    @property
    def predicate(self):
        return self._predicate_node

    @property
    def object(self):
        return self._object_node

    @property
    def query_type(self):
        return self._query_type

    def to_xml(self, bot, clientid):
        xml = ""
        if self.query_type == RDFQuery.QUERY:
            xml += "<q>"
        else:
            xml += "<notq>"
        xml += "<subj>%s</subj>"%self._subject_node.to_xml(bot, clientid)
        xml += "<pred>%s</pred>"%self._predicate_node.to_xml(bot, clientid)
        xml += "<obj>%s</obj>"%self._object_node.to_xml(bot, clientid)
        if self.query_type == RDFQuery.QUERY:
            xml += "</q>"
        else:
            xml += "</notq>"
        return xml

    def to_string(self, bot, clientid):
        subject = self._subject_node.resolve(bot, clientid)
        predicate = self._predicate_node.resolve(bot, clientid)
        object = self._object_node.resolve(bot, clientid)

        str = ""
        if self.query_type == RDFQuery.QUERY:
            str += "query=( "
        else:
            str += "not=( "

        str += "subj=" + subject + ", "
        str += "pred=" + predicate + ", "
        str += "obj=" + object

        str += " )"

        return str

    def get_parameter_value(self, name, parameters):
        for pair in parameters:
            if name == pair[0]:
                return pair[1]
        return None

    def execute(self, bot, clientid, parameters=None):

        subject = self._subject_node.resolve(bot, clientid)
        predicate = self._predicate_node.resolve(bot, clientid)
        object = self._object_node.resolve(bot, clientid)

        # Now see if any are variables rather than data
        if subject.startswith("?"):
            if parameters is not None:
                subj_val = self.get_parameter_value(subject, parameters)
            else:
                subj_val = None
        else:
            subj_val = subject

        if predicate.startswith("?"):
            if parameters is not None:
                pred_val = self.get_parameter_value(predicate, parameters)
            else:
                pred_val = None
        else:
            pred_val = predicate

        if object.startswith("?"):
            if parameters is not None:
                obj_val = self.get_parameter_value(object, parameters)
            else:
                obj_val = None
        else:
            obj_val = object

        # Query using subj, pred and obj data
        if self.query_type == RDFQuery.QUERY:
            entities = bot.brain.rdf.match(subject=subj_val, predicate=pred_val, object=obj_val)
        else:
            entities = bot.brain.rdf.not_match(subject=subj_val, predicate=pred_val, object=obj_val)

        results = []
        for entity in entities:
            result = []
            if subject.startswith("?"):
                result.append([subject, entity.subject])
            else:
                result.append([None, entity.subject])

            if predicate.startswith("?"):
                result.append([predicate, entity.predicate])
            else:
                result.append([None, entity.predicate])

            if object.startswith("?"):
                result.append([object, entity.object])
            else:
                result.append([None, entity.object])

            results.append(result)

        return RDFQueryResultSet(subject, predicate, object, results)

