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
from programy.config.brain.openchatbot import BrainOpenChatBotConfiguration
from programy.utils.substitutions.substitues import Substitutions


class BrainOpenChatBotsConfiguration(BaseSectionConfigurationData):

    def __init__(self):
        BaseSectionConfigurationData.__init__(self, "openchatbots")
        self._openchatbots = {}
        self._protocols = ['http']
        self._domains = []

    @property
    def protocols(self):
        return self._protocols

    @property
    def domains(self):
        return self._domains

    def exists(self, name):
        return bool(name in self._openchatbots)

    def openchatbot(self, name):
        if name in self._openchatbots:
            return self._openchatbots[name]
        return None

    def openchatbots(self):
        return self._openchatbots.keys()

    def check_for_license_keys(self, license_keys):
        BaseSectionConfigurationData.check_for_license_keys(self, license_keys)

    def load_config_section(self, configuration_file, configuration, bot_root, subs: Substitutions = None):
        openchatbots = configuration_file.get_section(self.section_name, configuration)
        if openchatbots is not None:
            openchatbot_keys = configuration_file.get_keys(openchatbots)

            for name in openchatbot_keys:
                if name == 'protocols':
                    protocols = configuration_file.get_option(openchatbots, "protocols", missing_value=['http'], subs=subs)
                    self._protocols = [x.strip() for x in protocols.split(",")]
                elif name == 'domains':
                    domains = configuration_file.get_option(openchatbots, "domains", missing_value=[], subs=subs)
                    self._domains = [x.strip() for x in domains.split(",")]
                else:
                    openchatbot = BrainOpenChatBotConfiguration(name)
                    openchatbot.load_config_section(configuration_file, openchatbots, bot_root, subs=subs)
                    self._openchatbots[name] = openchatbot

        else:
            YLogger.warning(self, "Config section [openchatbots] missing from Brain, no openchatbots loaded")

    def to_yaml(self, data, defaults=True):
        if defaults is True:
            data['openchatbots'] = self._openchatbots
            data['protocols'] = self._protocols
            data['domains'] = self._domains
        else:
            data['openchatbots'] = {}
            data['protocols'] = ['http']
            data['domains'] = []
