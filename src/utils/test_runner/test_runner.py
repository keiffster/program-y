import csv
import re
import datetime

from programy.clients.client import BotClient
from programy.utils.files.filefinder import FileFinder
from programy.clients.events.console.config import ConsoleConfiguration

class TestQuestion(object):

    def __init__(self, question, answers, topic=None, that=None):
        self._category = None
        self._question = question
        self._answers = answers
        self._answers_regex = []
        self._topic = topic
        self._that = that
        for answer in answers:
            if answer is not None and answer:
                if answer[0] == "!":
                    self._answers_regex.append(("-", re.compile(answer)))
                else:
                    self._answers_regex.append(("+", re.compile(answer)))
        self._response = None

    @property
    def category(self):
        return self._category

    @category.setter
    def category(self, category):
        self._category = category

    @property
    def question(self):
        return self._question

    @property
    def answers(self):
        return self._answers

    @property
    def answers_regex(self):
        return self._answers_regex

    @property
    def answers_string(self):
        return " or ".join(self._answers)

    @property
    def response(self):
        return self._response

    @response.setter
    def response(self, response):
        self._response = response

    @property
    def topic(self):
        return self._topic

    @property
    def that(self):
        return self._that

class TestFileFileFinder(FileFinder):

    def __init__(self):
        FileFinder.__init__(self)

    def empty_row(self, row):
        return bool(len(row) < 2)

    def is_comment(self, question):
        return bool(question[0] == '#')

    def is_template(self, question):
        return bool(question[0] == '$')

    def clean_up_answer(self, text):
        return text.replace('"', "").strip()

    def add_answers_to_template(self, row, question, templates):
        answers = []
        for answer in row[1:]:
            answers.append(self.clean_up_answer(answer))
        templates[question] = answers

    def add_template_answers(self, templates, answer, answers):
        if answer in templates:
            template = templates[answer]
            for template_answer in template:
                answers.append(template_answer)
        else:
            print("Template [%s] not found!" % answer)

    def load_file_contents(self, filename, userid="*"):
        print("Loading aiml_tests from file [%s]" % filename)
        questions = []
        templates = {}
        with open(filename, 'r') as csvfile:
            csvreader = csv.reader(csvfile, delimiter=',', quotechar='"')
            for row in csvreader:
                if self.empty_row(row) is False:
                    question = row[0]
                    if self.is_comment(question) is False:
                        if self.is_template(question) is True:
                            self.add_answers_to_template(row, question, templates)
                        else:
                            answers = []
                            that = None
                            topic = None
                            for answer in row[1:]:
                                answer = answer.strip()
                                if answer:
                                    if self.is_template(answer) is True:
                                        self.add_template_answers(templates, answer, answers)
                                    else:
                                        if answer.startswith("\"THAT="):
                                            thatsplits = self.clean_up_answer(answer).split("=")
                                            that = thatsplits[1]
                                        elif answer.startswith("\"TOPIC="):
                                            topicsplits = self.clean_up_answer(answer).split("=")
                                            topic = topicsplits[1]
                                        else:
                                            answers.append(self.clean_up_answer(answer))
                            questions.append(TestQuestion(question, answers, topic=topic, that=that))
        return questions


class TestRunnerBotClient(BotClient):

    def __init__(self):
        BotClient.__init__(self, "TestRunner")

    @property
    def test_dir(self):
        return self.arguments.args.test_dir

    @property
    def test_file(self):
        return self.arguments.args.test_file

    @property
    def qna_file(self):
        return self.arguments.args.qna_file

    @property
    def verbose(self):
        return self.arguments.args.verbose

    def get_description(self):
        return 'ProgramY Test Runner Client'

    def add_client_arguments(self, parser=None):
        if parser is not None:
            parser.add_argument('--test_dir', dest='test_dir', help='directory containing test files to run against grammar')
            parser.add_argument('--test_file', dest='test_file', help='Single file of aiml_tests to run against grammar')
            parser.add_argument('--qna_file', dest='qna_file', help='A file containing questions and answers')
            parser.add_argument('--verbose', dest='verbose', action='store_true', help='print out each question to be asked')

    def set_environment(self):
        self.bot.brain.properties.add_property("env", "TestRunner")

    def get_client_configuration(self):
        return ConsoleConfiguration()

    def run(self):
        file_finder = TestFileFileFinder()
        if self.test_dir is not None:
            print("Loading Tests from directory [%s]" % self.test_dir)
            questions = file_finder.load_dir_contents(self.test_dir, extension=".tests", subdir=True)
        else:
            questions = file_finder.load_single_file_contents(self.test_file)

        question_and_answers = open(self.qna_file, "w+")

        successes = []
        failures = []
        warnings = 0
        start = datetime.datetime.now()
        for category in questions.keys():
            for test in questions[category]:
                test.category = category

                if any((c in '$*_^#') for c in test.question):
                    print("WARNING: Wildcards in question! [%s]"%test.question)
                    warnings = warnings +1

                if test.topic is not None:
                    conversation = self.bot.get_conversation(self.clientid)
                    conversation.set_property("topic", test.topic)

                if test.that is not None:
                    response = self.bot.ask_question(self.clientid, test.that, responselogger=self)

                response = self.bot.ask_question(self.clientid, test.question, responselogger=self)
                success = False
                test.response = response

                if self.verbose:
                    print(test.question, "->", test.response)
                question_and_answers.write('"%s", "%s"\n'%(test.question, test.response))

                if not test.answers_regex:
                    if test.response == "":
                        break
                else:
                    for expected_regex in test.answers_regex:
                        regex_type = expected_regex[0]
                        expression = expected_regex[1]
                        match = expression.search(response)
                        if match is not None and regex_type == "+":
                            success = True
                            break
                        elif match is None and regex_type == "-":
                            success = True
                            break

                if success is True:
                    successes.append(test)
                else:
                    failures.append(test)

        question_and_answers.flush ()
        question_and_answers.close ()

        stop = datetime.datetime.now()
        diff = stop-start
        total_tests = len(successes)+len(failures)

        print("Successes: %d" % len(successes))
        print("Failures:  %d" % len(failures))
        if warnings > 0:
            print("Warnings:  %d" % warnings)
        for failure in failures:
            print("\t%s: [%s] expected [%s], got [%s]" % (failure.category, failure.question, failure.answers_string, failure.response))
        print("Total processing time %f.2 secs"%diff.total_seconds())
        print("Thats approx %f aiml_tests per sec"%(total_tests/diff.total_seconds()))

if __name__ == '__main__':

    def run():
        print("Loading, please wait...")
        console_app = TestRunnerBotClient()
        console_app.run()

    run()
