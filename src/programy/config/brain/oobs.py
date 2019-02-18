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
from programy.config.brain.oob import BrainOOBConfiguration
from programy.utils.substitutions.substitues import Substitutions


class BrainOOBSConfiguration(BaseSectionConfigurationData):
    def __init__(self):
        BaseSectionConfigurationData.__init__(self, "oob")
        self._default = None
        self._oobs = {}

    def exists(self, name):
        if name == 'default':
            return bool(self._default is not None)
        return bool(name in self._oobs)

    def default(self):
        return self._default

    def oob(self, name):
        if name in self._oobs:
            return self._oobs[name]
        return None

    def oobs(self):
        return self._oobs.keys()

    def check_for_license_keys(self, license_keys):
        BaseSectionConfigurationData.check_for_license_keys(self, license_keys)

    def load_config_section(self, configuration_file, configuration, bot_root, subs: Substitutions = None):
        oobs = configuration_file.get_section("oob", configuration)
        if oobs is not None:
            oob_keys = configuration_file.get_keys(oobs)

            for name in oob_keys:
                oob = BrainOOBConfiguration(name)
                oob.load_config_section(configuration_file, oobs, bot_root, subs=subs)
                if name == 'default':
                    self._default = oob
                else:
                    self._oobs[name] = oob

        else:
            YLogger.warning(self, "Config section [oobs] missing from Brain, no oobs loaded")

    def to_yaml(self, data, defaults=True):
        if defaults is True:
            data['default'] = {'classname': 'programy.oob.defaults.default.DefaultOutOfBandProcessor'}
            data['alarm'] = {'classname': 'programy.oob.defaults.alarm.AlarmOutOfBandProcessor'}
            data['camera'] = {'classname': 'programy.oob.defaults.camera.CameraOutOfBandProcessor'}
            data['clear'] = {'classname': 'programy.oob.defaults.clear.ClearOutOfBandProcessor'}
            data['dial'] = {'classname': 'programy.oob.defaults.dial.DialOutOfBandProcessor'}
            data['dialog'] = {'classname': 'programy.oob.defaults.dialog.DialogOutOfBandProcessor'}
            data['email'] = {'classname': 'programy.oob.defaults.email.EmailOutOfBandProcessor'}
            data['geomap'] = {'classname': 'programy.oob.defaults.map.MapOutOfBandProcessor'}
            data['schedule'] = {'classname': 'programy.oob.defaults.schedule.ScheduleOutOfBandProcessor'}
            data['search'] = {'classname': 'programy.oob.defaults.search.SearchOutOfBandProcessor'}
            data['sms'] = {'classname': 'programy.oob.defaults.sms.SMSOutOfBandProcessor'}
            data['url'] = {'classname': 'programy.oob.defaults.url.URLOutOfBandProcessor'}
            data['wifi'] = {'classname': 'programy.oob.defaults.wifi.WifiOutOfBandProcessor'}
        else:
            if self._default is not None:
                self.config_to_yaml(data, self._default, defaults)
            for oob in self._oobs:
                self.config_to_yaml(data, oob, defaults)
