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

class RDFEntity(object):

    def __init__(self, subject=None, predicate=None, object=None):
        self._subject = subject
        self._predicate = predicate
        self._object = object

    @property
    def subject(self):
        return self._subject

    @property
    def predicate(self):
        return self._predicate

    @property
    def object(self):
        return self._object

    def to_xml(self, bot, clientid):
        xml = ""
        xml += "<subj>%s</subj>"%self._subject.to_xml(bot, clientid)
        xml += "<pred>%s</pred>"%self._predicate.to_xml(bot, clientid)
        xml += "<obj>%s</obj>"%self._object.to_xml(bot, clientid)
        return xml

    def to_string(self, resultset):
        str = "( "

        if resultset.subject.startswith("?"):
            str += resultset.subject
        else:
            str += "_"
        str += "="
        str += self.subject

        str += ", "

        if resultset.predicate.startswith("?"):
            str += resultset.predicate
        else:
            str += "_"
        str += "="
        str += self.predicate

        str += ", "

        if resultset.object.startswith("?"):
            str += resultset.object
        else:
            str += "_"
        str += "="
        str += self.object

        str += " )"
        return str
