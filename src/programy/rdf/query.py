"""
Copyright (c) 2016-17 Keith Sterling http://www.keithsterling.com

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


from programy.rdf.resultset import RDFQueryResultSet

class RDFQuery(object):

    QUERY = 1
    NOT_QUERY = 2

    def __init__(self, rdf_subject, rdf_predicate, rdf_object, query_type=QUERY):
        self._subject_node = rdf_subject
        self._predicate_node = rdf_predicate
        self._object_node = rdf_object
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
        rdf_subject = self._subject_node.resolve(bot, clientid)
        rdf_predicate = self._predicate_node.resolve(bot, clientid)
        rdf_object = self._object_node.resolve(bot, clientid)

        string = ""
        if self.query_type == RDFQuery.QUERY:
            string += "query=( "
        else:
            string += "not=( "

        string += "subj=" + rdf_subject + ", "
        string += "pred=" + rdf_predicate + ", "
        string += "obj=" + rdf_object

        string += " )"

        return string

    @staticmethod
    def get_parameter_value(name, parameters):
        for pair in parameters:
            if name == pair[0]:
                return pair[1]
        return None

    def execute(self, bot, clientid, parameters=None):

        rdf_subject = self._subject_node.resolve(bot, clientid)
        rdf_predicate = self._predicate_node.resolve(bot, clientid)
        rdf_object = self._object_node.resolve(bot, clientid)

        # Now see if any are variables rather than data
        if rdf_subject.startswith("?"):
            if parameters is not None:
                subj_val = RDFQuery.get_parameter_value(rdf_subject, parameters)
            else:
                subj_val = None
        else:
            subj_val = rdf_subject

        if rdf_predicate.startswith("?"):
            if parameters is not None:
                pred_val = RDFQuery.get_parameter_value(rdf_predicate, parameters)
            else:
                pred_val = None
        else:
            pred_val = rdf_predicate

        if rdf_object.startswith("?"):
            if parameters is not None:
                obj_val = RDFQuery.get_parameter_value(rdf_object, parameters)
            else:
                obj_val = None
        else:
            obj_val = rdf_object

        # Query using subj, pred and obj data
        if self.query_type == RDFQuery.QUERY:
            entities = bot.brain.rdf.match(rdf_subject=subj_val, rdf_predicate=pred_val, rdf_object=obj_val)
        else:
            entities = bot.brain.rdf.not_match(rdf_subject=subj_val, rdf_predicate=pred_val, rdf_object=obj_val)

        results = []
        for entity in entities:
            result = []
            if rdf_subject.startswith("?"):
                result.append([rdf_subject, entity.subject])
            else:
                result.append([None, entity.subject])

            if rdf_predicate.startswith("?"):
                result.append([rdf_predicate, entity.predicate])
            else:
                result.append([None, entity.predicate])

            if rdf_object.startswith("?"):
                result.append([rdf_object, entity.object])
            else:
                result.append([None, entity.object])

            results.append(result)

        return RDFQueryResultSet(rdf_subject, rdf_predicate, rdf_object, results)
