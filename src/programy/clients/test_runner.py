import logging
import csv
import re
import datetime

from programy.clients.clients import BotClient
from programy.utils.files.filefinder import FileFinder

class TestQuestion(object):

    def __init__(self, question, answers):
        self._question = question
        self._answers = answers
        self._answers_regex = []
        for answer in answers:
            if answer is not None and len(answer) > 0:
                self._answers_regex.append(re.compile(answer))
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


class TestFileFileFinder(FileFinder):

    def __init__(self):
        FileFinder.__init__(self)

    def empty_row(self, row):
        return bool(len(row)<2)

    def is_comment(self, question):
        return bool(question[0]=='#')

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

    def load_file_contents(self, filename):
        print("Loading aiml_tests from file [%s]" % filename)
        questions = []
        templates = {}
        with open(filename, 'r') as csvfile:
            csvreader = csv.reader(csvfile, delimiter=',', quotechar='"')
            for row in csvreader:
                if self.empty_row(row) is False:
                    question = row[0]
                    #print("{", question, "}")
                    if self.is_comment(question) is False:
                        if self.is_template(question) is True:
                            self.add_answers_to_template(row, question, templates)
                        else:
                            answers = []
                            for answer in row[1:]:
                                answer = answer.strip()
                                if self.is_template(answer) is True:
                                    self.add_template_answers(templates, answer, answers)
                                else:
                                    answers.append(self.clean_up_answer(answer))
                            questions.append(TestQuestion(question, answers))
        return questions


class TestRunnerBotClient(BotClient):

    def __init__(self):
        BotClient.__init__(self)
        self.clientid = "TestRunner"

    @property
    def test_dir(self):
        return self.arguments.args.test_dir

    @property
    def test_file(self):
        return self.arguments.args.test_file

    @property
    def verbose(self):
        return self.arguments.args.verbose

    def get_description(self):
        return 'ProgramY Test Runner Client'

    def add_client_arguments(self, parser):
        parser.add_argument('--test_dir', dest='test_dir', help='directory containing test files to run against grammar')
        parser.add_argument('--test_file', dest='test_file', help='Single file ot aiml_tests to run against grammar')
        parser.add_argument('--verbose', dest='verbose', action='store_true', help='print out each question to be asked')

    def set_environment(self):
        self.bot.brain.predicates.pairs.append(["env", "TestRunner"])

    def run(self):
        file_finder = TestFileFileFinder()
        if self.test_dir is not None:
            print ("Loading Tests from directory [%s]" % self.test_dir)
            collection = file_finder.load_dir_contents(self.test_dir, extension=".tests", subdir=True)
        else:
            collection = file_finder.load_single_file_contents(self.test_file)

        successes = []
        failures = []
        warnings = 0
        start = datetime.datetime.now()
        for category in collection.keys():
            for test in collection[category]:
                test.category = category
                if self.verbose:
                    print(test.question)
                if any((c in '*$_^,') for c in test.question):
                    print ("WARNING: Wildcards in question! [%s]"%test.question)
                    warnings = warnings +1
                response = self.bot.ask_question(self.clientid, test.question)
                success = False
                test.response = response
                if len(test.answers_regex) == 0:
                    if test.response == "":
                        success = True
                        break
                else:
                    for expected_regex in test.answers_regex:
                        if expected_regex.search(response):
                            success = True
                            break
                if success is True:
                    successes.append(test)
                else:
                    failures.append(test)
        stop = datetime.datetime.now()
        diff = stop-start
        total_tests = len(successes)+len(failures)

        print ("Successes: %d" % len(successes))
        print ("Failures:  %d" % len(failures))
        if warnings > 0:
            print ("Warnings:  %d" % warnings)
        for failure in failures:
            print ("\t%s: [%s] expected [%s], got [%s]" % (failure.category, failure.question, failure.answers_string, failure.response))
        print ("Total processing time %f.2 secs"%diff.total_seconds())
        print ("Thats approx %f aiml_tests per sec"%(total_tests/diff.total_seconds()))

if __name__ == '__main__':

    def run():
        print("Loading, please wait...")
        console_app = TestRunnerBotClient()
        console_app.run()

    run()

