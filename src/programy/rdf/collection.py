import logging

from programy.mappings.base import BaseCollection
from programy.rdf.entity import RDFEntity
from programy.utils.files.filefinder import FileFinder

class RDFLoader(FileFinder):
    def __init__(self, collection):
        FileFinder.__init__(self)
        self._collection = collection

    def load_file_contents(self, filename):
        if logging.getLogger().isEnabledFor(logging.DEBUG): logging.debug("Loading rdf [%s]", filename)
        try:
            self._collection.load_from_filename(filename)
        except Exception as excep:
            if logging.getLogger().isEnabledFor(logging.ERROR): logging.error("Failed to load rdf [%s] - %s", filename, excep)

class RDFCollection(BaseCollection):

    def __init__(self):
        BaseCollection.__init__(self)
        self._subjects = {}
        self._entities = []

    def split_line(self, line):
        splits = self.split_line_by_char(line)
        if len(splits) > 3:
            return [splits[0], splits[1], self.get_split_char().join(splits[2:])]
        else:
            return splits

    def get_split_char(self):
        return ":"

    def get_split_pattern(self):
        return ".*"

    def split_line_by_char(self, line):
        splits = line.split(self.get_split_char())
        return splits

    def process_splits(self, splits):
        subject = splits[0]
        predicate = splits[1]
        object = splits[2]

        if subject not in self._subjects:
            self._subjects[subject] = {}

        if predicate not in self._subjects[subject]:
            self._subjects[subject][predicate] = {}

        if object not in self._subjects[subject][predicate]:
            self._subjects[subject][predicate][object] = {}

        entity = RDFEntity(subject, predicate, object)
        self._subjects[subject][predicate][object] = entity
        self._entities.append(entity)

        return True

    def has_subject(self, subject):
        return bool(subject in self._subjects)

    def subjects(self):
        return self._subjects.keys ()

    def has_predicate(self, subject, predicate):
        if self.has_subject(subject):
            predicates = self._subjects[subject]
            return bool(predicate in predicates)
        return False

    def predicates(self, subject):
        return list(self._subjects[subject].keys ())

    def has_object(self, subject, predicate, object):
        if self.has_subject(subject):
            if self.has_predicate(subject, predicate):
                objects = self._subjects[subject][predicate]
                return bool(object in objects)
        return False

    def objects(self, subject, predicate):
        return list(self._subjects[subject][predicate].keys ())

    def add_entity(self, subject, predicate, object):
        if self.has_subject(subject) is False:
            self._subjects[subject] = {}

        if self.has_predicate(subject, predicate) is False:
            self._subjects[subject][predicate] = {}

        if self.has_object(subject, predicate, object) is False:
            entity =  RDFEntity(subject, predicate, object)
            self._subjects[subject][predicate][object] = entity
            self._entities.append(entity)
        else:
            if logging.getLogger().isEnabledFor(logging.WARNING): logging.warning("Duplicate RDF Entity [%s][%s][%s]"%(subject, predicate, object))

    def delete_entity(self, subject, predicate=None, object=None):

        if predicate is not None and object is not None and self.has_object(subject, predicate, object):
            self._entities.remove(self._subjects[subject][predicate][object])
            del self._subjects[subject][predicate][object]

        elif predicate is not None and self.has_predicate(subject, predicate):
            obj_keys = []
            for object in self._subjects[subject][predicate]:
                self._entities.remove(self._subjects[subject][predicate][object])
                obj_keys.append(object)
            for key in obj_keys:
                del self._subjects[subject][predicate][key]
            del self._subjects[subject][predicate]

        elif self.has_subject(subject):
            pred_keys = []
            for predicate in self._subjects[subject]:
                obj_keys = []
                for object in self._subjects[subject][predicate]:
                    self._entities.remove(self._subjects[subject][predicate][object])
                    obj_keys.append(object)
                for key in obj_keys:
                    del self._subjects[subject][predicate][key]
                pred_keys.append(predicate)
            for key in pred_keys:
                del self._subjects[subject][key]
            del self._subjects[subject]

    def match(self, subject=None, predicate=None, object=None):

        entities = []
        if subject is None:
            for for_subject in self._subjects:
                if predicate is None:
                    for for_predicate in self._subjects[for_subject]:
                        if object is None:
                            for for_object in self._subjects[for_subject][for_predicate]:
                                entities.append(self._subjects[for_subject][for_predicate][for_object])
                        elif self.has_object(for_subject, for_predicate, object):
                            entities.append(self._subjects[for_subject][for_predicate][object])
                elif self.has_predicate(for_subject, predicate):
                    if object is None:
                        for for_object in self._subjects[for_subject][predicate]:
                            entities.append(self._subjects[for_subject][predicate][for_object])
                    elif self.has_object(for_subject, predicate, object):
                        entities.append(self._subjects[for_subject][predicate][object])
        else:
            if self.has_subject(subject):
                if predicate is None:
                    for for_predicate in self._subjects[subject]:
                        if object is None:
                            for for_object in self._subjects[subject][for_predicate]:
                                entities.append(self._subjects[subject][for_predicate][for_object])
                        elif self.has_object(subject, for_predicate, object):
                            entities.append(self._subjects[subject][for_predicate][object])
                elif self.has_predicate(subject, predicate):
                    if object is None:
                        for for_object in self._subjects[subject][predicate]:
                            entities.append(self._subjects[subject][predicate][for_object])
                    elif self.has_object(subject, predicate, object):
                        entities.append(self._subjects[subject][predicate][object])

        return entities

    def not_match(self, subject=None, predicate=None, object=None):

        entities = self._entities[:]
        matched = self.match(subject, predicate, object)

        to_remove = []
        for match in matched:
            for entity in entities:
                if entity.subject == match.subject:
                    to_remove.append(entity)

        for rem in to_remove:
            if rem in entities:
                entities.remove(rem)

        return entities

    def load(self, configuration):
        loader = RDFLoader(self)
        if configuration.files is not None:
            files = loader.load_dir_contents(configuration.files, configuration.directories, configuration.extension)
            return len(files)
        else:
            self._subjects = {}
            self._entities = []
            return 0
