import sys
import os.path

if __name__ == '__main__':

    rdf_dir = sys.argv[1]
    csv_file = sys.argv[2]

    print("rdf_dir:", rdf_dir)
    print("csv_file:", csv_file)

    entities = []

    files = 0
    for dirpath, dirnames, filenames in os.walk(rdf_dir):
        for filename in filenames:
            files += 1
            rdf_file = os.path.join(dirpath, filename)
            file = open(rdf_file, "r")
            for line in file:
                if line and len(line.strip()) > 0:
                    entity = []
                    rdf_splits = line.split(":")
                    entity.append(rdf_file)
                    entity += rdf_splits
                    entities.append(entity)
            file.close ()

    entities.sort(key=lambda x: x[1])

    with open(csv_file, "w+") as output_file:
        for entity in entities:
            new_line = ", ".join(entity)
            output_file.write(new_line)

    print("Files: %d"%files)
    print("RDFs:  %d"%len(entities))