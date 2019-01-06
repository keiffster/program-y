"""
Copyright (c) 2016-2019 Keith Sterling http://www.keithsterling.com

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated
documentation files (the "Software"), to deal in the Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software,
and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions
of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO
THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

"""
from programy.utils.logging.ylogger import YLogger

from programy.extensions.base import Extension


class RDFAdminExtension(Extension):

    # execute() is the interface that is called from the <extension> tag in the AIML
    def execute(self, client_context, data):
        YLogger.debug(client_context, "RDF Admin - [%s]", data)

        rdf = ""
        segments = data.split()
        if segments[0] == 'SUBJECTS':
            subjects = client_context.brain.rdf.subjects()
            if segments[1] == 'LIST':
                rdf += "<ul>"
                for subject in subjects:
                    rdf += "<li>%s</li>"%subject
                rdf += "</ul>"
            else:
                return str(len(subjects))

        elif segments[0] == "PREDICATES":
            subject = segments[1]
            predicates = client_context.brain.rdf.predicates(subject)
            rdf += "<ul>"
            for predicate in predicates:
                rdf += "<li>%s</li>" % predicate
            rdf += "</ul>"

        elif segments[0] == "OBJECT":
            subject = segments[1]
            predicate = segments[2]
            objects =  client_context.brain.rdf.objects(subject, predicate)
            rdf += "<ul>"
            for object in objects:
                for obj in object:
                    rdf += "<li>%s</li>" % obj
            rdf += "</ul>"

        return rdf