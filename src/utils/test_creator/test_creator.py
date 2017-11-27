import xml.etree.ElementTree as ET
import sys

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

if __name__ == '__main__':

    aiml_file = sys.argv[1]
    test_file = sys.argv[2]
    ljust = int(sys.argv[3])
    replace_file = sys.argv[4]

    default = None
    if len(sys.argv) > 5:
        default = sys.argv[5]

    print("aiml_file:", aiml_file)
    print("test_file:", test_file)
    print("replace_file:", replace_file)
    print("Default:", default)

    texts, sets, bots = load_replacements(replace_file)

    with open(test_file, "w+") as output_file:
        if default is not None:
            output_file.write('$DEFAULT, "%s"\n\n'%default)
        try:
            tree = ET.parse(aiml_file)
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
                    test_line = '%s "answer"'%(question)

                output_file.write(test_line)
                output_file.write("\n")

            topics = aiml.findall('topic')
            if len(topics) > 0:
                print("I dont handle topics yet!")

        except Exception as e:
            print(e)

        exit(0)


