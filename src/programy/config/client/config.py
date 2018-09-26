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
from programy.utils.logging.ylogger import YLogger

from programy.config.container import BaseContainerConfigurationData
from programy.config.bot.bot import BotConfiguration
from programy.scheduling.config import SchedulerConfiguration
from programy.storage.config import StorageConfiguration

class ClientConfigurationData(BaseContainerConfigurationData):

    def __init__(self, name):
        BaseContainerConfigurationData.__init__(self, name)
        self._description = 'ProgramY AIML2.0 Client'
        self._bot_configs = []
        self._bot_configs.append(BotConfiguration("bot"))
        self._bot_selector = None
        self._scheduler = SchedulerConfiguration()
        self._storage = StorageConfiguration()
        self._renderer = None

    @property
    def description(self):
        return self._description

    @property
    def configurations(self):
        return self._bot_configs

    @property
    def bot_selector(self):
        return self._bot_selector

    @property
    def scheduler(self):
        return self._scheduler

    @property
    def storage(self):
        return self._storage

    @property
    def renderer(self):
        return self._renderer

    def load_configuration(self, configuration_file, section, bot_root):

        assert(configuration_file is not None)

        if section is not None:
            self._description = configuration_file.get_option(section, "description", missing_value='ProgramY AIML2.0 Client')

            bot_names = configuration_file.get_multi_option(section, "bot", missing_value="bot")
            first = True
            for name in bot_names:
                if first is True:
                    config = self._bot_configs[0]
                    first = False
                else:
                    config = BotConfiguration(name)
                    self._bot_configs.append(config)
                config.load_configuration(configuration_file, bot_root)

            self._bot_selector = configuration_file.get_option(section, "bot_selector", missing_value="programy.clients.client.DefaultBotSelector")

            self._scheduler.load_config_section(configuration_file, section, bot_root)

            self._storage.load_config_section(configuration_file, section, bot_root)

            self._renderer = configuration_file.get_option(section, "renderer")

        else:
            YLogger.warning(self, "No bot name defined for client [%s], defaulting to 'bot'.", self.section_name)
            self._bot_configs[0]._section_name = "bot"
            self._bot_configs[0].load_configuration(configuration_file, bot_root)

    def to_yaml(self, data, defaults=True):

        assert (data is not None)

        if defaults is True:
            data['description'] = 'ProgramY AIML2.0 Client'
            data['bot'] = 'bot'
            data['bot_selector'] = "programy.clients.client.DefaultBotSelector"

            data[self._scheduler.id] = {}
            self._scheduler.to_yaml(data[self._scheduler.id], defaults)


            data['renderer'] = "programy.clients.render.text.TextRenderer"

        else:
            data['description'] = self._description
            data['bot'] = self._bot_configs[0].id
            data['bot_selector'] = self.bot_selector

            data[self._scheduler.id] = {}
            self._scheduler.to_yaml(data[self._scheduler.id], defaults)

            data['renderer'] = self.renderer
