import uuid
import datetime

from programy.utils.logging.ylogger import YLogger

from flask import Flask
from flask import jsonify
from flask import request
from flask import make_response
from flask import abort
from flask import current_app

from programy.clients.restful.flask.client import FlaskRestBotClient
from programy.clients.restful.flask.webchat.config import WebChatConfiguration
from programy.clients.render.html import HtmlRenderer


class WebChatBotClient(FlaskRestBotClient):

    def __init__(self, argument_parser=None):
        FlaskRestBotClient.__init__(self, "WebChat", argument_parser)
        # Enter you API keys, here, alternatively store in a db or file and load at startup
        # This is an exmaple, and therefore not suitable for production
        self._api_keys = [
        ]

    def get_client_configuration(self):
        return WebChatConfiguration()

    def get_default_renderer(self):
        return HtmlRenderer()

    def is_apikey_valid(self, apikey):
        return bool(apikey in self._api_keys)

    def get_api_key(self, request):
        if 'api_key' in request.args:
            return request.args['api_key']
        return None

    def unauthorised_access_response(self, error_code=401):
        return make_response(jsonify({'error': 'Unauthorized access'}), error_code)

    def check_api_key(self, request):
        if self.configuration.client_configuration.use_api_keys is True:
            api_key = self.get_api_key(request)
            if api_key is None:
                YLogger.error(self, "Unauthorised access - api required but missing")
                return self.unauthorised_access_response()

            if self.is_apikey_valid(api_key) is False:
                YLogger.error(self, "'Unauthorised access - invalid api key")
                return self.unauthorised_access_response()

        return None

    def get_question(self, request):
        if 'question' in request.args:
            return request.args['question']
        return None

    def get_userid(self, request):
        userid = request.cookies.get(self.configuration.client_configuration.cookie_id)
        if userid is None:
            userid = str(uuid.uuid4().hex)
            YLogger.debug(self, "Setting userid cookie to :%s" % userid)
        else:
            YLogger.debug(self, "Found userid cookie : %s" % userid)
        return userid

    def get_userid_cookie_expirary_date(self, duration):
        expire_date = datetime.datetime.now()
        expire_date = expire_date + datetime.timedelta(days=duration)
        return expire_date

    def create_success_response_data(self, question, answer):
        return {"question": question, "answer": answer}

    def get_default_response(self, client_context):
        return client_context.bot.default_response

    def create_error_response_data(self, client_context, question, error):
        return {"question": question,
                "answer": self.get_default_response(client_context),
                "error": error
                }

    def create_response(self, response_data, userid, userid_expire_date):
        response = jsonify({'response': response_data})
        response.set_cookie(self.configuration.client_configuration.cookie_id, userid, expires=userid_expire_date)
        return response

    def get_answer(self, client_context, question):
        if question == 'YINITIALQUESTION':
            answer = client_context.bot.get_initial_question(client_context)
        else:
            self._questions += 1
            answer = client_context.bot.ask_question(client_context, question, responselogger=self)
        return answer

    def receive_message(self, request):

        api_key_response = self.check_api_key(request)
        if api_key_response is not None:
            return api_key_response

        question = self.get_question(request)
        if question is None:
            YLogger.error(self, "'question' missing from request")
            abort(400)

        userid = self.get_userid(request)

        userid_expire_date = self.get_userid_cookie_expirary_date(self.configuration.client_configuration.cookie_expires)

        client_context = self.create_client_context(userid)
        try:
            answer = self.get_answer(client_context, question)
            rendered = self._renderer.render(client_context, answer)
            response_data = self.create_success_response_data(question, rendered)

        except Exception as excep:
            YLogger.exception(self, "Failed receving message", excep)
            response_data = self.create_error_response_data(client_context, question, str(excep))

        return self.create_response(response_data, userid, userid_expire_date)


if __name__ == '__main__':

    print("Initiating WebChat Client...")

    APP = Flask(__name__)

    WEB_CLIENT = WebChatBotClient()

    @APP.route('/')
    def index():
        return current_app.send_static_file('webchat.html')

    @APP.route(WEB_CLIENT.configuration.client_configuration.api, methods=['GET'])
    def receive_message():
        try:
            return WEB_CLIENT.receive_message(request)
        except Exception as e:
            print("Error receiving webchat message", e)
            YLogger.exception(None, "Web client error", e)
            return "500"

    @APP.route(WEB_CLIENT.ping_responder.config.url, methods=['GET'])
    def ping():
        return jsonify(WEB_CLIENT.ping_responder.ping())

    @APP.route(WEB_CLIENT.ping_responder.config.shutdown, methods=['GET'])
    def shutdown():
        WEB_CLIENT.ping_responder.stop_ping_service()
        return 'Server shutting down...'

    WEB_CLIENT.run(APP)
