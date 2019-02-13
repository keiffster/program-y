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
from programy.config.container import BaseContainerConfigurationData
from programy.config.brain.overrides import BrainOverridesConfiguration
from programy.config.brain.defaults import BrainDefaultsConfiguration
from programy.config.brain.binaries import BrainBinariesConfiguration
from programy.config.brain.braintree import BrainBraintreeConfiguration
from programy.config.brain.services import BrainServicesConfiguration
from programy.config.brain.securities import BrainSecuritiesConfiguration
from programy.config.brain.oobs import BrainOOBSConfiguration
from programy.config.brain.dynamic import BrainDynamicsConfiguration
from programy.config.brain.tokenizer import BrainTokenizerConfiguration
from programy.config.brain.debugfiles import BrainDebugFilesConfiguration
from programy.utils.substitutions.substitues import Substitutions


class BrainConfiguration(BaseContainerConfigurationData):

    def __init__(self, section_name="brain"):
        self._overrides = BrainOverridesConfiguration()
        self._defaults = BrainDefaultsConfiguration()
        self._binaries = BrainBinariesConfiguration()
        self._braintree = BrainBraintreeConfiguration()
        self._services = BrainServicesConfiguration()
        self._security = BrainSecuritiesConfiguration()
        self._oob = BrainOOBSConfiguration()
        self._dynamics = BrainDynamicsConfiguration()
        self._tokenizer = BrainTokenizerConfiguration()
        self._debugfiles = BrainDebugFilesConfiguration()
        BaseContainerConfigurationData.__init__(self, section_name)

    @property
    def overrides(self):
        return self._overrides

    @property
    def defaults(self):
        return self._defaults

    @property
    def binaries(self):
        return self._binaries

    @property
    def braintree(self):
        return self._braintree

    @property
    def services(self):
        return self._services

    @property
    def security(self):
        return self._security

    @property
    def oob(self):
        return self._oob

    @property
    def dynamics(self):
        return self._dynamics

    @property
    def tokenizer(self):
        return self._tokenizer

    @property
    def debugfiles(self):
        return self._debugfiles

    def check_for_license_keys(self, license_keys):
        self._overrides.check_for_license_keys(license_keys)
        self._defaults.check_for_license_keys(license_keys)
        self._binaries.check_for_license_keys(license_keys)
        self._braintree.check_for_license_keys(license_keys)
        self._services.check_for_license_keys(license_keys)
        self._security.check_for_license_keys(license_keys)
        self._oob.check_for_license_keys(license_keys)
        self._dynamics.check_for_license_keys(license_keys)
        self._tokenizer.check_for_license_keys(license_keys)
        self._debugfiles.check_for_license_keys(license_keys)
        BaseContainerConfigurationData.check_for_license_keys(self, license_keys)

    def load_configuration(self, configuration_file, bot_root, subs: Substitutions = None):
        brain_config = configuration_file.get_section(self.section_name)
        if brain_config is not None:
            self._overrides.load_config_section(configuration_file, brain_config, bot_root, subs=subs)
            self._defaults.load_config_section(configuration_file, brain_config, bot_root, subs=subs)
            self._binaries.load_config_section(configuration_file, brain_config, bot_root, subs=subs)
            self._braintree.load_config_section(configuration_file, brain_config, bot_root, subs=subs)
            self._services.load_config_section(configuration_file, brain_config, bot_root, subs=subs)
            self._security.load_config_section(configuration_file, brain_config, bot_root, subs=subs)
            self._oob.load_config_section(configuration_file, brain_config, bot_root, subs=subs)
            self._dynamics.load_config_section(configuration_file, brain_config, bot_root, subs=subs)
            self._tokenizer.load_config_section(configuration_file, brain_config, bot_root, subs=subs)
            self._debugfiles.load_config_section(configuration_file, brain_config, bot_root, subs=subs)

    def to_yaml(self, data, defaults=True):
        self.config_to_yaml(data, BrainOverridesConfiguration(), defaults)
        self.config_to_yaml(data, BrainDefaultsConfiguration(), defaults)
        self.config_to_yaml(data, BrainBinariesConfiguration(), defaults)
        self.config_to_yaml(data, BrainBraintreeConfiguration(), defaults)
        self.config_to_yaml(data, BrainServicesConfiguration(), defaults)
        self.config_to_yaml(data, BrainSecuritiesConfiguration(), defaults)
        self.config_to_yaml(data, BrainOOBSConfiguration(), defaults)
        self.config_to_yaml(data, BrainDynamicsConfiguration(), defaults)
        self.config_to_yaml(data, BrainTokenizerConfiguration(), defaults)
        self.config_to_yaml(data, BrainDebugFilesConfiguration(), defaults)
