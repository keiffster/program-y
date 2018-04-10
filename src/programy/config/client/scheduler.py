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

from programy.config.base import BaseConfigurationData
from programy.config.bot.bot import BotConfiguration


class SchedulerConfiguration(BaseConfigurationData):

    def __init__(self):
        BaseConfigurationData.__init__(self, name="scheduler")
        self._name = None
        self._debug_level = 0
        self._add_listeners = False
        self._remove_all_jobs = False
        self._blocking = False

    @property
    def name(self):
        return self._name

    @property
    def debug_level(self):
        return self._debug_level

    @property
    def add_listeners(self):
        return self._add_listeners

    @property
    def remove_all_jobs(self):
        return self._remove_all_jobs

    @property
    def blocking(self):
        return self._blocking

    def load_config_section(self, configuration_file, configuration, bot_root):
        scheduler = configuration_file.get_section(self._section_name, configuration)
        if scheduler is not None:
            self._name = configuration_file.get_option(scheduler, "name", missing_value=None)
            self._debug_level = configuration_file.get_int_option(scheduler, "debug_level", missing_value=0)
            self._add_listeners = configuration_file.get_bool_option(scheduler, "add_listeners", missing_value=False)
            self._remove_all_jobs = configuration_file.get_bool_option(scheduler, "remove_all_jobs", missing_value=False)

        else:
            YLogger.warning(self, "'scheduler' section missing from client config, using to defaults")



