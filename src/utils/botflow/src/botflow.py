import csv
import os
import re
import argparse
import shutil


def tabs(num):
    if tabs == 0:
        return ""
    else:
        return "\t" * num


class VarType(object):
    def __init__(self):
        self._values = []

    def extract_values_between_brackets(self, text, var_type):
        search_str = '%s\((.+?)\)' % var_type
        m = re.search(search_str, text)
        if m:
            return m.group(1)
        else:
            raise Exception("No value for defined type %s", text)


class SelectVar(VarType):
    def __init__(self, text):
        VarType.__init__(self)
        values = self.extract_values_between_brackets(text, "Select")
        self._values = [x.strip() for x in values.split(",")]

    def type_values_to_str(self):
        text = ", ".join(self._values)
        text += " or exit"
        return text

    def get_next_step(self, step, value):
        for condition in step._conditions:
            compare = condition._condition[2:]
            if compare == value:
                return condition._next_step
        return step._conditions[0]._next_step

    def output_template(self, aiml_file, topic_name, step):
        if step._conditions:
            aiml_file.write('\t\t\t\t<condition name="%s">\n' % step._variable)
            for value in self._values:
                next_step = self.get_next_step(step, value)
                aiml_file.write(
                    '\t\t\t\t\t<li value="%s"><srai>%s STEP %s</srai></li>\n' % (value, topic_name, next_step))
            aiml_file.write('\t\t\t\t\t<li><srai>%s STEP %s</srai></li>\n' % (topic_name, step._step))
            aiml_file.write('\t\t\t\t</condition>\n')
        else:
            aiml_file.write('\t\t\t\t<condition name="%s">\n' % step._variable)
            for value in self._values:
                aiml_file.write('\t\t\t\t\t<li value="%s"><srai>EXECUTE %s</srai></li>\n' % (value, topic_name))
            aiml_file.write('\t\t\t\t\t<li><srai>%s STEP %s</srai></li>\n' % (topic_name, step._step))
            aiml_file.write('\t\t\t\t</condition>\n')


class DateVar(VarType):
    def __init__(self, text):
        VarType.__init__(self)
        self._values.append(self.extract_values_between_brackets(text, "Date"))

    def type_values_to_str(self):
        text = self._values[0]
        text += " or exit"
        return text

    def output_template(self, aiml_file, topic_name, step):
        if step._conditions:
            next_step = step._conditions[0]._next_step
            aiml_file.write('\t\t\t\t<think><set name="Valid"><srai>VALID DATE <star /></srai></set></think>\n')
            aiml_file.write('\t\t\t\t<condition name="Valid">\n')
            aiml_file.write('\t\t\t\t\t<li value="TRUE"><srai>%s STEP %s</srai></li>\n' % (topic_name, next_step))
            aiml_file.write('\t\t\t\t\t<li><srai>%s STEP %s</srai></li>\n' % (topic_name, step._step))
            aiml_file.write('\t\t\t\t</condition>\n')
        else:
            aiml_file.write('\t\t\t\t<think><set name="Valid"><srai>VALID DATE <star /></srai></set></think>\n')
            aiml_file.write('\t\t\t\t<condition name="Valid">\n')
            aiml_file.write('\t\t\t\t\t<li value="TRUE"><srai>EXECUTE %s</srai></li>\n' % (topic_name))
            aiml_file.write('\t\t\t\t\t<li><srai>%s STEP %s</srai></li>\n' % (topic_name, step._step))
            aiml_file.write('\t\t\t\t</condition>\n')


