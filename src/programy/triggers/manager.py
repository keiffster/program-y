"""
Copyright (c) 2016-2020 Keith Sterling http://www.keithsterling.com

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
from typing import Dict
from abc import ABC
from abc import abstractmethod
from programy.utils.logging.ylogger import YLogger
from programy.triggers.config import TriggerConfiguration
from programy.context import ClientContext
from programy.utils.classes.loader import ClassLoader


class TriggerManager(ABC):

    def __init__(self, config: TriggerConfiguration):

        assert isinstance(config, TriggerConfiguration)

        self._config = config

    @abstractmethod
    def trigger(self, event: str, client_context: ClientContext = None, additional: Dict[str, str] = None) -> bool:
        raise NotImplementedError()  # pragma: no cover

    @staticmethod
    def load_trigger_manager(config: TriggerConfiguration):
        if config.manager is not None:
            try:
                return ClassLoader.instantiate_class(config.manager)(config)

            except Exception as e:
                YLogger.exception(None, "Failed to load trigger manager [%s]", e, config.manager)

        else:
            YLogger.error(None, "No Trigger Manager defined in configuration")

        return None
