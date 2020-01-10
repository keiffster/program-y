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
import os
from programy.clients.embed.datafile import EmbeddedDataFileBot
from programy.clients.args import CommandLineClientArguments


class EmbeddedBasicBot(EmbeddedDataFileBot):

    def __init__(self, logging_filename=None):
        filepath = os.path.dirname(__file__) + os.sep
        if logging_filename is not None:
            self._logging_filename = logging_filename
        else:
            self._logging_filename = filepath + 'basicbot/logging.yaml'

        files = {'aiml': [filepath + 'basicbot/categories'],
                 'learnf': [filepath + 'basicbot/learnf'],
                 'patterns': filepath + 'basicbot/nodes/pattern_nodes.conf',
                 'templates': filepath + 'basicbot/nodes/template_nodes.conf',
                 'properties': filepath + 'basicbot/properties/properties.txt',
                 'defaults': filepath + 'basicbot/properties/defaults.txt',
                 'sets': [filepath + 'basicbot/sets'],
                 'maps': [filepath + 'basicbot/maps'],
                 'rdfs': [filepath + 'basicbot/rdfs'],
                 'denormals': filepath + 'basicbot/lookups/denormal.txt',
                 'normals': filepath + 'basicbot/lookups/normal.txt',
                 'genders': filepath + 'basicbot/lookups/gender.txt',
                 'persons': filepath + 'basicbot/lookups/person.txt',
                 'person2s': filepath + 'basicbot/lookups/person2.txt',
                 'regexes': filepath + 'basicbot/regex/regex-templates.txt',
                 'spellings': filepath + 'basicbot/spelling/corpus.txt',
                 'preprocessors': filepath + 'basicbot/processing/preprocessors.conf',
                 'postprocessors': filepath + 'basicbot/processing/postprocessors.conf',
                 'postquestionprocessors': filepath + 'basicbot/processing/postquestionprocessors.conf'
                 }
        EmbeddedDataFileBot.__init__(self, files)

    def parse_arguments(self, argument_parser):
        client_args = CommandLineClientArguments(self, parser=None)
        if self._logging_filename is not None:
            client_args._logging = self._logging_filename
        return client_args

if __name__ == '__main__':

    print("Loading Bot Brain....please wait!")
    my_bot = EmbeddedBasicBot()

    print("Asked 'Hello', Response '%s'" % my_bot.ask_question("Hello"))
    print("Asked 'What are you', Response '%s'" % my_bot.ask_question("What are you"))
    print("Asked 'Where are you',  Response '%s'" % my_bot.ask_question("Where are you"))