class IntVar(VarType):
    def __init__(self, text):
        VarType.__init__(self)
        if '(' in text:
            ranges = self.extract_values_between_brackets(text, "Int")
            splits = ranges.split(",")
            if len(splits) > 1:
                self._values.append(splits[0])  # Min
                self._values.append(splits[1])  # Max
            else:
                self._values.append(splits[0])  # Max

    def type_values_to_str(self):
        if len(self._values) == 2:
            text = " to ".join(self._values)
        else:
            text = " max %s" % self._values[0]
        text += " or exit"
        return text

    def output_template(self, aiml_file, topic_name, step):
        if step._conditions:
            next_step = step._conditions[0]._next_step
            if len(self._values) == 2:
                aiml_file.write(
                    '\t\t\t\t<think><set name="Valid"><srai>VALID INT <star /> %s %s</srai></set></think>\n' % (
                        self._values[0], self._values[1]))
            elif len(self._values) == 1:
                aiml_file.write('\t\t\t\t<think><set name="Valid"><srai>VALID INT <star /> %s</srai></set></think>\n' %
                                self._values[0])
            else:
                aiml_file.write('\t\t\t\t<think><set name="Valid"><srai>VALID INT <star /></srai></set></think>\n')
            aiml_file.write('\t\t\t\t<condition name="Valid">\n')
            aiml_file.write(
                '\t\t\t\t\t<li value="TRUE"><srai>%s STEP %s</srai></li>\n' % (topic_name, next_step))
            aiml_file.write('\t\t\t\t\t<li><srai>%s STEP %s</srai></li>\n' % (topic_name, step._step))
            aiml_file.write('\t\t\t\t</condition>\n')
        else:
            if len(self._values) == 2:
                aiml_file.write(
                    '\t\t\t\t<think><set name="Valid"><srai>VALID INT <star /> %s %s</srai></set></think>\n' % (
                        self._values[0], self._values[1]))
            elif len(self._values) == 1:
                aiml_file.write('\t\t\t\t<think><set name="Valid"><srai>VALID INT <star /> %s</srai></set></think>\n' %
                                self._values[0])
            else:
                aiml_file.write('\t\t\t\t<think><set name="Valid"><srai>VALID INT <star /></srai></set></think>\n')
            aiml_file.write('\t\t\t\t<condition name="Valid">\n')
            aiml_file.write('\t\t\t\t\t<li value="TRUE"><srai>EXECUTE %s</srai></li>\n' % (topic_name))
            aiml_file.write('\t\t\t\t\t<li><srai>%s STEP %s</srai></li>\n' % (topic_name, step._step))
            aiml_file.write('\t\t\t\t</condition>\n')


class TextVar(VarType):
    def __init__(self, text):
        VarType.__init__(self)
        self._values.append(text)

    def type_values_to_str(self):
        return ""

    def output_template(self, aiml_file, topic_name, step):
        if step is not None:
            aiml_file.write('\t\t\t\t<srai>%s STEP %s</srai>\n' % (topic_name, step._next_step))
        else:
            aiml_file.write('\t\t\t\t<srai>EXECUTE %s</srai>\n' % topic_name)


class StepCondition(object):
    def __init__(self, next_step, condition):
        self._next_step = next_step
        self._condition = condition


class Step(object):
    def __init__(self, csv_line):
        print(csv_line)
        self._step = csv_line[0]
        self._prompt = csv_line[1]
        self._variable = csv_line[2]
        self._type = self._var_type(csv_line[3])
        csv_length = len(csv_line)
        self._conditions = []
        if csv_length > 4:
            if len(csv_line[4]) > 0:  # If its more than a blank line
                index = 4
                while index < csv_length:
                    next_step = csv_line[index]
                    condition = csv_line[index + 1]
                    self._conditions.append(StepCondition(next_step, condition))
                    index += 2

    def __str__(self):
        if self._conditions:
            next_steps = ", ".join("%s %s"(x._next_step, x.condition) for x in self._conditions)
        else:
            next_steps = "EXECUTE"
        return "[%s] - %s -> %s" % (self._step, self._prompt, next_steps)

    @staticmethod
    def _var_type(text):
        if text.startswith("Select"):
            return SelectVar(text)
        elif text.startswith("Date"):
            return DateVar(text)
        elif text.startswith("Int"):
            return IntVar(text)
        else:
            return TextVar(text)

    def output_aiml(self, aiml_file, topic_name):

        # Step Question
        aiml_file.write('\t\t<category>\n')
        aiml_file.write('\t\t\t<pattern>\n')
        aiml_file.write('\t\t\t\t%s STEP %s\n' % (topic_name, self._step))
        aiml_file.write('\t\t\t</pattern>\n')
        aiml_file.write('\t\t\t<template>\n')
        if self._type._values:
            aiml_file.write('\t\t\t\t%s - (%s)\n' % (self._prompt, self._type.type_values_to_str()))
        else:
            aiml_file.write('\t\t\t\t%s\n' % self._prompt)
        aiml_file.write('\t\t\t</template>\n')
        aiml_file.write('\t\t</category>\n\n')

        aiml_file.write('\t\t<category>\n')
        aiml_file.write('\t\t\t<pattern>*</pattern>\n')
        if self._type._values:
            aiml_file.write('\t\t\t<that>%s *</that>\n' % self._prompt)
        else:
            aiml_file.write('\t\t\t<that>%s</that>\n' % self._prompt)
        aiml_file.write('\t\t\t<template>\n')
        aiml_file.write('\t\t\t\t<think><set name="%s"><star /></set></think>\n' % self._variable)

        self._type.output_template(aiml_file, topic_name, self)


        aiml_file.write('\t\t\t</template>\n')
        aiml_file.write('\t\t</category>\n\n')

        aiml_file.write('\t\t<category>\n')
        aiml_file.write('\t\t\t<pattern>EXIT</pattern>\n')
        if self._type._values:
            aiml_file.write('\t\t\t<that>%s *</that>\n' % self._prompt)
        else:
            aiml_file.write('\t\t\t<that>%s</that>\n' % self._prompt)
        aiml_file.write('\t\t\t<template>\n')
        aiml_file.write('\t\t\t\t<srai>EXIT %s</srai>\n' % topic_name)
        aiml_file.write('\t\t\t</template>\n')
        aiml_file.write('\t\t</category>\n\n')


