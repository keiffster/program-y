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
from programy.clients.events.console.client import ConsoleBotClient
from programy.utils.console.console import outputLog
from programy.storage.utils.processors import CSVFileReader


class AutoAnswerConsoleBotClient(ConsoleBotClient):

    def __init__(self, defaults_qandas, argument_parser=None):
        ConsoleBotClient.__init__(self, argument_parser)
        self._qandas = []
        self.load_qandas(defaults_qandas)

    def process_line(self, name, line):
        del name
        if len(line) > 0:
            self._qandas.append([line[0], [x.strip(' "') for x in line[1:]]])

    def load_qandas(self, defaults_qandas):
        if self.arguments.args.qandas is not None:
            try:
                reader = CSVFileReader(self.arguments.args.qandas)
                reader.process_lines("qandas", self)
                return

            except Exception as excep:
                outputLog(self, "Using q&a defaults, as unable to load file [%s], reason[%s]" %
                          (self.arguments.args.qandas, str(excep)))

        self._qandas = defaults_qandas[:]

    def add_client_arguments(self, parser=None):
        if parser is not None:
            parser.add_argument('--qandas', dest='qandas',
                                help='list of questions and answers in csv format '
                                     '[question, answer1, answer2, ... answern]')

    def is_right_answer(self, response, answers):
        if len(answers) == 1:
            if answers[0] == '*':
                if len(response) > 0:
                    return True

        return bool(response in answers)

    def process_question_answer(self, client_context):
        for qanda in self._qandas:
            question = qanda[0]
            answers = qanda[1]
            response = self.process_question(client_context, question)
            if self.is_right_answer(response, answers) is True:
                outputLog(self, "RIGHT - Question=[%s], Answer=[%s]" % (question, response))

            else:
                outputLog(self, "WRONG - Question=[%s], Answer=[%s]" % (question, response))

        raise KeyboardInterrupt()


if __name__ == '__main__':
    outputLog(None, "Initiating Auto Answer Console Client...")

    default_quands = [
        ["Hello", ["*"]],
        ["What are you", ["*"]],
        ["Where are you", ["I'm currently in Kinghorn."]]
    ]

    console_app = AutoAnswerConsoleBotClient(default_quands)
    console_app.run()
