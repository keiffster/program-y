import unittest
import os

from programy.config.file.xml_file import XMLConfigurationFile
from programy.config.client.client import ClientConfiguration


class XMLConfigurationFileTests(unittest.TestCase):

    def test_load_from_file(self):
        client_config = ClientConfiguration()
        xml = XMLConfigurationFile(client_config)
        self.assertIsNotNone(xml)
        xml.load_from_file(os.path.dirname(__file__)+"/test_xml.xml", ",")
        self.assertIsNotNone(xml.xml_data)
        brain = xml.get_section("brain")
        self.assertIsNotNone(brain)
        files = xml.get_section("files", brain)
        self.assertIsNotNone(files)
        aiml = xml.get_section("aiml", files)
        self.assertIsNotNone(aiml)

        depth_str = xml.get_option(brain, "max_depth")
        self.assertEqual('100', depth_str)
        supress_warnings = xml.get_bool_option(brain, "supress_warnings")
        self.assertTrue(supress_warnings)
        depth_int = xml.get_int_option(brain, "max_depth")
        self.assertEqual(100, depth_int)

        with self.assertRaises(Exception):
            xml.get_bool_option(brain, "max_depth")

        with self.assertRaises(Exception):
            xml.get_int_option(brain, "supress_warnings")

        other_depth = xml.get_option(brain, "max_other_depth", 50)
        self.assertEqual(50, other_depth)
        supress_other_warnings = xml.get_bool_option(brain, "supress_other_warnings", True)
        self.assertTrue(supress_other_warnings)
        other_depth_int = xml.get_int_option(brain, "other_depth_int", 999)
        self.assertEqual(999, other_depth_int)

        files = xml.get_section("files", aiml)
        self.assertIsNotNone(files)
        self.assertEqual(files.text, "/aiml")
        extension = xml.get_section("extension", aiml)
        self.assertIsNotNone(extension)
        self.assertEqual(extension.text, ".aiml")
        directories = xml.get_section("directories", aiml)
        self.assertIsNotNone(directories)
        self.assertEqual(directories.text, "True")

    def test_load_from_text(self):
        client_config = ClientConfiguration()
        xml = XMLConfigurationFile(client_config)
        self.assertIsNotNone(xml)
        xml.load_from_text("""<?xml version="1.0" encoding="UTF-8"?>
<configuration>
    <brain>
        <supress_warnings>True</supress_warnings>
        <allow_system_aiml>True</allow_system_aiml>
        <allow_learn_aiml>True</allow_learn_aiml>
        <allow_learnf_aiml>True</allow_learnf_aiml>

       <files>
           <aiml>
               <files>/aiml</files>
               <extension>.aiml</extension>
               <directories>True</directories>
           </aiml>
           <sets>
               <files>/sets</files>
               <extension>.txt</extension>
               <directories>False</directories>
           </sets>
           <maps>
               <files>/maps</files>
               <extension>.txt</extension>
               <directories>True</directories>
           </maps>
            <denormal>denormal.txt</denormal>
            <normal>normal.txt</normal>
            <gender>gender.txt</gender>
            <person>person.txt</person>
            <person2>person2.txt</person2>
            <predicates>predicates.txt</predicates>
            <pronouns>pronouns.txt</pronouns>
            <properties>properties.txt</properties>
            <triples>triples.txt</triples>
            <preprocessors>preprocessors.txt</preprocessors>
            <postprocessors>postprocessors.txt</postprocessors>
       </files>
        <services>
            <REST>
                <path>programy.utils.services.rest.GenericRESTService</path>
            </REST>
            <Pannous>
                <path>programy.utils.services.pannous.PannousService</path>
            </Pannous>
            <Pandora>
                <path>programy.utils.services.pandora.PandoraService</path>
            </Pandora>
            <Wikipedia>
                <path>programy.utils.services.wikipedia.WikipediaService</path>
            </Wikipedia>
        </services>
    </brain>
    <bot>
        <prompt>>>></prompt>
        <default_response>Sorry, I don't have an answer for that!</default_response>
        <exit_response>So long, and thanks for the fish!</exit_response>
        <initial_question>Hi, how can I help you?</initial_question>
    </bot>
</configuration>
""", ",")

