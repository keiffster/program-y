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

from programy.config.container import BaseContainerConfigurationData
from programy.utils.substitutions.substitues import Substitutions


class TriggerConfiguration(BaseContainerConfigurationData):

    LOCAL_MANAGER = "programy.triggers.local.LocalTriggerManager"
    REST_MANAGER = "programy.triggers.rest.RestTriggerManager"

    def __init__(self, name="triggers"):
        BaseContainerConfigurationData.__init__(self, name)
        self._manager = TriggerConfiguration.LOCAL_MANAGER

    @property
    def manager(self):
        return self._manager

    def additionals_to_add(self):
        return ["url", "method", "token"]

    def load_config_section(self, configuration_file, section, bot_root, subs: Substitutions = None):
        triggers = configuration_file.get_section(self._section_name, section)
        if triggers is not None:
            self._manager = configuration_file.get_option(triggers, "manager", missing_value=TriggerConfiguration.LOCAL_MANAGER)
            self.load_additional_key_values(configuration_file, triggers)
        else:
            YLogger.warning(self, "'triggers' section missing from client config, using defaults")

    def to_yaml(self, data, defaults=True):

        assert (data is not None)

        if defaults is True:
            data['manager'] = TriggerConfiguration.LOCAL_MANAGER

        else:
            data['manager'] = self._manager
