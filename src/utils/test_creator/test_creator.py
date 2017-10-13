import xml.etree.ElementTree as ET
import sys

if __name__ == '__main__':

    input = sys.argv[1]
    output = sys.argv[2]
    default = None
    if len(sys.argv) > 3:
        default = sys.argv[3]

    print("Input:", input)
    print("Output:", output)
    print("Default:", default)

    with open(output, "w+") as output_file:
        if default is not None:
            output_file.write('$DEFAULT, "%s"\n\n'%default)
        try:
            tree = ET.parse(input)
            aiml = tree.getroot()
            categories = aiml.findall('category')
            for category in categories:
                pattern = category.find("pattern")
                sets = pattern.findall('set')
                bots = pattern.findall('bot')
                if len(sets) > 0:
                    pattern_text = ""
                    if pattern.text is not None:
                        pattern_text += pattern.text
                    pattern_text += " SET[%s] "%sets[0].text
                    if pattern.tail is not None:
                        pattern_text += pattern.tail.strip()
                elif len(bots) > 0:
                    pattern_text = ""
                    if pattern.text is not None:
                        pattern_text += pattern.text
                    pattern_text += " BOT[%s] "%bots[0].text
                    if pattern.tail is not None:
                        pattern_text += pattern.tail.strip()
                else:
                    pattern_text = pattern.text
                if default is not None:
                    test_line = '"%s", $DEFAULT'%(pattern_text)
                else:
                    template = category.find('template')
                    test_line = '"%s", "%s"'%(pattern_text, template.text)
                output_file.write(test_line)
                output_file.write("\n")

            topics = aiml.findall('topic')
            if len(topics) > 0:
                print("I dont handle topics yet!")

        except Exception as e:
            print(e)

