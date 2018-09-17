import unittest
import os
import os.path

from programy.rdf.collection import RDFCollection
from programy.storage.entities.store import Store


class RDFStoreAsserts(unittest.TestCase):

    def assert_rdf_storage(self, store):

        store.empty()

        store.add_rdf("ACTIVITY", "ACT", "hasPurpose", "to entertain by performing")
        store.add_rdf("ACTIVITY", "ACT", "hasSize", "0")
        store.add_rdf("ACTIVITY", "ACT", "hasSyllables", "1")
        store.add_rdf("ACTIVITY", "ACT", "isa", "Activity0")
        store.add_rdf("ACTIVITY", "ACT", "lifeArea", "Recreation")
        store.commit()

        rdf_collection = RDFCollection()
        store.load(rdf_collection, "ACTIVITY")

        self.assertTrue(rdf_collection.contains("ACTIVITY"))
        self.assertTrue(rdf_collection.has_subject('ACT'))
        self.assertTrue(rdf_collection.has_predicate('ACT', "hasPurpose"))
        self.assertTrue(rdf_collection.has_object('ACT', "hasPurpose", "to entertain by performing"))

    def assert_upload_from_text(self, store):

        store.empty()

        store.upload_from_text("ACTIVITY", """
            ACT:hasPurpose:to entertain by performing
            ACT:hasSize:0
            ACT:hasSyllables:1
            ACT:isa:Activity
            ACT:lifeArea:Recreation
            ADVENTURE:hasPurpose:to provide new experience
            ADVENTURE:hasSize:0
            ADVENTURE:hasSyllables:3
            ADVENTURE:isa:Activity
            ADVENTURE:lifeArea:Recreation
            FISHING:hasPurpose:to hunt for fish
            FISHING:hasSize:0
            FISHING:hasSyllables:2
            FISHING:isa:Activity
            FISHING:lifeArea:Recreation
            """)

        rdf_collection = RDFCollection()
        store.load(rdf_collection, "ACTIVITY")

        self.assertTrue(rdf_collection.contains("ACTIVITY"))
        self.assertTrue(rdf_collection.has_subject('ACT'))
        self.assertTrue(rdf_collection.has_predicate('ACT', "hasPurpose"))
        self.assertTrue(rdf_collection.has_object('ACT', "hasPurpose", "to entertain by performing"))

    def assert_upload_from_text_file(self, store):
        store.empty()

        store.upload_from_file(os.path.dirname(__file__)+os.sep+"data"+os.sep+"rdfs"+os.sep+"text"+os.sep+"activity.rdf")

        rdf_collection = RDFCollection()
        store.load(rdf_collection, "ACTIVITY")

        self.assertTrue(rdf_collection.contains("ACTIVITY"))
        self.assertTrue(rdf_collection.has_subject('ACT'))
        self.assertTrue(rdf_collection.has_predicate('ACT', "hasPurpose"))
        self.assertTrue(rdf_collection.has_object('ACT', "hasPurpose", "to entertain by performing"))

    def assert_upload_text_files_from_directory_no_subdir(self, store):

        store.empty()

        store.upload_from_directory(os.path.dirname(__file__)+os.sep+"data"+os.sep+"rdfs"+os.sep+"text", subdir=False)

        rdf_collection = RDFCollection()
        store.load(rdf_collection, "ACTIVITY")

        self.assertTrue(rdf_collection.contains("ACTIVITY"))
        self.assertTrue(rdf_collection.has_subject('ACT'))
        self.assertTrue(rdf_collection.has_predicate('ACT', "hasPurpose"))
        self.assertTrue(rdf_collection.has_object('ACT', "hasPurpose", "to entertain by performing"))

    def assert_upload_from_csv_file(self, store):

        store.empty()

        store.upload_from_file(os.path.dirname(__file__)+os.sep+"data"+os.sep+"rdfs"+os.sep+"csv"+os.sep+"activity.csv", format=Store.CSV_FORMAT)

        rdf_collection = RDFCollection()
        store.load(rdf_collection, "ACTIVITY")

        self.assertTrue(rdf_collection.contains("ACTIVITY"))
        self.assertTrue(rdf_collection.has_subject('ACT'))
        self.assertTrue(rdf_collection.has_predicate('ACT', "hasPurpose"))
        self.assertTrue(rdf_collection.has_object('ACT', "hasPurpose", "to entertain by performing"))

    def assert_upload_csv_files_from_directory_with_subdir(self, store):

        store.empty()

        store.upload_from_directory(os.path.dirname(__file__)+os.sep+"data"+os.sep+"rdfs"+os.sep+"csv", subdir=True, format=Store.CSV_FORMAT)

        rdf_collection = RDFCollection()
        store.load_all(rdf_collection)

        self.assertTrue(rdf_collection.contains("ACTIVITY"))
        self.assertTrue(rdf_collection.has_subject('ACT'))
        self.assertTrue(rdf_collection.has_predicate('ACT', "hasPurpose"))
        self.assertTrue(rdf_collection.has_object('ACT', "hasPurpose", "to entertain by performing"))

        self.assertTrue(rdf_collection.contains("ANIMAL"))
        self.assertTrue(rdf_collection.has_subject('ANT'))
        self.assertTrue(rdf_collection.has_predicate('ANT', "hasPurpose"))
        self.assertTrue(rdf_collection.has_object('ANT', "hasPurpose", "to make anthills"))

