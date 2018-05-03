"""
Copyright (c) 2016-2018 Keith Sterling http://www.keithsterling.com

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

from programy.config.section import BaseSectionConfigurationData
from programy.config.brain.security import BrainSecurityAuthenticationConfiguration
from programy.config.brain.security import BrainSecurityAuthorisationConfiguration



class BrainSecuritiesConfiguration(BaseSectionConfigurationData):
    def __init__(self):
        BaseSectionConfigurationData.__init__(self, "security")
        self._authorisation = None
        self._authentication = None

    @property
    def authorisation(self):
        return self._authorisation

    @property
    def authentication(self):
        return self._authentication

    def load_config_section(self, configuration_file, configuration, bot_root):
        securities = configuration_file.get_section(self.section_name, configuration)
        if securities is not None:
            self._authentication = BrainSecurityAuthenticationConfiguration()
            self._authentication.load_config_section(configuration_file, securities, bot_root)

            self._authorisation = BrainSecurityAuthorisationConfiguration()
            self._authorisation.load_config_section(configuration_file, securities, bot_root)

    def to_yaml(self, data, defaults=True):
        self.config_to_yaml(data, BrainSecurityAuthenticationConfiguration(), defaults)
        self.config_to_yaml(data, BrainSecurityAuthorisationConfiguration(), defaults)
