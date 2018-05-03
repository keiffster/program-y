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

from programy.config.section import BaseSectionConfigurationData


class BrainNodesConfiguration(BaseSectionConfigurationData):

    def __init__(self):
        BaseSectionConfigurationData.__init__(self, "nodes")
        self._pattern_nodes = None
        self._template_nodes = None

    @property
    def pattern_nodes(self):
        return self._pattern_nodes

    @property
    def template_nodes(self):
        return self._template_nodes

    def load_config_section(self, configuration_file, configuration, bot_root):
        nodes = configuration_file.get_section("nodes", configuration)
        if nodes is not None:
            pattern_nodes = configuration_file.get_option(nodes, "pattern_nodes", missing_value=None)
            if pattern_nodes is not None:
                self._pattern_nodes = self.sub_bot_root(pattern_nodes, bot_root)
            template_nodes = configuration_file.get_option(nodes, "template_nodes", missing_value=None)
            if template_nodes is not None:
                self._template_nodes = self.sub_bot_root(template_nodes, bot_root)
        else:
            YLogger.warning(self, "'nodes' section missing from bot config, using to defaults")

    def to_yaml(self, data, defaults=True):
        if defaults is True:
            data['pattern_nodes'] = "./config/pattern_nodes.conf"
            data['template_nodes'] = "./config/template_nodes.conf"
        else:
            data['pattern_nodes'] = self._pattern_nodes
            data['template_nodes'] = self._template_nodes
