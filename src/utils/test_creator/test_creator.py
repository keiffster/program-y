import xml.etree.ElementTree as ET
import sys
import os


def load_replacements(replace_file):
    texts = {}
    bots = {}
    sets = {}
    with open(replace_file, "r") as file:
        for line in file:
            line = line.strip()
            name_value = line.split(":")
            type_name = name_value[0].split(",")
            if len(type_name) == 2:
                if type_name[0] == "SET":
                    sets[type_name[1]] = name_value[1].upper()
                elif type_name[0] == "BOT":
                    bots[type_name[1]] = name_value[1].upper()
                else:
                    print("Unknown mapping type", type_name[0].upper())
            else:
                texts[type_name[0]] = name_value[1]

    return texts, sets, bots


def replace_wildcard(text, texts, wildcard):
    if wildcard in text and wildcard in texts:
        return text.replace(wildcard, texts[wildcard])
    return text


def replace_wildcards(text, texts):
    text = replace_wildcard(text, texts, "*")
    text = replace_wildcard(text, texts, "#")
    text = replace_wildcard(text, texts, "^")
    text = replace_wildcard(text, texts, "_")
    return text


def create_test_file(source, destination):

    print ("Creating %s in %s" %(source, destination))

    directory = os.path.dirname(destination)
    if not os.path.exists(directory):
        os.makedirs(directory)

    with open(destination, "w+") as output_file:
        if default is not None:
            output_file.write('$DEFAULT, "%s"\n\n'%default)
        try:
            tree = ET.parse(source)
            aiml = tree.getroot()
            categories = aiml.findall('category')
            for category in categories:
                pattern_text = ""

                pattern = category.find("pattern")
                for elt in pattern.iter():

                    if elt.tag == "pattern":
                        text = elt.text.strip().upper()
                        pattern_text += replace_wildcards(text, texts)

                    elif elt.tag == "set":
                        if 'name' in elt.attrib:
                            name = elt.attrib['name']
                        else:
                            name = elt.text.strip()

                        if name in sets:
                            pattern_text += sets[name]
                        else:
                            pattern_text += "SET[%s]"%name

                    elif elt.tag == "bot":
                        if 'name' in elt.attrib:
                            name = elt.attrib['name']
                        else:
                            name = elt.text.strip()

                        if name in bots:
                            pattern_text += bots[name]
                        else:
                            pattern_text += "BOT[%s]" % name

                    pattern_text += " "

                    if elt.tail is not None and elt.tail.strip() != "":
                        text = elt.tail.strip().upper()
                        pattern_text += replace_wildcards(text, texts)
                        pattern_text += " "

                question = '"%s",'%pattern_text.strip()
                question = question.ljust(ljust)


                if default is not None:
                    test_line = '%s $DEFAULT'%(question)

                else:
                    template = category.find('template')

                    answer = template.text
                    if answer:
                        if len(answer) > 80:
                            answer = (answer[0:80])
                    else:
                        answer = "ERROR"

                    test_line = '%s "%s"' % (question, answer.strip())

                output_file.write(test_line)
                output_file.write("\n")

            topics = aiml.findall('topic')
            if len(topics) > 0:
                print("I dont handle topics yet!")

        except Exception as e:
            print(e)



if __name__ == '__main__':

    source = sys.argv[1]
    if source not in ['-f', '-d']:
        print ("Please specify file -f or directory -d")
        exit(-1)

    aiml_source = sys.argv[2]
    test_dest = sys.argv[3]
    ljust = int(sys.argv[4])
    replace_file = sys.argv[5]

    default = None
    if len(sys.argv) > 6:
        default = sys.argv[6]

    print("aiml_source:", aiml_source)
    print("test_dest:", test_dest)
    print("replace_file:", replace_file)
    print("Default:", default)

    listOfFiles = list()
    if source == '-d':
        for (dirpath, dirnames, filenames) in os.walk(aiml_source):
            listOfFiles += [os.path.join(dirpath.replace(aiml_source, ""), file) for file in filenames]

    else:
        listOfFiles == aiml_source

    texts, sets, bots = load_replacements(replace_file)

    if source == '-f':
        create_test_file(aiml_source, test_dest)

    else:

        for fileToProcess in listOfFiles:
            if fileToProcess[0] == '/':
                create_test_file(aiml_source + fileToProcess, test_dest + fileToProcess + ".tests")
            else:
                create_test_file(aiml_source + os.sep + fileToProcess, test_dest + os.sep + fileToProcess + ".tests")

