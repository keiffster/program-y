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

from programy.utils.classes.loader import ClassLoader
from programy.dynamic.sets.numeric import IsNumeric
from programy.dynamic.maps.plural import PluralMap
from programy.dynamic.maps.singular import SingularMap
from programy.dynamic.maps.predecessor import PredecessorMap
from programy.dynamic.maps.successor import SuccessorMap


class DynamicsCollection(object):

    def __init__(self):
        self._dynamic_sets = {}
        self._dynamic_maps = {}
        self._dynamic_vars = {}

    def load_from_configuration(self, dynamics_configuration):

        if dynamics_configuration is not None:

            for set_name in dynamics_configuration.dynamic_sets:
                self.add_dynamic_set(set_name, dynamics_configuration.dynamic_sets[set_name], dynamics_configuration)

            for map_name in dynamics_configuration.dynamic_maps:
                self.add_dynamic_map(map_name, dynamics_configuration.dynamic_maps[map_name], dynamics_configuration)

            for var_name in dynamics_configuration.dynamic_vars:
                self.add_dynamic_var(var_name, dynamics_configuration.dynamic_vars[var_name], dynamics_configuration)

            self.load_default_dynamics(dynamics_configuration)

    def load_default_dynamics(self, dynamics_configuration):
        self.load_default_dynamic_sets(dynamics_configuration)
        self.load_default_dynamic_maps(dynamics_configuration)
        self.load_default_dynamic_vars(dynamics_configuration)

    def load_default_dynamic_sets(self, dynamics_configuration):
        if IsNumeric.NAME not in self._dynamic_sets:
            YLogger.warning(self, "Dynamic set %s not defined, adding default implementation", IsNumeric.NAME)
            self._dynamic_sets[IsNumeric.NAME] = IsNumeric(dynamics_configuration)

    def load_default_dynamic_maps(self, dynamics_configuration):
        if PluralMap.NAME not in self._dynamic_maps:
            YLogger.warning(self, "Dynamic set %s not defined, adding default implementation", PluralMap.NAME)
            self._dynamic_maps[PluralMap.NAME] = PluralMap(dynamics_configuration)

        if SingularMap.NAME not in self._dynamic_maps:
            YLogger.warning(self, "Dynamic set %s not defined, adding default implementation", SingularMap.NAME)
            self._dynamic_maps[SingularMap.NAME] = SingularMap(dynamics_configuration)

        if SuccessorMap.NAME not in self._dynamic_maps:
            YLogger.warning(self, "Dynamic set %s not defined, adding default implementation", SuccessorMap.NAME)
            self._dynamic_maps[SuccessorMap.NAME] = SuccessorMap(dynamics_configuration)

        if PredecessorMap.NAME not in self._dynamic_maps:
            YLogger.warning(self, "Dynamic set %s not defined, adding default implementation", PredecessorMap.NAME)
            self._dynamic_maps[PredecessorMap.NAME] = PredecessorMap(dynamics_configuration)

    def load_default_dynamic_vars(self, dynamics_configuration):
        return

    ###################################################################################################
    # Dynamic Sets

    @property
    def dynamic_sets(self):
        return self._dynamic_sets

    def add_dynamic_set(self, name, classname, config_file):
        self._dynamic_sets[name.upper()] = (ClassLoader.instantiate_class(classname))(config_file)

    def is_dynamic_set(self, name):
        return bool(name.upper() in self._dynamic_sets)

    def dynamic_set(self, client_context, name, value):
        name = name.upper()
        if name in self._dynamic_sets:
            dynamic_set = self._dynamic_sets[name]
            return dynamic_set.is_member(client_context, value)
        return None

    ###################################################################################################
    # Dynamic Maps

    @property
    def dynamic_maps(self):
        return self._dynamic_maps

    def add_dynamic_map(self, name, classname, config_file):
        self._dynamic_maps[name.upper()] = (ClassLoader.instantiate_class(classname))(config_file)

    def is_dynamic_map(self, name):
        return bool(name.upper() in self._dynamic_maps)

    def dynamic_map(self, client_context, name, value):
        name = name.upper()
        if name in self._dynamic_maps:
            dynamic_map = self._dynamic_maps[name]
            return dynamic_map.map_value(client_context, value)
        return None

    ###################################################################################################
    # Dynamic Vars

    @property
    def dynamic_vars(self):
        return self._dynamic_vars

    def add_dynamic_var(self, name, classname, config_file):
        self._dynamic_vars[name.upper()] = (ClassLoader.instantiate_class(classname))(config_file)

    def is_dynamic_var(self, name):
        return bool(name.upper() in self._dynamic_vars)

    def dynamic_var(self, client_context, name, value=None):
        name = name.upper()
        if name in self._dynamic_vars:
            dynamic_var = self._dynamic_vars[name]
            return dynamic_var.get_value(client_context, value)
        return None

    def set_dynamic_var(self, client_context, name, value):
        try:
            name = name.upper()
            if name in self._dynamic_vars:
                dynamic_var = self._dynamic_vars[name]
                dynamic_var.set_value(client_context, value)
        except Exception as e:
            YLogger.exception(self, "Unable to set value for dynamic var %s", e, name)