class BotFlow(object):
    def __init__(self):
        self._steps = []
        self._name = None

    def load_flow(self, flow_file, name):
        print("Loading flow file [%s]" % flow_file)

        self._steps.clear()
        self._name = name.upper()

        with open(flow_file, "r+") as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',', quotechar='"')
            first = True
            for line in csv_reader:
                if first is False:
                    if len(line) > 4:
                        self._steps.append(Step(line))
                    else:
                        print("Invalid line [%s], missing elements" % line)
                first = False

    def write_aiml_header(self, aiml_file):
        aiml_file.write('<?xml version="1" encoding="UTF-8" ?>\n')
        aiml_file.write('<aiml>\n\n')

    def write_aiml_footer(self, aiml_file):
        aiml_file.write('\n</aiml>')

    def write_entry_category(self, aiml_file, first_step):
        aiml_file.write('\t<category>\n')
        aiml_file.write('\t\t<pattern>START %s</pattern>\n' % self._name)
        aiml_file.write('\t\t<template>\n')
        aiml_file.write('\t\t\t<think>\n')
        # Set the topic
        aiml_file.write('\t\t\t\t<set name="topic">%s</set>\n' % self._name)
        # Clear variables before we start
        for step in self._steps:
            aiml_file.write('\t\t\t\t<set name="%s" />\n' % step._variable)
        aiml_file.write('\t\t\t</think>\n')
        # Jump to the first step
        aiml_file.write('\t\t\t<srai>%s STEP %s</srai>\n' % (self._name, first_step))
        aiml_file.write('\t\t</template>\n')
        aiml_file.write('\t</category>\n\n')

    def write_topic_open(self, aiml_file, name):
        aiml_file.write('\t<topic name="%s">\n\n' % name)

    def write_topic_close(self, aiml_file):
        aiml_file.write('\t</topic>\n')

    def write_dialog_flow(self, aiml_file):
        for step in self._steps:
            step.output_aiml(aiml_file, self._name)

    def generate_aiml(self, aiml_dir):
        print("Generating aiml in [%s]" % aiml_dir)

        with open(aiml_dir + os.sep + self._name + ".aiml", "w+", encoding="utf-8") as aiml_file:
            self.write_aiml_header(aiml_file)

            self.write_entry_category(aiml_file, self._steps[0]._step)

            self.write_topic_open(aiml_file, self._name)

            self.write_dialog_flow(aiml_file)

            self.write_topic_close(aiml_file)

            self.write_aiml_footer(aiml_file)

    def copy_supporting_files(self, from_dir, to_dir):
        shutil.copyfile(from_dir + os.sep + "aimlstandardlibrary.aiml", to_dir + os.sep + "aimlstandardlibrary.aiml")
        shutil.copyfile(from_dir + os.sep + "botflowlibrary.aiml", to_dir + os.sep + "botflowlibrary.aiml")


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Program-Y Flow Bot')

    parser.add_argument('-flow', dest='flowfile', help='Flow file to load')
    parser.add_argument('-topic', dest='topic', help='Topic name')
    parser.add_argument('-lib', dest='lib', help='Library of aiml files')
    parser.add_argument('-aiml', dest='aimldir', help='Directory to create aiml files in')

    args = parser.parse_args()

    botflow = BotFlow()

    botflow.load_flow(args.flowfile, args.topic)

    botflow.generate_aiml(args.aimldir)

    botflow.copy_supporting_files(args.lib, args.aimldir)
