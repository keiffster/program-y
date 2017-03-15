import logging
import csv
import re

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

    def load_file_contents(self, filename):
        print("Loading tests from file [%s]" % filename)
        questions = []
        with open(filename, 'r') as csvfile:
            csvreader = csv.reader(csvfile, delimiter=',', quotechar='"')
            for row in csvreader:
                if len(row) > 1:
                    question = row[0]
                    if question[0] != '#':
                        answers = []
                        for answer in row[1:]:
                            answers.append(answer.replace('"', "").strip())
                        questions.append(TestQuestion(question, answers))
        return questions


class TestRunnerBotClient(BotClient):

    def __init__(self):
        BotClient.__init__(self)
        self.clientid = "TestRunner"

    @property
    def test_dir(self):
        return self.arguments.args.test_dir

    def get_description(self):
        return 'ProgramY Test Runner Client'

    def add_client_arguments(self, parser):
        parser.add_argument('--test_dir', dest='test_dir', help='directory containing test files to run against grammar')

    def set_environment(self):
        self.bot.brain.predicates.pairs.append(["env", "TestRunner"])

    def run(self):
        print ("Loading Tests from directory [%s]" % self.test_dir)
        file_finder = TestFileFileFinder()
        collection = file_finder.load_dir_contents(self.test_dir, extension=".tests")
        successes = []
        failures = []
        for category in collection.keys():
            for test in collection[category]:
                test.category = category
                response = self.bot.ask_question(self.clientid, test.question).upper()
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

        print ("Successes: %d" % len(successes))
        print ("Failures:  %d" % len(failures))
        for failure in failures:
            print ("\t%s: [%s] expected [%s], got [%s]" % (failure.category, failure.question, failure.answers_string, failure.response))

if __name__ == '__main__':

    def run():
        print("Loading, please wait...")
        console_app = TestRunnerBotClient()
        console_app.run()

    run()

