import unittest

from programy.clients.events.console.config import ConsoleConfiguration
from programy.config.brain.dynamic import BrainDynamicsConfiguration
from programy.config.file.yaml_file import YamlConfigurationFile


class BrainDynamicsConfigurationTests(unittest.TestCase):

    def test_with_data(self):
        yaml = YamlConfigurationFile()
        self.assertIsNotNone(yaml)
        yaml.load_from_text("""
        brain:
            dynamic:
                variables:
                    gettime: programy.dynamic.variables.datetime.GetTime
                sets:
                    number: programy.dynamic.sets.numeric.IsNumeric
                    roman:   programy.dynamic.sets.roman.IsRomanNumeral
                maps:
                    romantodec: programy.dynamic.maps.roman.MapRomanToDecimal
                    dectoroman: programy.dynamic.maps.roman.MapDecimalToRoman
        """, ConsoleConfiguration(), ".")

        brain_config = yaml.get_section("brain")

        dynamic_config = BrainDynamicsConfiguration()
        dynamic_config.load_config_section(yaml, brain_config, ".")

        self.assertEquals({'GETTIME': 'programy.dynamic.variables.datetime.GetTime'}, dynamic_config.dynamic_vars)
        self.assertEquals({'NUMBER': 'programy.dynamic.sets.numeric.IsNumeric', 'ROMAN': 'programy.dynamic.sets.roman.IsRomanNumeral'}, dynamic_config.dynamic_sets)
        self.assertEquals({'ROMANTODEC': 'programy.dynamic.maps.roman.MapRomanToDecimal', 'DECTOROMAN': 'programy.dynamic.maps.roman.MapDecimalToRoman'}, dynamic_config.dynamic_maps)

    def test_with_missing_vars_sets_maps(self):
        yaml = YamlConfigurationFile()
        self.assertIsNotNone(yaml)
        yaml.load_from_text("""
        brain:
            dynamic:
        """, ConsoleConfiguration(), ".")

        brain_config = yaml.get_section("brain")

        dynamic_config = BrainDynamicsConfiguration()
        dynamic_config.load_config_section(yaml, brain_config, ".")

        self.assertEquals({}, dynamic_config.dynamic_vars)
        self.assertEquals({}, dynamic_config.dynamic_sets)
        self.assertEquals({}, dynamic_config.dynamic_maps)

    def test_with_missing_vars_sets_maps2(self):
        yaml = YamlConfigurationFile()
        self.assertIsNotNone(yaml)
        yaml.load_from_text("""
        brain:
            dynamic:
                something: else
        """, ConsoleConfiguration(), ".")

        brain_config = yaml.get_section("brain")

        dynamic_config = BrainDynamicsConfiguration()
        dynamic_config.load_config_section(yaml, brain_config, ".")

        self.assertEquals({}, dynamic_config.dynamic_vars)
        self.assertEquals({}, dynamic_config.dynamic_sets)
        self.assertEquals({}, dynamic_config.dynamic_maps)

    def test_without_data(self):
        yaml = YamlConfigurationFile()
        self.assertIsNotNone(yaml)
        yaml.load_from_text("""
        brain:
            dynamic:
        """, ConsoleConfiguration(), ".")

        brain_config = yaml.get_section("brain")

        dynamic_config = BrainDynamicsConfiguration()
        dynamic_config.load_config_section(yaml, brain_config, ".")

        self.assertEquals({}, dynamic_config.dynamic_vars)
        self.assertEquals({}, dynamic_config.dynamic_sets)
        self.assertEquals({}, dynamic_config.dynamic_maps)

    def test_with_no_data(self):
        yaml = YamlConfigurationFile()
        self.assertIsNotNone(yaml)
        yaml.load_from_text("""
        brain:
        """, ConsoleConfiguration(), ".")

        brain_config = yaml.get_section("brain")

        dynamic_config = BrainDynamicsConfiguration()
        dynamic_config.load_config_section(yaml, brain_config, ".")

        self.assertEquals({}, dynamic_config.dynamic_vars)
        self.assertEquals({}, dynamic_config.dynamic_sets)
        self.assertEquals({}, dynamic_config.dynamic_maps)

    def test_to_yaml_defaults(self):
        yaml = {}
        dynamic_config = BrainDynamicsConfiguration()
        dynamic_config.to_yaml(yaml, defaults=True)

        self.assertEquals({'GETTIME': 'programy.dynamic.variables.datetime.GetTime'}, yaml['variables'])
        self.assertEquals({'NUMBER': 'programy.dynamic.sets.numeric.IsNumeric',
                           'ROMAN': 'programy.dynamic.sets.roman.IsRomanNumeral',
                           'STOPWORD': 'programy.dynamic.sets.stopword.IsStopWord',
                           'SYNSETS': 'programy.dynamic.sets.synsets.IsSynset'},  yaml['sets'])
        self.assertEquals({'ROMANTODDEC': 'programy.dynamic.maps.roman.MapRomanToDecimal',
                           'DECTOROMAN': 'programy.dynamic.maps.roman.MapDecimalToRoman',
                           'LEMMATIZE': 'programy.dynamic.maps.lemmatize.LemmatizeMap',
                           'STEMMER': 'programy.dynamic.maps.stemmer.StemmerMap'},  yaml['maps'])

    def test_to_yaml_no_defaults(self):
        yaml = YamlConfigurationFile()
        self.assertIsNotNone(yaml)
        yaml.load_from_text("""
        brain:
            dynamic:
                variables:
                    gettime: programy.dynamic.variables.datetime.GetTime
                sets:
                    number: programy.dynamic.sets.numeric.IsNumeric
                    roman:   programy.dynamic.sets.roman.IsRomanNumeral
                maps:
                    romantodec: programy.dynamic.maps.roman.MapRomanToDecimal
                    dectoroman: programy.dynamic.maps.roman.MapDecimalToRoman
        """, ConsoleConfiguration(), ".")

        brain_config = yaml.get_section("brain")

        dynamic_config = BrainDynamicsConfiguration()
        dynamic_config.load_config_section(yaml, brain_config, ".")

        data = {}
        dynamic_config.to_yaml(data, defaults=False)

        self.assertEquals({'GETTIME': 'programy.dynamic.variables.datetime.GetTime'}, data['variables'])
        self.assertEquals({'NUMBER': 'programy.dynamic.sets.numeric.IsNumeric', 'ROMAN': 'programy.dynamic.sets.roman.IsRomanNumeral'}, data['sets'])
        self.assertEquals({'ROMANTODEC': 'programy.dynamic.maps.roman.MapRomanToDecimal', 'DECTOROMAN': 'programy.dynamic.maps.roman.MapDecimalToRoman'}, data['maps'])

    def test_to_yaml_no_defaults_no_data(self):
        yaml = {}
        dynamic_config = BrainDynamicsConfiguration()
        dynamic_config.to_yaml(yaml, defaults=False)

        self.assertEquals({}, yaml['variables'])
        self.assertEquals({},  yaml['sets'])
        self.assertEquals({},  yaml['maps'])

    def test_defaults(self):
        dynamic_config = BrainDynamicsConfiguration()
        data = {}
        dynamic_config.to_yaml(data, True)

        BrainDynamicsConfigurationTests.assert_defaults(self, data)

    @staticmethod
    def assert_defaults(test, data):
        test.assertTrue('sets' in data)
        test.assertEqual(data['sets']['NUMBER'], 'programy.dynamic.sets.numeric.IsNumeric')
        test.assertEqual(data['sets']['ROMAN'], 'programy.dynamic.sets.roman.IsRomanNumeral')
        test.assertEqual(data['sets']['STOPWORD'], 'programy.dynamic.sets.stopword.IsStopWord')
        test.assertEqual(data['sets']['SYNSETS'], 'programy.dynamic.sets.synsets.IsSynset')

        test.assertTrue('maps' in data)
        test.assertEqual(data['maps']['ROMANTODDEC'], 'programy.dynamic.maps.roman.MapRomanToDecimal')
        test.assertEqual(data['maps']['DECTOROMAN'], 'programy.dynamic.maps.roman.MapDecimalToRoman')
        test.assertEqual(data['maps']['LEMMATIZE'], 'programy.dynamic.maps.lemmatize.LemmatizeMap')
        test.assertEqual(data['maps']['STEMMER'], 'programy.dynamic.maps.stemmer.StemmerMap')

        test.assertTrue('variables' in data)
        test.assertEqual(data['variables']['GETTIME'], 'programy.dynamic.variables.datetime.GetTime')
