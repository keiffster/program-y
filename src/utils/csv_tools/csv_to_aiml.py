import sys
import csv
class CSVToAIMLGenerator(object):

    def __init__(self):
        self._input = sys.argv[1]
        self._output = sys.argv[2]

    def run(self):
        csv_file = None
        aiml_file = None
        try:
            csv_file = open(self._input, "r+")
            csv_reader = csv.reader(csv_file, delimiter=',', quotechar='"')

            aiml_file = open(self._output, "w+")

            aiml_file.write('<?xml version="1.0" encoding="UTF-8"?>\n')
            aiml_file.write('<aiml>\n')

            aiml_file.write('\n')
            for line in csv_reader:
                if line:
                    if line[0] == "Pattern":
                        continue
                    template = line[0].strip()
                    pattern = line[1].strip(' "')
                    topic = None
                    if len(line)>2:
                        topic = line[2].strip(' "')
                        if not topic:
                            topic = None
                    that = None
                    if len(line)>3:
                        that = line[3].strip(' "')
                        if not that:
                            that = None
                    tab = ""
                    if topic is not None:
                        aiml_file.write('<topic name="%s">\n'%topic)
                        tab = "\t"
                    aiml_file.write('%s<category>\n'%tab)
                    aiml_file.write('%s\t<pattern>%s</pattern>\n'%(tab, template))
                    if that is not None:
                        aiml_file.write('%s\t<that>%s</that>\n' % (tab, that))
                    aiml_file.write('%s\t<template>\n'%tab)
                    aiml_file.write('%s\t\t%s\n'%(tab, pattern))
                    aiml_file.write('%s\t</template>\n'%tab)
                    aiml_file.write('%s</category>\n'%tab)

                    if topic is not None:
                        aiml_file.write('</topic>\n')

                    aiml_file.write('\n')

            aiml_file.write('</aiml>\n')

        except Exception as excep:
            print (excep)
        finally:
            if csv_file is not None:
                csv_file.close ()
            if aiml_file is not None:
                aiml_file.flush ()
                aiml_file.close ()

if __name__ == '__main__':

    def run():
        print("Convertin CSV to AIML...")
        generator = CSVToAIMLGenerator()
        generator.run()

    run()
