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

from programy.triggers.config import TriggerConfiguration
from programy.context import ClientContext
from programy.triggers.manager import TriggerManager
from programy.storage.factory import StorageFactory
from programy.utils.classes.loader import ClassLoader


class LocalTriggerManager(TriggerManager):

    def __init__(self, config: TriggerConfiguration):
        TriggerManager.__init__(self, config)
        self._triggers = {}

    @property
    def triggers(self):
        return self._triggers

    def empty(self):
        for event in self._triggers.keys():
            self._triggers[event].clear()


    def get_triggers(self, event: str) -> list:
        if event in self._triggers:
            return self._triggers[event]
        return []

    def has_trigger_event(self, event: str) -> bool:
        return bool(event in self._triggers)

    def add_triggers(self, triggers):
        for event, trigger in triggers.values():
            self.add_trigger(event, trigger)

    def add_trigger(self, event: str, classname: str):
        try:
            trigger = ClassLoader.instantiate_class(classname)()
            if event not in self._triggers:
                self._triggers[event] = []
            self._triggers[event].append(trigger)

        except Exception as e:
            YLogger.exception(self, "Failed to add trigger [%s] -> [%s]", e, event, classname)

    def load_triggers(self, storage_factory: StorageFactory):

        assert isinstance(storage_factory, StorageFactory)

        YLogger.debug(self, "Loading Triggers")
        if storage_factory.entity_storage_engine_available(StorageFactory.TRIGGERS) is True:
            trigger_engine = storage_factory.entity_storage_engine(StorageFactory.TRIGGERS)
            if trigger_engine:
                try:
                    triggers_store = trigger_engine.triggers_store()
                    triggers_store.load_all(self)

                except Exception as e:
                    YLogger.exception(self, "Failed to load triggers from storage", e)

    def trigger(self, event: str, client_context: ClientContext = None, additional: {} = None) -> bool:

        if client_context is not None:
            assert isinstance(client_context, ClientContext)

        YLogger.debug(client_context, "Event triggered [%s]", event)

        if event in self._triggers:

            if additional is None:
                additional = {}
            if "event" not in additional:
                additional["event"] = event

            trigger_list = self._triggers[event]
            for trigger in trigger_list:
                try:
                    YLogger.debug(client_context, "Firing trigger for event [%s]", event)
                    trigger.trigger(client_context=client_context, additional=additional)
                    return True

                except Exception as exec:
                    YLogger.exception(client_context, "Trigger %s failed to fire", exec, event)

        return False
