import xml.etree.ElementTree as ET
from os import walk, sep

file_converters = {
    "DefaultPredicates":    { "seperator": ":", "filename": "defaults.txt"},
    "GenderSubstitutions":  { "seperator": ":", "filename": "gender.txt"},
    "PersonSubstitutions":  { "seperator": ":", "filename": "person.txt"},
    "Person2Substitutions": { "seperator": ":", "filename": "person2.txt"},
    "Splitters":            {                   "filename": "converters.txt"},
    "Substitutions":        { "seperator": ":", "filename": "denormals.txt"},
    "Settings":             { "seperator": ":", "filename": "settings.txt", "ignores": [
                                                                                        "aimldirectory",
                                                                                        "configdirectory",
                                                                                        "logdirectory",
                                                                                        "convertersfile",
                                                                                        "person2substitutionsfile",
                                                                                        "personsubstitutionsfile",
                                                                                        "gendersubstitutionsfile",
                                                                                        "defaultpredicates",
                                                                                        "substitutionsfile",
                                                                                        "maxlogbuffersize",
                                                                                        "notacceptinguserinputmessage",
                                                                                        "stripperregex",
                                                                                        "islogging",
                                                                                        "willcallhome",
                                                                                        "timeout",
                                                                                        "timeoutmessage",]}
    }


class PandoraBotsFileConverter(object):

    @staticmethod
    def all_files(path):
        files = []
        for (_, _, names) in walk(path):
            for name in names:
                files.append(path + sep + name)
            break
        return files

    @staticmethod
    def get_filename(file):
        splits1 = file.split(sep)
        splits2 = splits1[-1].split(".")
        return splits2[0]

    @staticmethod
    def convert_file(from_file, to_file, converter):
        print(from_file)
        with open(to_file, "w+") as open_file:
            tree = ET.parse(from_file)
            xml = tree.getroot()
            for item in xml:
                name = None
                if 'name' in item.attrib:
                    name = item.attrib['name'].strip()
                value = item.attrib['value'].strip()

                seperator = ":"
                if 'seperator' in converter:
                    seperator = converter['seperator']

                ignores = []
                if 'ignores' in converter:
                    ignores = converter['ignores']

                if name:
                    if name not in ignores:
                        open_file.write("%s%s%s\n" % (name, seperator, value))
                else:
                    open_file.write("%s\n" % value)

    def convert(self, from_files, to_files):

        files = self.all_files(from_files)
        for from_file in files:
            filename = self.get_filename(from_file)
            if filename in file_converters:
                converter = file_converters[filename]
                to_file = to_files + sep + converter["filename"]
                self.convert_file(from_file, to_file, converter)


if __name__ == '__main__':

    from_files = "./pbfiles"
    to_files = "./yfiles"
    converter = ":"

    converter = PandoraBotsFileConverter()
    converter.convert(from_files, to_files)