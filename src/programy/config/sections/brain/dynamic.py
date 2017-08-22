"""
Copyright (c) 2016-17 Keith Sterling http://www.keithsterling.com

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated
documentation files (the "Software"), to deal in the Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software,
and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO
THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""

import logging

from programy.config.base import BaseConfigurationData
from programy.utils.classes.loader import ClassLoader

class BrainDynamicsConfiguration(BaseConfigurationData):

    def __init__(self):
        BaseConfigurationData.__init__(self, "dynamic")
        self._dynamic_sets      = {}
        self._dynamic_maps      = {}
        self._dynamic_vars      = {}

    @property
    def dynamic_sets(self):
        return self._dynamic_sets

    def add_dynamic_set(self, name, classname, config_file):
        self._dynamic_sets[name.upper()] = (ClassLoader.instantiate_class(classname))(config_file)

    @property
    def dynamic_maps(self):
        return self._dynamic_maps

    def add_dynamic_map(self, name, classname, config_file):
        self._dynamic_maps[name.upper()] = (ClassLoader.instantiate_class(classname))(config_file)

    @property
    def dynamic_vars(self):
        return self._dynamic_vars

    def add_dynamic_var(self, name, classname, config_file):
        self._dynamic_vars[name.upper()] = (ClassLoader.instantiate_class(classname))(config_file)

    def load_config_section(self, config_file, brain_config, bot_root):
        dynamic_config = config_file.get_section("dynamic", brain_config)
        if dynamic_config is not None:
            self.load_dynamic_sets(config_file, dynamic_config)
            self.load_dynamic_maps(config_file, dynamic_config)
            self.load_dynamic_vars(config_file, dynamic_config)
        else:
            if logging.getLogger().isEnabledFor(logging.ERROR): logging.error("Config section [dynamic] missing from Brain, using defaults")
        self.check_default_sets(config_file)

    def load_dynamic_sets(self, config_file, dynamic_config):
        sets_config = config_file.get_option(dynamic_config, "sets")
        if sets_config is not None:
            for set in sets_config.keys():
                dyn_set = sets_config[set]
                self._dynamic_sets[set.upper()] = (ClassLoader.instantiate_class(dyn_set))(config_file)

    def check_default_sets(self, config_file):
        if 'NUMBER' not in self._dynamic_sets:
            if logging.getLogger().isEnabledFor(logging.WARNING): logging.warning("Dynamic set NUMBER not defined, adding default implementation")
            self._dynamic_sets['NUMBER'] = (ClassLoader.instantiate_class("programy.dynamic.sets.numeric.IsNumeric"))(config_file)

    def is_dynamic_set(self, name):
        return bool(name.upper() in self._dynamic_sets)

    def dynamic_set(self, bot, clientid, name, value):
        name = name.upper()
        if name in self._dynamic_sets:
            dynamic_set = self._dynamic_sets[name]
            return dynamic_set.is_member(bot, clientid, value)
        else:
            return None

    def is_dynamic_map(self, name):
        return bool(name.upper() in self._dynamic_maps)

    def load_dynamic_maps(self, config_file, dynamic_config):
        maps_config = config_file.get_option(dynamic_config, "maps")
        if maps_config is not None:
            for map in maps_config.keys():
                dyn_map = maps_config[map]
                self._dynamic_maps[map.upper()] = (ClassLoader.instantiate_class(dyn_map))(config_file)

    def dynamic_map(self, bot, clientid, name, value):
        name = name.upper()
        if name in self._dynamic_maps:
            dynamic_map = self._dynamic_maps[name]
            return dynamic_map.map_value(bot, clientid, value)
        else:
            return None

    def is_dynamic_var(self, name):
        return bool(name.upper() in self._dynamic_vars)

    def load_dynamic_vars(self, config_file, dynamic_config):
        vars_config = config_file.get_option(dynamic_config, "variables")
        if vars_config is not None:
            for var in vars_config.keys():
                dyn_var = vars_config[var]
                self._dynamic_vars[var.upper()] = (ClassLoader.instantiate_class(dyn_var))(config_file)

    def dynamic_var(self, bot, clientid, name, value=None):
        name = name.upper()
        if name in self._dynamic_vars:
            dynamic_var = self._dynamic_vars[name]
            return dynamic_var.get_value(bot, clientid, value)
        else:
            return None



