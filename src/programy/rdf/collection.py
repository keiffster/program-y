"""
Copyright (c) 2016-2020 Keith Sterling http://www.keithsterling.com

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated
documentation files (the "Software"), to deal in the Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software,
and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the
Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO
THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""
from programy.utils.logging.ylogger import YLogger
from programy.mappings.base import BaseCollection
from programy.storage.factory import StorageFactory


class RDFEntity:

    def __init__(self, subject):
        self._subject = subject
        self._predicates = {}

    @property
    def predicates(self):
        return self._predicates


class RDFCollection(BaseCollection):

    RDFS = "rdfs"

    def __init__(self):
        BaseCollection.__init__(self)
        self._entities = {}
        self._stores = {}
        self._entities_to_ids = {}
        self._entities_to_stores = {}

    @property
    def entities(self):
        return self._entities

    @property
    def stores(self):
        return self._stores

    @property
    def entities_to_ids(self):
        return self._entities_to_ids

    @property
    def entities_to_stores(self):
        return self._entities_to_stores

    def empty(self):
        YLogger.debug(self, "Emptying RDF Collection")
        self._entities.clear()
        self._stores.clear()
        self._entities_to_ids.clear()
        self._entities_to_stores.clear()

    def contains(self, rdfname):
        return bool(rdfname.upper() in self._stores)

    def storename(self, mapname):
        if mapname in self._stores:
            return self._stores[mapname]
        return None

    def subjects(self):
        return list(self._entities.keys())

    def predicates(self, subject):
        if subject in self._entities:
            return list(self._entities[subject].predicates.keys())
        return []

    def objects(self, subject, predicate):
        if subject in self._entities:
            if predicate in self._entities[subject].predicates:
                return [self._entities[subject].predicates[predicate]]
        return []

    def load(self, storage_factory):
        YLogger.debug(self, "Loading RDF Collection")
        if storage_factory.entity_storage_engine_available(StorageFactory.RDF) is True:
            rdf_engine = storage_factory.entity_storage_engine(StorageFactory.RDF)
            try:
                rdfs_store = rdf_engine.rdf_store()
                rdfs_store.load_all(self)
                return True

            except Exception as e:
                YLogger.exception(self, "Failed to load rdf from storage", e)

        return False

    def reload(self, storage_factory, rdf_name):
        YLogger.debug(self, "Reloading RDF [%s]", rdf_name)
        if storage_factory.entity_storage_engine_available(StorageFactory.RDF) is True:
            rdf_engine = storage_factory.entity_storage_engine(StorageFactory.RDF)
            try:
                rdfs_store = rdf_engine.rdf_store()
                rdfs_store.reload(self, rdf_name)
                return True

            except Exception as e:
                YLogger.exception(self, "Failed to load rdf from storage", e)

        return False

    def add_entity(self, subject, predicate, obj, rdf_name, rdf_store=None, entityid=None):
        YLogger.debug(self, "Adding RDF Entity [%s] [%s] [%s] [%s]", subject, predicate, obj, rdf_name)

        subject = subject.upper()
        predicate = predicate.upper()

        if subject not in self._entities:
            the_subject = RDFEntity(subject)
            self._entities[subject] = the_subject

            if entityid is not None:
                entityid = entityid.upper()
                if entityid not in self._entities_to_ids:
                    self._entities_to_ids[entityid] = []
                self._entities_to_ids[entityid].append(the_subject)

            self._stores[rdf_name] = rdf_store
            self._entities_to_stores[subject] = rdf_name

        entity = self._entities[subject]

        if predicate in entity.predicates:
            entity.predicates[predicate].append(obj)
        else:
            entity.predicates[predicate] = [obj]

    def has_subject(self, subject):
        return bool(subject.upper() in self._entities)

    def has_predicate(self, subject, predicate):
        if self.has_subject(subject):

            entity = self._entities[subject.upper()]
            return bool(predicate.upper() in entity.predicates)

        return False

    def has_object(self, subject, predicate, obj):
        if self.has_subject(subject):
            entity = self._entities[subject.upper()]

            if self.has_predicate(subject, predicate):
                objects = entity.predicates[predicate.upper()]

                for anobject in objects:
                    if obj == anobject:
                        return True

        return False

    def delete_entity(self, subject, predicate=None, obj=None):
        YLogger.debug(self, "Deleting RDF Entity [%s] [%s] [%s]", subject, predicate, obj)

        if self.has_subject(subject):

            if predicate is None and obj is None:
                YLogger.debug(None, "Removing entire subject %s", subject)
                del self._entities[subject.upper()]
                return

            entity = self._entities[subject.upper()]

            if obj is None:
                if self.has_predicate(subject, predicate):
                    YLogger.debug(None, "Removing entire predicate %s, subject %s", predicate, subject)
                    del entity.predicates[predicate.upper()]
            else:
                if predicate.upper() in entity.predicates:
                    objects = entity.predicates[predicate.upper()]

                    if obj in objects:
                        YLogger.debug(None, "Removing object %s from predicate %s, subject %s", obj, predicate, subject)
                        objects = entity.predicates[predicate.upper()]
                        objects.remove(obj)

                    if len(entity.predicates[predicate.upper()]) == 0:
                        YLogger.debug(None, "Removing empty predicate %s, subject %s", predicate, subject)
                        del entity.predicates[predicate.upper()]

            if len(entity.predicates.keys()) == 0:
                YLogger.debug(None, "Removing empty subject %s", subject)
                del self._entities[subject.upper()]

    def all_as_tuples(self):
        tuples = []
        for subject, entity in self._entities.items():
            for predicate, objects in entity.predicates.items():
                for obj in objects:
                    tuples.append([subject, predicate, obj])
        return tuples

    def matched_as_tuples(self, subject=None, predicate=None, obj=None):
        tuples = []
        for entity_subject, entity in self._entities.items():
            if subject is None or subject == entity_subject:
                for entity_predicate, entity_objects in entity.predicates.items():
                    if predicate is None or predicate == entity_predicate:
                        for entity_obj in entity_objects:
                            if obj is None or obj == entity_obj:
                                YLogger.debug(None, "Matched tuple subject %s, predicate %s, object %s",
                                              entity_subject, entity_predicate, entity_obj)
                                tuples.append([entity_subject, entity_predicate, entity_obj])
        return tuples

    def not_matched_as_tuples(self, subject=None, predicate=None, obj=None):
        matched_tuples = self.matched_as_tuples(subject, predicate, obj)
        all_tuples = self.all_as_tuples()
        not_matched = []
        for atuple in all_tuples:
            if atuple not in matched_tuples:
                not_matched.append(atuple)

        return not_matched

    def remove(self, entities, subject=None, predicate=None, obj=None):
        if predicate is None and obj is None:
            YLogger.debug(self, "Removing subject=[%s]", subject)
        elif obj is None:
            YLogger.debug(self, "Removing subject=[%s], predicate=[%s]", subject, predicate)
        else:
            YLogger.debug(self, "Removing subject=[%s], predicate=[%s], object=[%s]", subject, predicate, obj)

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

            else:
                YLogger.warning(None, "RDF remove, no subject, predicte or object specified, nothing removed!")

        return [entity for entity in entities if entity not in removes]

    @staticmethod
    def _get_subject_element(subject, entity_subject):
        subj_element = None
        if subject is not None:

            if subject.startswith("?"):
                subj_element = [subject, entity_subject]

            elif subject == entity_subject:
                subj_element = ["subj", entity_subject]

        else:
            subj_element = ["subj", entity_subject]

        return subj_element

    @staticmethod
    def _get_predicate_element(predicate, entity_pred):
        pred_element = None
        if predicate is not None:

            if predicate.startswith("?"):
                pred_element = [predicate, entity_pred]

            elif predicate == entity_pred:
                pred_element = ["pred", entity_pred]

        else:
            pred_element = ["pred", entity_pred]

        return pred_element

    @staticmethod
    def _get_object_elements(entity, obj, entity_pred):

        obj_elements = []
        if obj is not None:

            if obj.startswith("?"):

                for objct in entity.predicates[entity_pred]:
                    obj_elements.append([obj, objct])

            else:

                for objct in entity.predicates[entity_pred]:

                    if objct == obj:
                        obj_elements.append(["obj", objct])
        else:

            for objct in entity.predicates[entity_pred]:
                obj_elements.append(["obj", objct])

        return obj_elements

    def match_to_vars(self, subject=None, predicate=None, obj=None):
        if predicate is None and obj is None:
            YLogger.debug(self, "Matching subject=[%s]", subject)

        elif obj is None:
            YLogger.debug(self, "Matching subject=[%s], predicate=[%s]", subject, predicate)

        else:
            YLogger.debug(self, "Matching subject=[%s], predicate=[%s], object=[%s]", subject, predicate, obj)

        results = []
        for entity_subject, entity in self._entities.items():
            subj_element = RDFCollection._get_subject_element(subject, entity_subject)

            for entity_pred in entity.predicates:

                pred_element = RDFCollection._get_predicate_element(predicate, entity_pred)

                obj_elements = RDFCollection._get_object_elements(entity, obj, entity_pred)

                if subj_element is not None and pred_element is not None and len(obj_elements) > 0:
                    for objct in obj_elements:
                        results.append([subj_element, pred_element, objct])

        return results

    def not_match_to_vars(self, subject=None, predicate=None, obj=None):
        if predicate is None and obj is None:
            YLogger.debug(self, "Not matching subject=[%s]", subject)
        elif obj is None:
            YLogger.debug(self, "Not matching subject=[%s], predicate=[%s]", subject, predicate)
        else:
            YLogger.debug(self, "Not matching subject=[%s], predicate=[%s], object=[%s]", subject, predicate, obj)

        if subject is not None and subject.startswith("?") is True:
            all_subject = subject
        else:
            all_subject = None

        if predicate is not None and predicate.startswith("?") is True:
            all_predicate = predicate
        else:
            all_predicate = None

        if obj is not None and obj.startswith("?") is True:
            all_obj = obj
        else:
            all_obj = None

        all_vars = self.match_to_vars(all_subject, all_predicate, all_obj)

        matched = self.match_to_vars(subject, predicate, obj)

        to_remove = []
        for entity in all_vars:
            for atuple in matched:
                if entity[0][1] == atuple[0][1]:
                    to_remove.append(entity)

        return [entity for entity in all_vars if entity not in to_remove]

    def match_only_vars(self, subject=None, predicate=None, obj=None):
        if predicate is None and obj is None:
            YLogger.debug(self, "Matching only vars subject=[%s]", subject)
        elif obj is None:
            YLogger.debug(self, "Matching only vars subject=[%s], predicate=[%s]", subject, predicate)
        else:
            YLogger.debug(self, "Matching only vars subject=[%s], predicate=[%s], object=[%s]", subject, predicate, obj)

        results = self.match_to_vars(subject, predicate, obj)
        returns = []
        for atuple in results:
            aset = []
            for pair in atuple:
                if pair[0].startswith("?"):
                    aset.append(pair)
            returns.append(aset)

        return returns

    def get_unify_vars(self, variables):
        unified_vars = {}
        for var in variables:
            unified_vars[var] = None
        return unified_vars

    def dict_to_array(self, adict):
        atuple = []
        for name, value in adict.items():
            atuple.append([name, value])
        return atuple

    def unify(self, variables, sets):
        YLogger.debug(self, "Unifying Vars [%s]", variables)

        if not sets:
            return []

        unifications = []
        # For each tuple in the first set
        for atuple in sets[0]:
            # Check to see if there are vars thay need unifying
            unified_vars = self.get_unify_vars(variables)
            if unified_vars:
                # Get the value of the tuples which match the vars
                if self.unify_tuple(atuple, unified_vars) is True:
                    # If we have more sets, keep checking that the vars are still matching
                    unified = True
                    if len(sets) > 1:
                        unified = self.unify_set(1, sets, unified_vars, 0)
                    # If we have unified all variables then we have a match
                    if unified is True and list(unified_vars.values()):
                        unifications.append(self.dict_to_array(unified_vars))

        return unifications

    def unify_set(self, num_set, sets, unified_vars, depth):
        YLogger.debug(self, "Unifying Set")

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

    def unify_tuple(self, tuples, variables):
        YLogger.debug(self, "Unifying Tuple")

        for name, value in tuples:
            if name in variables:
                if variables[name] is None:
                    variables[name] = value
                else:
                    if variables[name] != value:
                        return False

        return True
