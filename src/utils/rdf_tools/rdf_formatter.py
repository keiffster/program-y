
import sys
import os

class RDFFormatter():

    def __init__(self):
        self._rdf_file = sys.argv[1]

    def get_basename_category(self):
        basename = os.path.basename(self._rdf_file)
        segments = basename.split(".")
        if len(segments) > 1:
            category = segments[0].upper()
        else:
            category = segments.upper()
        return category

    def read_rdf_rdf_file_file(self, category):
        rdfs = {}

        with open(self._rdf_file, "r") as rdf_rdf_file:
            for line in rdf_rdf_file:
                if line:
                    if line.strip().startswith("#") is False:
                        rdf = line.split(":")
                        if len(rdf) > 2:
                            subject = rdf[0].strip().upper()
                            predicate = rdf[1].strip().upper()
                            object = ":".join([x.strip() for x in rdf[2:]])

                            if subject not in rdfs:
                                rdfs[subject] = {}
                                rdfs[subject]['CATEGORY'] = category

                            rdfs[subject][predicate] = object
        return rdfs

    def write_new_rdf_file(self, rdfs):
        temp_filename = self._rdf_file + ".tmp"
        with open(temp_filename, "w+") as rdf_output_tmp:
            for subject in rdfs.keys():
                rdf_output_tmp.write ( "#%s\n"%subject)
                for predicate in rdfs[subject].keys ():
                    rdf_output_tmp.write("%s:%s:%s\n"%(subject, predicate, rdfs[subject][predicate]))
                rdf_output_tmp.write("\n")

        os.remove(self._rdf_file)
        os.rename(temp_filename, self._rdf_file)

    def run(self):

        category = self.get_basename_category()

        rdfs = self.read_rdf_rdf_file_file(category)

        self.write_new_rdf_file(rdfs)


if __name__ == '__main__':

    def run():
        print("Formatting RDF File")
        formatter = RDFFormatter()
        formatter.run()

    run()
