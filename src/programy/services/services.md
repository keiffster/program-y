# Program-y Service

## Types of Service
j6iu
* Library
* Rest 

## Service Class
```Python
class Service:

    DEFAULT_RESPONSE = "Service failed to return valid response"

    def __init__(self, configuration):
        self._configuration = configuration

    @property
    def configuration(self):
        return self._configuration

    @property
    def category(self) -> str:
        return self.configuration.category

    @property
    def name(self) -> str:
        return self.configuration.name

    def patterns(self) -> list:
        return []

    def initialise(self, client):
        pass

    def _match(self, question: str):

    def execute_query(self, question, aiml=False):

    def _get_bot_response(self, client_context, sentence):
        return client_context.bot.ask_question(client_context, sentence)        # pragma: no cover

    def _get_default_response(self, client_context):
        :
        :

    def ask_question(self, client_context, question):
        :
        :

    def get_default_aiml_file(self):
        return None

    def load_default_aiml(self, parser):
        :
        :
```

## Service Query Class
```python
class ServiceQuery(ABC):

    def __init__(self, service):
        self._service = service

    def parse_matched(self, matched):
        pass

    @abstractmethod
    def execute(self):
        raise NotImplementedError

    def aiml_response(self, response):
        YLogger.debug(self, response)
        return response

    @staticmethod
    def _get_matched_var(matched, index, name, optional=False):
        try:
            value = matched[index]

            if value is 'NONE':
                return None
            return value.strip()

        except:
            if optional is False:
                raise ValueError("query variable [%s] missing" % name)

        return None
```

## Service Exception Class
```python
class ServiceException(Exception):

    def __init__(self, msg: str):
        Exception.__init__(self, msg)
```
## Service Configuration

### Base Configuration
```yaml
service:
  type: library
  name: metoffice
  category: weather
  service_class: programy.services.library.metoffice.service.MetOfficeService
  success_prefix: METOFFICE RESULT
  default_response: METOFFICE SERVICE ERROR
  default_srai: METOFFICE SERVICE ERROR
  default_aiml: metoffice.aiml
  load_default_aiml: True
```

### REST Configuration
```yaml
service:
  type: rest
  name: duckduckgo
  category: search
  service_class: programy.services.rest.duckduckgo.service.DuckDuckGoService
  success_prefix: DUCKDUCKGO RESULT
  default_response: DUCKDUCKGO SERVICE ERROR
  rest:
    timeout: 1000
    retries: 100, 500, 1000, 2000, 5000, 10000
```