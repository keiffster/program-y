"""
Copyright (c) 2016-2019 Keith Sterling http://www.keithsterling.com

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


class BrainOverridesConfiguration(BaseSectionConfigurationData):

    def __init__(self):
        BaseSectionConfigurationData.__init__(self, "overrides")
        self._allow_system_aiml = False
        self._allow_learn_aiml = False
        self._allow_learnf_aiml = False

    @property
    def allow_system_aiml(self):
        return self._allow_system_aiml

    @property
    def allow_learn_aiml(self):
        return self._allow_learn_aiml

    @property
    def allow_learnf_aiml(self):
        return self._allow_learnf_aiml

    def check_for_license_keys(self, license_keys):
        BaseSectionConfigurationData.check_for_license_keys(self, license_keys)

    def load_config_section(self, configuration_file, configuration, bot_root, subs: Substitutions = None):
        overrides = configuration_file.get_section(self._section_name, configuration)
        if overrides is not None:
            self._allow_system_aiml = configuration_file.get_bool_option(overrides, "allow_system_aiml", missing_value=False, subs=subs)
            self._allow_learn_aiml = configuration_file.get_bool_option(overrides, "allow_learn_aiml", missing_value=False, subs=subs)
            self._allow_learnf_aiml = configuration_file.get_bool_option(overrides, "allow_learnf_aiml", missing_value=False, subs=subs)
        else:
            YLogger.warning(self, "'overrides' section missing from brain config, using to defaults")

    def to_yaml(self, data, defaults=True):
        if defaults is True:
            data['allow_system_aiml'] = False
            data['allow_learn_aiml'] = False
            data['allow_learnf_aiml'] = False
        else:
            data['allow_system_aiml'] = self._allow_system_aiml
            data['allow_learn_aiml'] = self._allow_learn_aiml
            data['allow_learnf_aiml'] = self._allow_learnf_aiml
