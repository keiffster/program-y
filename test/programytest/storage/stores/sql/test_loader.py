import unittest
from unittest.mock import patch
import os
from programy.storage.stores.sql.loader import Uploader


class MockArguments:

    def __init__(self):
        self.entity = None
        self.url = None
        self.file = None
        self.dir = None
        self.subdir = None
        self.extension = None
        self.create=None
        self.drop = None
        self.verbose = None


class SQLUploaderTests(unittest.TestCase):

    def setUp(self) -> None:
        self.basepath = os.path.dirname(__file__) + os.sep + ".." + os.sep + ".." + "/asserts/store/data/"

    def test_create_arguments(self):
        arguments = Uploader.create_arguments()
        self.assertIsNotNone(arguments)

    def test_run_no_args(self):
        Uploader.run()

    @staticmethod
    def patch_get_args(arguments):
        args = MockArguments()
        args.entity = "categories"
        args.url = "mysql+pymysql://root:Password123@localhost:3306/programy"
        args.file = None
        args.dir = os.path.dirname(__file__) + os.sep + ".." + os.sep + ".." + os.sep + ".." + "/asserts/store/data/" + "categories"
        args.subdir = True
        args.extension = ".aiml"
        args.drop = False
        args.create = True
        args.verbose = False
        return args

    @patch("programy.storage.stores.sql.loader.Uploader.get_args", patch_get_args)
    def test_run(self):
        Uploader.run()

    @staticmethod
    def patch_get_args2(arguments):
        args = MockArguments()
        args.url = "mysql+pymysql://root:Password123@localhost:3306/programy"
        args.drop = True
        return args

    @patch("programy.storage.stores.sql.loader.Uploader.get_args", patch_get_args2)
    def test_run(self):
        Uploader.run()

    @staticmethod
    def patch_get_args3(arguments):
        raise Exception("Mock Exception")

    @patch("programy.storage.stores.sql.loader.Uploader.get_args", patch_get_args3)
    def test_run_with_exception(self):
        Uploader.run()

    def test_upload_unknown(self):
        with self.assertRaises(Exception):
            Uploader.upload(storetype='other',
                             url='mysql+pymysql://root:Password123@localhost:3306/programy',
                             filename=None,
                             dirname=self.basepath + "categories",
                             subdir=True, extension=".aiml",
                             create=True)

    def test_upload_no_dir_or_file(self):
        with self.assertRaises(Exception):
            Uploader.upload(storetype='categories',
                             url='mysql+pymysql://root:Password123@localhost:3306/programy',
                             filename=None,
                             dirname=None,
                             subdir=True, extension=".aiml",
                             create=True)

    def test_upload_categories(self):
        count, success = Uploader.upload(storetype='categories',
                                         url='mysql+pymysql://root:Password123@localhost:3306/programy',
                                         filename=None,
                                         dirname=self.basepath + "categories",
                                         subdir=True, extension=".aiml",
                                         create=True)
        self.assertEquals(9, count)
        self.assertEquals(9, success)

    def test_upload_maps(self):
        count, success = Uploader.upload(storetype='maps',
                                         url='mysql+pymysql://root:Password123@localhost:3306/programy',
                                         filename=None,
                                         dirname=self.basepath + "maps" + os.sep + "text",
                                         subdir=True, extension=".txt",
                                         create=True)
        self.assertEquals(11, count)
        self.assertEquals(11, success)

    def test_upload_sets(self):
        count, success = Uploader.upload(storetype='sets',
                                         url='mysql+pymysql://root:Password123@localhost:3306/programy',
                                         filename=None,
                                         dirname=self.basepath + "sets" + os.sep + "text",
                                         subdir=True, extension=".txt",
                                         create=True)
        self.assertEquals(8, count)
        self.assertEquals(8, success)

    def test_upload_rdfs(self):
        count, success = Uploader.upload(storetype='rdfs',
                                         url='mysql+pymysql://root:Password123@localhost:3306/programy',
                                         filename=None,
                                         dirname=self.basepath + "rdfs" + os.sep + "text",
                                         subdir=True, extension=".rdf",
                                         create=True)
        self.assertEquals(851, count)
        self.assertEquals(850, success)

    def test_upload_denormals(self):
        count, success = Uploader.upload(storetype='denormals',
                                         url='mysql+pymysql://root:Password123@localhost:3306/programy',
                                         filename=self.basepath + "lookups" + os.sep + "text" + os.sep + "denormal.txt",
                                         dirname=None,
                                         subdir=True, extension=".txt",
                                         create=True)
        self.assertEquals(138, count)
        self.assertEquals(124, success)


    def test_upload_normals(self):
        count, success = Uploader.upload(storetype='normals',
                                         url='mysql+pymysql://root:Password123@localhost:3306/programy',
                                         filename=self.basepath + "lookups" + os.sep + "text" + os.sep + "normal.txt",
                                         dirname=None,
                                         subdir=True, extension=".txt",
                                         create=True)
        self.assertEquals(459, count)
        self.assertEquals(458, success)

    def test_upload_genders(self):
        count, success = Uploader.upload(storetype='genders',
                                         url='mysql+pymysql://root:Password123@localhost:3306/programy',
                                         filename=self.basepath + "lookups" + os.sep + "text" + os.sep + "gender.txt",
                                         dirname=None,
                                         subdir=True, extension=".txt",
                                         create=True)
        self.assertEquals(16, count)
        self.assertEquals(15, success)

    def test_upload_persons(self):
        count, success = Uploader.upload(storetype='persons',
                                         url='mysql+pymysql://root:Password123@localhost:3306/programy',
                                         filename=self.basepath + "lookups" + os.sep + "text" + os.sep + "person.txt",
                                         dirname=None,
                                         subdir=True, extension=".txt",
                                         create=True)
        self.assertEquals(57, count)
        self.assertEquals(52, success)

    def test_upload_person2s(self):
        count, success = Uploader.upload(storetype='person2s',
                                         url='mysql+pymysql://root:Password123@localhost:3306/programy',
                                         filename=self.basepath + "lookups" + os.sep + "text" + os.sep + "person2.txt",
                                         dirname=None,
                                         subdir=True, extension=".txt",
                                         create=True)
        self.assertEquals(9, count)
        self.assertEquals(9, success)

    def test_upload_properties(self):
        count, success = Uploader.upload(storetype='properties',
                                         url='mysql+pymysql://root:Password123@localhost:3306/programy',
                                         filename=self.basepath + "lookups" + os.sep + "text" + os.sep + "properties.txt",
                                         dirname=None,
                                         subdir=True, extension=".txt",
                                         create=True)
        self.assertEquals(93, count)
        self.assertEquals(80, success)

    def test_upload_defaults(self):
        count, success = Uploader.upload(storetype='defaults',
                                         url='mysql+pymysql://root:Password123@localhost:3306/programy',
                                         filename=self.basepath + "lookups" + os.sep + "text" + os.sep + "defaults.txt",
                                         dirname=None,
                                         subdir=True, extension=".txt",
                                         create=True)
        self.assertEquals(2, count)
        self.assertEquals(2, success)

    def test_upload_regexes(self):
        count, success = Uploader.upload(storetype='regexes',
                                         url='mysql+pymysql://root:Password123@localhost:3306/programy',
                                         filename=self.basepath + "lookups" + os.sep + "text" + os.sep + "regex-templates.txt",
                                         dirname=None,
                                         subdir=True, extension=".txt",
                                         create=True)
        self.assertEquals(16, count)
        self.assertEquals(16, success)

    def test_upload_patternnodes(self):
        count, success = Uploader.upload(storetype='patternnodes',
                                         url='mysql+pymysql://root:Password123@localhost:3306/programy',
                                         filename=self.basepath + "lookups" + os.sep + "text" + os.sep + "pattern_nodes.conf",
                                         dirname=None,
                                         subdir=True, extension=".conf",
                                         create=True)
        self.assertEquals(17, count)
        self.assertEquals(12, success)

    def test_upload_templatenodes(self):
        count, success = Uploader.upload(storetype='templatenodes',
                                         url='mysql+pymysql://root:Password123@localhost:3306/programy',
                                         filename=self.basepath + "lookups" + os.sep + "text" + os.sep + "template_nodes.conf",
                                         dirname=None,
                                         subdir=True, extension=".conf",
                                         create=True)
        self.assertEquals(71, count)
        self.assertEquals(64, success)

    def test_upload_preprocessors(self):
        count, success = Uploader.upload(storetype='preprocessors',
                                         url='mysql+pymysql://root:Password123@localhost:3306/programy',
                                         filename=self.basepath + "lookups" + os.sep + "text" + os.sep + "preprocessors.conf",
                                         dirname=None,
                                         subdir=True, extension=".conf",
                                         create=True)
        self.assertEquals(2, count)
        self.assertEquals(2, success)

    def test_upload_postprocessors(self):
        count, success = Uploader.upload(storetype='postprocessors',
                                         url='mysql+pymysql://root:Password123@localhost:3306/programy',
                                         filename=self.basepath + "lookups" + os.sep + "text" + os.sep + "postprocessors.conf",
                                         dirname=None,
                                         subdir=True, extension=".conf")
        self.assertEquals(6, count)
        self.assertEquals(5, success)

    def test_upload_postquestionprocessors(self):
        count, success = Uploader.upload(storetype='postquestionprocessors',
                                         url='mysql+pymysql://root:Password123@localhost:3306/programy',
                                         filename=self.basepath + "lookups" + os.sep + "text" + os.sep + "postquestionprocessors.conf",
                                         dirname=None,
                                         subdir=True, extension=".conf",
                                         create=True)
        self.assertEquals(6, count)
        self.assertEquals(5, success)

    def test_upload_spelling(self):
        count, success = Uploader.upload(storetype='spelling',
                                         url='mysql+pymysql://root:Password123@localhost:3306/programy',
                                         filename=self.basepath + "spelling" + os.sep + "corpus.txt",
                                         dirname=None,
                                         subdir=True, extension=".txt",
                                         create=True)
        self.assertEquals(9, count)
        self.assertEquals(9, success)

    def test_upload_licenses(self):
        count, success = Uploader.upload(storetype='licenses',
                                         url='mysql+pymysql://root:Password123@localhost:3306/programy',
                                         filename=self.basepath + "licenses" + os.sep + "test_license.keys",
                                         dirname=None,
                                         subdir=True, extension=".txt",
                                         create=True)
        self.assertEquals(4, count)
        self.assertEquals(2, success)

    def test_upload_usergroups(self):
        count, success = Uploader.upload(storetype='usergroups',
                                         url='mysql+pymysql://root:Password123@localhost:3306/programy',
                                         filename=self.basepath + "security" + os.sep + "roles.yaml",
                                         dirname=None,
                                         subdir=True, extension=".txt",
                                         create=True)
        self.assertEquals(1, count)
        self.assertEquals(1, success)

    def test_upload_triggers(self):
        count, success = Uploader.upload(storetype='triggers',
                                         url='mysql+pymysql://root:Password123@localhost:3306/programy',
                                         filename=self.basepath + "triggers" + os.sep + "triggers.txt",
                                         dirname=None,
                                         subdir=True, extension=".txt",
                                         create=True)
        self.assertEquals(4, count)
        self.assertEquals(4, success)

    def test_upload_oobs(self):
        count, success = Uploader.upload(storetype='oobs',
                                         url='mysql+pymysql://root:Password123@localhost:3306/programy',
                                         filename=self.basepath + "oobs" + os.sep + "callmom.conf",
                                         dirname=None,
                                         subdir=True, extension=".conf",
                                         create=True)
        self.assertEquals(13, count)
        self.assertEquals(13, success)

    def test_upload_services(self):
        count, success = Uploader.upload(storetype='services',
                                         url='mysql+pymysql://root:Password123@localhost:3306/programy',
                                         filename=None,
                                         dirname=self.basepath + "services",
                                         subdir=True, extension=".yaml",
                                         create=True)
        self.assertEquals(1, count)
        self.assertEquals(1, success)
