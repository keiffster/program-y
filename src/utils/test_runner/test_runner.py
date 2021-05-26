import csv
import re
import datetime
import os

from programy.clients.client import BotClient
from programy.utils.files.filefinder import FileFinder
from programy.clients.events.console.config import ConsoleConfiguration


class TestQuestion(object):

    def __init__(self, question, answers, filename, topic=None, that=None):
        self._category = None
        self._question = question
        self._answers = answers
        self._answers_regex = []
        self._topic = topic
        self._that = that
        self._filename = filename

        for answer in answers:
            if answer is not None and answer:
                try:
                    if answer[0] == "!":
                        self._answers_regex.append(("-", re.compile(answer)))
                    else:
                        self._answers_regex.append(("+", re.compile(answer)))
                except Exception as e:
                    print ("Failed to add answer [%s]" % answer)

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

    @property
    def filename(self):
        return self._filename


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

    def load_file_contents(self, fileid, filename, userid="*"):
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

                            questions.append(TestQuestion(question, answers, filename, topic=topic, that=that))

        print("\tTotal %d questions"%len(questions))
        return questions


class TestRunnerBotClient(BotClient):

    def __init__(self):
        BotClient.__init__(self, "TestRunner")

    @property
    def test_dir(self):
        return self.arguments.args.test_dir

    @property
    def qna_dir(self):
        return self.arguments.args.qna_dir

    @property
    def test_file(self):
        return self.arguments.args.test_file

    @property
    def qna_file(self):
        return self.arguments.args.qna_file

    @property
    def fail_file(self):
        return self.arguments.args.fail_file

    @property
    def verbose(self):
        return self.arguments.args.verbose

    def get_description(self):
        return 'ProgramY Test Runner Client'

    def add_client_arguments(self, parser=None):
        if parser is not None:
            parser.add_argument('--test_dir', dest='test_dir', help='directory containing test files to run against grammar')
            parser.add_argument('--qna_dir', dest='qna_dir', help='directory where test results will be written, matches test_dir for structure')
            parser.add_argument('--test_file', dest='test_file', help='Single file of aiml_tests to run against grammar')
            parser.add_argument('--qna_file', dest='qna_file', help='A file containing questions and answers')
            parser.add_argument('--fail_file', dest='fail_file', help='A file containing all failures')
            parser.add_argument('--verbose', dest='verbose', action='store_true', help='print out each question to be asked')

    def set_environment(self):
        self.bot.brain.properties.add_property("env", "TestRunner")

    def get_client_configuration(self):
        return ConsoleConfiguration()

    def make_output_filename(self, filename):
        return filename.replace(self.test_dir, self.qna_dir).replace(".tests", ".results")

    def run(self):
        file_finder = TestFileFileFinder()
        if self.test_dir is not None:
            print("Loading Tests from directory [%s]" % self.test_dir)
            questions, file_maps = file_finder.load_dir_contents(self.test_dir, extension=".tests", subdir=True)

        else:
            questions = file_finder.load_single_file_contents(self.test_file)

        if not questions:
            return

        question_and_answers_name = None
        question_and_answers = None

        client_context = self.create_client_context("*")

        successes = []
        failures = []
        warnings = 0
        start = datetime.datetime.now()

        total_tests = 0
        for category in questions.keys():
            total_tests += len(questions[category])

        print("Starting test run of %d questions" % total_tests)

        for category in questions.keys():
            for test in questions[category]:
                test.category = category

                new_filename = self.make_output_filename(test.filename)

                if question_and_answers_name is None or question_and_answers_name != new_filename:

                    if question_and_answers_name is not None:
                        question_and_answers.flush()
                        question_and_answers.close()

                    print("Testing [%d] -> %s: " % (len(questions[category]), new_filename))

                    directory = os.path.dirname(new_filename)
                    if not os.path.exists(directory):
                        os.makedirs(directory)

                    question_and_answers = open(new_filename, "w+")
                    question_and_answers_name = new_filename

                if any((c in '$*_^#') for c in test.question):
                    if self.verbose:
                        print("WARNING: Wildcards in question! [%s]"%test.question)
                    warnings = warnings +1

                if test.topic is not None:
                    if self.verbose:
                        print("Topic:", test.topic)
                    conversation = client_context.bot.get_conversation(self.clientid)
                    conversation.set_property("topic", test.topic)

                try:
                    if test.that is not None:
                        if self.verbose:
                            print("Asked:", test.that)
                        client_context.bot.ask_question(client_context, test.that)

                    if self.verbose:
                        print("Asking:", test.question)
                    response = client_context.bot.ask_question(client_context, test.question)
                    success = False
                    test.response = response

                    if self.verbose:
                        print(test.question, "->", test.response)

                except Exception as error:
                    print("****** Error asking %s", test.question)

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

        print("Test run complete....")

        if question_and_answers_name is not None:
            question_and_answers.flush ()
            question_and_answers.close ()

        stop = datetime.datetime.now()
        diff = stop-start
        total_tests = len(successes)+len(failures)

        print("Successes: %d" % len(successes))
        print("Failures:  %d" % len(failures))
        if warnings > 0:
            print("Warnings:  %d" % warnings)

        directory = os.path.dirname(self.fail_file)
        if not os.path.exists(directory):
            os.makedirs(directory)

        print("Writing failure file...")
        with open(self.fail_file, "w+") as fail_file:
            for failure in failures:
                fail_file.write("%s: [%s] expected [%s], got [%s]\n" % (failure.category, failure.question, failure.answers_string, failure.response))
            fail_file.flush()
            fail_file.close()

        print("Total processing time %f.2 secs"%diff.total_seconds())
        print("That's approx %f aiml tests per sec"%(total_tests/diff.total_seconds()))


if __name__ == '__main__':

    def run():
        print("Loading, please wait...")
        console_app = TestRunnerBotClient()
        console_app.run()

    run()
