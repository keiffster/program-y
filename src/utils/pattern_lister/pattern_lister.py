import xml.etree.ElementTree as ET
import sys
import os
import os.path

if __name__ == '__main__':

    aiml_dir = sys.argv[1]
    csv_file = sys.argv[2]

    print("aiml_dir:", aiml_dir)
    print("csv_file:", csv_file)

    questions = []

    files = 0
    for dirpath, dirnames, filenames in os.walk(aiml_dir):
        for filename in filenames:
            files += 1
            aiml_file = os.path.join(dirpath, filename)
            print (aiml_file)

            try:
                tree = ET.parse(aiml_file)
                aiml = tree.getroot()
                categories = aiml.findall('category')
                for category in categories:
                    pattern_text = ""

                    pattern = category.find("pattern")
                    for elt in pattern.iter():

                        comma = False
                        if elt.tag == "pattern":
                            if elt.text is not None:
                                text = elt.text.strip().upper()
                                pattern_text += " ".join(text.split())
                                comma = True

                        elif elt.tag == "set":
                            if 'name' in elt.attrib:
                                name = elt.attrib['name']
                            else:
                                name = elt.text.strip()
                            if comma is True:
                                pattern_text += " "
                            pattern_text += " SET[%s]"%name
                            if text:
                                pattern_text += " "
                                pattern_text += " ".join(text.split())
                            comma = True

                        elif elt.tag == "bot":
                            if 'name' in elt.attrib:
                                name = elt.attrib['name']
                            else:
                                name = elt.text.strip()
                            if comma is True:
                                pattern_text += " "
                            pattern_text += " BOT[%s]" % name
                            if text:
                                pattern_text += " "
                                pattern_text += " ".join(text.split())
                            comma = True

                        if elt.tail is not None and elt.tail.strip() != "":
                            if comma is True:
                                pattern_text += " "
                            text = elt.tail.strip().upper()
                            if text:
                                pattern_text += " "
                                pattern_text += " ".join(text.split())
                            comma = True

                        if pattern_text is not None:
                            pattern_text = pattern_text.strip()
                            if len(pattern_text) > 0:
                                questions.append([aiml_file, pattern_text])


            except Exception as e:
                print(e)
                raise e

    questions.sort(key=lambda x: x[1])
    with open(csv_file, "w+") as output_file:
        for line in questions:
            new_line = ", ".join(line[1].split())
            output_file.write(line[0])
            output_file.write(", ")
            output_file.write(new_line)
            output_file.write("\n")

    print("Files:    %d"%files)
    print("Patterns: %d"%len(questions))