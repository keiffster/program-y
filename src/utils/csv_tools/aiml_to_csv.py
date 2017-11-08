import sys
import xml.etree.ElementTree as ET
import csv
import re

class AIMLToCSVGenerator(object):

    def __init__(self):
        self._input = sys.argv[1]
        self._output = sys.argv[2]

    def run(self):
        csv_file = None

        try:
            tree = ET.parse(self._input)
            csv_file = open(self._output, "w+")
            csv_writer = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
            root = tree.getroot()
            for element in root:
                if element.tag == 'category':
                    self.parse_category_to_file(csv_writer, element, topic="*")
                elif element.tag == 'topic':
                    for child in element:
                        if child.tag == 'category':
                            self.parse_category_to_file(csv_writer, child, topic=element.attrib['name'])

        except Exception as excep:
            print (excep)
        finally:
            if csv_file is not None:
                csv_file.flush()
                csv_file.close ()

    def parse_category_to_file(self, csv_writer, category, topic):
        pattern = None
        that = "*"
        template = None
        for element in category:
            if element.tag == 'pattern':
                pattern = AIMLToCSVGenerator.element_to_string(element)
            elif element.tag == 'that':
                that = element.text
            elif element.tag == 'template':
                template = AIMLToCSVGenerator.element_to_string(element)

        pattern = AIMLToCSVGenerator.strip_all_whitespace(pattern)
        template = AIMLToCSVGenerator.strip_all_whitespace(template)
        topic = AIMLToCSVGenerator.strip_all_whitespace(topic)
        that = AIMLToCSVGenerator.strip_all_whitespace(that)

        csv_writer.writerow([pattern, topic, that, template])

    @staticmethod
    def element_to_string(element):
        s = element.text or ""
        for sub_element in element:
            s += ET.tostring(sub_element).decode("utf-8")
        s += element.tail
        return s

    @staticmethod
    def strip_all_whitespace(string):
        first_pass = re.sub(r'[\n\t\r+]', '', string)
        second_pass = re.sub(r'\s+', ' ', first_pass)
        return second_pass.strip()

if __name__ == '__main__':

    def run():
        print("Convertin AIML to CSV...")
        generator = AIMLToCSVGenerator()
        generator.run()

    run()
