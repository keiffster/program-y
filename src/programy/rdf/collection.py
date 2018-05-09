from programy.utils.logging.ylogger import YLogger

from programy.mappings.base import BaseCollection
from programy.utils.files.filefinder import FileFinder

class RDFLoader(FileFinder):
    def __init__(self, collection):
        FileFinder.__init__(self)
        self._collection = collection

    def load_file_contents(self, id, filename, userid="*"):
        YLogger.debug(self, "Loading RDF File [%s]", filename)
        try:
            self._collection.load_from_filename(filename, id)
        except Exception as excep:
            YLogger.error(self, "Failed to load RDF File [%s] - %s", filename, excep)

class RDFEntity(object):

    def __init__(self, subject):
        self._subject = subject
        self._predicates = {}

#TODO No logging statements at all in RDF!
class RDFCollection(BaseCollection):

    def __init__(self):
        BaseCollection.__init__(self)
        self._entities = {}
        self._files = {}
        self._entities_to_ids = {}

    def empty(self):
        self._entities.clear()
        self._files.clear()
        self._entities_to_ids.clear()

    def contains(self, rdfname):
        return bool(rdfname.upper() in self._files)

    def filename(self, rdfname):
        return self._files[rdfname]

    def load(self, configuration):
        loader = RDFLoader(self)
        if configuration.files is not None:
            count = 0
            for file in configuration.files:
                rdfs, file_rdfs = loader.load_dir_contents(file, configuration.directories, configuration.extension)
                count += len(rdfs)
                for key in file_rdfs.keys():
                    self._files[key] = file_rdfs[key]
            return count
        return 0

    def reload_file(self, rdf_name):
        loader = RDFLoader(self)
        rdf_name = rdf_name.upper()
        filename = self.filename(rdf_name)
        if rdf_name in self._entities_to_ids:
            to_delete = []
            for entity in self._entities_to_ids[rdf_name]:
                to_delete.append(entity)
            for entity in to_delete:
                self.delete_entity(entity._subject)
        loader.load_file_contents(rdf_name, filename)

    def split_line(self, line):
        splits = self.split_line_by_char(line)
        if len(splits) > 3:
            return [splits[0], splits[1], self.get_split_char().join(splits[2:])]
        return splits

    def get_split_char(self):
        return ":"

    def get_split_pattern(self):
        return ".*"

    def split_line_by_char(self, line):
        splits = line.split(self.get_split_char())
        return splits

    def process_splits(self, splits, id=None):

        subject = splits[0]
        predicate = splits[1]
        obj = splits[2]

        self.add_entity(subject, predicate, obj, id)
        return True

    def subjects(self):
        return self._entities.keys()

    def predicates(self, subject):
        if subject in self._entities:
            return self._entities[subject]._predicates.keys()
        return []

    def objects(self, subject, predicate):
        if subject in self._entities:
            if predicate in self._entities[subject]._predicates:
                return [self._entities[subject]._predicates[predicate]]
        return []

    def add_entity(self, subject, predicate, obj, id=None):
        subject = subject.upper()
        predicate = predicate.upper()

        if subject not in self._entities:
            the_subject = RDFEntity(subject)
            self._entities[subject] = the_subject
            if id is not None:
                id = id.upper()
                if id not in self._entities_to_ids:
                    self._entities_to_ids[id] = []
                self._entities_to_ids[id].append(the_subject)

        entity = self._entities[subject]

        entity._predicates[predicate] = obj

    def has_subject(self, subject):
        return bool(subject.upper() in self._entities)

    def has_predicate(self, subject, predicate):
        if self.has_subject(subject):
            entity = self._entities[subject.upper()]
            return bool(predicate.upper() in entity._predicates)
        return False

    def has_object(self, subject, predicate, obj):
        if self.has_subject(subject):
            entity = self._entities[subject.upper()]
            if self.has_predicate(subject, predicate):
                return bool(entity._predicates[predicate.upper()] == obj)
        return False

    def delete_entity(self, subject, predicate=None, obj=None):

        if self.has_subject(subject):
            if predicate is None and obj is None:
                del self._entities[subject.upper()]
                return
            entity = self._entities[subject.upper()]
            if self.has_predicate(subject, predicate):
                if obj is None or obj == entity._predicates[predicate.upper()]:
                    del entity._predicates[predicate.upper()]
            if bool(entity._predicates) is False :
                del self._entities[subject.upper()]

    def all_as_tuples(self):
        all = []
        for subject, entity in self._entities.items():
            for predicate, obj in entity._predicates.items():
                all.append ([subject, predicate, obj])
        return all

    def matched_as_tuples(self, subject=None, predicate=None, obj=None):
        all = []
        for entity_subject, entity in self._entities.items():
            if subject is None or subject == entity_subject:
                for entity_predicate, entity_obj in entity._predicates.items():
                    if predicate is None or predicate == entity_predicate:
                        if obj is None or obj == entity_obj:
                            all.append([entity_subject, entity_predicate, entity_obj])
        return all

    def remove(self, entities, subject=None, predicate=None, obj=None):
        removes = []
        for entity in entities:
            if subject is not None:
                if predicate is not None:
                    if obj is not None:
                        if subject == entity[0] and predicate == entity[1] and obj == entity[2]:
                            removes.append(entity)
                    else:
                        if subject == entity[0] and predicate == entity[1]:
                            removes.append(entity)
                else:
                    if obj is not None:
                        if subject == entity[0] and obj == entity[2]:
                            removes.append(entity)
                    else:
                        if subject == entity[0]:
                            removes.append(entity)
            elif predicate is not None:
                if obj is not None:
                    if predicate == entity[1] and obj == entity[2]:
                        removes.append(entity)
                else:
                    if predicate == entity[1]:
                        removes.append(entity)
            elif obj is not None:
                if obj == entity[2]:
                    removes.append(entity)

        return [entity for entity in entities if entity not in removes]

    def match_to_vars(self, subject=None, predicate=None, obj=None):
        results = []
        for entity_subject, entity in self._entities.items():
            subj_element = None
            if subject is not None:
                if subject.startswith("?"):
                    subj_element = [subject, entity_subject]
                elif subject == entity_subject:
                    subj_element = ["subj", entity_subject]
            else:
                subj_element = ["subj", entity_subject]

            for entity_pred in entity._predicates:
                pred_element = None
                obj_element = None
                if predicate is not None:
                    if predicate.startswith("?"):
                        pred_element = [predicate, entity_pred]
                    elif predicate == entity_pred:
                        pred_element = ["pred", entity_pred]

                    if obj is not None:
                        if obj.startswith("?"):
                            obj_element = [obj, entity._predicates[entity_pred]]
                        elif obj == entity._predicates[entity_pred]:
                            obj_element = ["obj", entity._predicates[entity_pred]]
                    else:
                        obj_element = ["obj", entity._predicates[entity_pred]]

                else:
                    pred_element = ["pred", entity_pred]

                    if obj is not None:
                        if obj.startswith("?"):
                            obj_element = [obj, entity._predicates[entity_pred]]
                        elif subject == entity_subject:
                            obj_element = [obj, entity._predicates[entity_pred]]
                    else:
                        obj_element = ["obj", entity._predicates[entity_pred]]

                if subj_element is not None and pred_element is not None and obj_element is not None:
                    results.append([subj_element, pred_element, obj_element])

        return results

    def not_match_to_vars(self, subject=None, predicate=None, obj=None):

        if subject is not None and subject.startswith("?") is True:
            all_subject = subject
        else:
            all_subject = None
        if predicate  is not None and predicate.startswith("?") is True:
            all_predicate = predicate
        else:
            all_predicate = None
        if obj  is not None and obj.startswith("?") is True:
            all_obj = obj
        else:
            all_obj = None
        all = self.match_to_vars(all_subject, all_predicate, all_obj)
        matched = self.match_to_vars(subject, predicate, obj)

        to_remove =[]
        for entity in all:
           for atuple in matched:
               if entity[0][1] == atuple[0][1]:
                   #print("Removing from all", entity)
                   to_remove.append(entity)

        return [entity for entity in all if entity not in to_remove]

    def match_only_vars(self, subject=None, predicate=None, obj=None):
        results = self.match_to_vars(subject, predicate, obj)
        returns = []
        for atuple in results:
            aset = []
            for pair in atuple:
                if pair[0].startswith("?"):
                    aset.append(pair)
            if aset:
                returns.append(aset)

        return returns

    def get_unify_vars(self, vars):
        unified_vars = {}
        for var in vars:
            unified_vars[var] = None
        return unified_vars

    def dict_to_array(self, adict):
        atuple = []
        for name, value in adict.items():
            atuple.append([name, value])
        return atuple

    def unify(self, vars, sets):
        unifications = []
        if sets:
            # For each tuple in the first set
            for atuple in sets[0]:
                # Check to see if there are vars thay need unifying
                unified_vars = self.get_unify_vars(vars)
                if unified_vars:
                    # Get the value of the tuples which match the vars
                    if self.unify_tuple(atuple, unified_vars) is True:
                        # If we have more sets, keep checking that the vars are still matching
                        unified = True
                        if len(sets) > 1:
                            unified = self.unify_set(1, sets, unified_vars, 0)
                            #print("Unified?", unified_vars, unified)
                        # If we have unified all variables then we have a match
                        if unified is True and None not in unified_vars.values():
                            unifications.append(self.dict_to_array(unified_vars))
        return unifications

    def unify_set(self, num_set, sets, unified_vars, depth):
        aset = sets[num_set]
        unified = False
        for atuple in aset:
            if self.unify_tuple(atuple, unified_vars) is False:
                continue
            else:
                unified = True
            if num_set < len(sets)-1:
                return self.unify_set(num_set+1, sets, unified_vars, depth+1)
        return unified

    def unify_tuple(self, tuple, vars):
        for name, value in tuple:
            if name in vars:
                if vars[name] is None:
                    vars[name] = value
                else:
                    if vars[name] != value:
                        return False
        return True
