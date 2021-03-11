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
import random
import time


class ServiceCoordinatorConfiguration:

    def __init__(self):
        self._category = None
        self._coordinator = None
        self._services = []

    def from_yaml(self, yaml_data):
        self._category = yaml_data.get('category')
        self._coordinator = yaml_data.get('coordinator')
        self._services = yaml_data.get('services')


class ServiceCoordinator:

    def __init__(self):
        self._services = []

    def add_service(self, service):
        self._services.append(service)

    def execute_query(self, question, srai=False, skip_failures=True):
        raise NotImplementedError()


class SelectableServiceCoordinator(ServiceCoordinator):

    def __init__(self):
        ServiceCoordinator.__init__(self)

    def _get_servicen(self):
        raise NotImplementedError()

    def execute_query(self, question, srai=False, skip_failures=True, try_next_on_failure=False):
        if self._services:
            running = True
            tried = []
            while running is True:
                service = self._get_servicen()
                if service.name not in tried:
                    result = service.execite_query(question, srai)
                    if result:
                        if result['status'] == 'success':
                            return result
                        elif skip_failures is False:
                            return result

                    tried.append(service.name)

                if len(tried) == len(self._services):
                    running = False

        return None


class RandomResultServiceCoordinator(SelectableServiceCoordinator):

    def __init__(self):
        SelectableServiceCoordinator.__init__(self)

    def _get_servicen(self):
        random.seed(time.time())
        servicen = random.randint(0, len(self._services)-1)
        return self._services[servicen]


class RoundRobinResultServiceCoordinator(SelectableServiceCoordinator):

    def __init__(self):
        SelectableServiceCoordinator.__init__(self)
        self._servicen = 0

    def _get_servicen(self):
        if self._servicen >= len(self._services):
            self._servicen = 0

        service = self._services[self._servicen]
        self._servicen += 1
        return service


class AllResultsServiceCoordinator(ServiceCoordinator):

    def __init__(self):
        ServiceCoordinator.__init__(self)

    def execute_query(self, question, srai=False, skip_failures=True):
        if self._services:
            results = []
            for service in self._services:
                result = service.execite_query(question, srai)
                if result:
                    if result['status'] == 'success':
                        results.append(result)
                    elif skip_failures is False:
                        results.append(result)

            return results

        return None
