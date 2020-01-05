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

from programy.config.section import BaseSectionConfigurationData
from programy.utils.substitutions.substitues import Substitutions


class BrainDynamicsConfiguration(BaseSectionConfigurationData):

    def __init__(self):
        BaseSectionConfigurationData.__init__(self, "dynamic")
        self._dynamic_sets = {}
        self._dynamic_maps = {}
        self._dynamic_vars = {}

    @property
    def dynamic_sets(self):
        return self._dynamic_sets

    @property
    def dynamic_maps(self):
        return self._dynamic_maps

    @property
    def dynamic_vars(self):
        return self._dynamic_vars

    def load_config_section(self, configuration_file, configuration, bot_root, subs: Substitutions = None):
        dynamic_config = configuration_file.get_section("dynamic", configuration)
        if dynamic_config is not None:
            self.load_dynamic_sets(configuration_file, dynamic_config, subs=subs)
            self.load_dynamic_maps(configuration_file, dynamic_config, subs=subs)
            self.load_dynamic_vars(configuration_file, dynamic_config, subs=subs)
        else:
            YLogger.error(self, "Config section [dynamic] missing from Brain, using defaults")

    def load_dynamic_sets(self, configuration_file, dynamic_config, subs: Substitutions = None):
        sets_config = configuration_file.get_option(dynamic_config, "sets", subs=subs)
        if sets_config is not None:
            for set_key in sets_config.keys():
                dyn_set_class = sets_config[set_key]
                self._dynamic_sets[set_key.upper()] = dyn_set_class

    def load_dynamic_maps(self, configuration_file, dynamic_config, subs: Substitutions = None):
        maps_config = configuration_file.get_option(dynamic_config, "maps", subs=subs)
        if maps_config is not None:
            for map_name in maps_config.keys():
                dyn_map_class = maps_config[map_name]
                self._dynamic_maps[map_name.upper()] = dyn_map_class

    def load_dynamic_vars(self, configuration_file, dynamic_config, subs: Substitutions = None):
        vars_config = configuration_file.get_option(dynamic_config, "variables", subs=subs)
        if vars_config is not None:
            for var_name in vars_config.keys():
                dyn_var_class = vars_config[var_name]
                self._dynamic_vars[var_name.upper()] = dyn_var_class

    def to_yaml(self, data, defaults=True):
        if defaults is True:
            data['sets'] = {}
            data['sets']['NUMBER'] = 'programy.dynamic.sets.numeric.IsNumeric'
            data['sets']['ROMAN'] = 'programy.dynamic.sets.roman.IsRomanNumeral'
            data['sets']['STOPWORD'] = 'programy.dynamic.sets.stopword.IsStopWord'
            data['sets']['SYNSETS'] = 'programy.dynamic.sets.synsets.IsSynset'

            data['maps'] = {}
            data['maps']['ROMANTODDEC'] = 'programy.dynamic.maps.roman.MapRomanToDecimal'
            data['maps']['DECTOROMAN'] = 'programy.dynamic.maps.roman.MapDecimalToRoman'
            data['maps']['LEMMATIZE'] = 'programy.dynamic.maps.lemmatize.LemmatizeMap'
            data['maps']['STEMMER'] = 'programy.dynamic.maps.stemmer.StemmerMap'

            data['variables'] = {}
            data['variables']['GETTIME'] = 'programy.dynamic.variables.datetime.GetTime'

        else:
            data['sets'] = {}
            for key, value in self._dynamic_sets.items():
                data['sets'][key] = value

            data['maps'] = {}
            for key, value in self._dynamic_maps.items():
                data['maps'][key] = value

            data['variables'] = {}
            for key, value in self._dynamic_vars.items():
                data['variables'][key] = value
