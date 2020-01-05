"""
Copyright (c) 2016-2020 Keith Sterling http://www.keithsterling.com

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated
documentation files (the "Software"), to deal in the Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software,
and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions
of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO
THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""
import threading
import datetime
import requests
from flask import Flask, jsonify, request

from programy.utils.logging.ylogger import YLogger
from programy.clients.ping.config import PingResponderConfig
from programy.utils.console.console import outputLog


class PingResponder():

    def __init__(self, client):
        self._start_time = datetime.datetime.now()
        self._config = client.configuration.client_configuration.responder
        self._client = client

    @property
    def config(self):
        return self._config

    def ping(self):

        payload = {"start_time": "%s" % self._start_time,
                   "client": self._client.id,
                   "questions": self._client.num_questions
                   }
        payload['bots'] = self._client.get_question_counts()
        payload['logging'] = YLogger.snapshot().to_json()

        return payload

    @staticmethod
    def ping_service(ping_app: Flask, config: PingResponderConfig):

        if config.ssl_cert_file is not None and \
                config.ssl_key_file is not None:
            context = (config.ssl_cert_file,
                       config.ssl_key_file)

            outputLog(None, "Healthcheck running in https mode")
            ping_app.run(host=config.host,
                         port=config.port,
                         debug=config.debug,
                         ssl_context=context)
        else:
            outputLog(None, "Healthcheck running in http mode, careful now !")
            ping_app.run(host=config.host,
                         port=config.port,
                         debug=config.debug)

    def start_ping_service(self, ping_app: Flask):
        t = threading.Thread(target=PingResponder.ping_service, args=(ping_app, self.config))
        t.daemon = False
        t.start()
        return t

    def stop_ping_service(self):
        func = request.environ.get('werkzeug.server.shutdown')
        if func is None:
            raise RuntimeError('Not running with the Werkzeug Server')
        func()

    def shutdown_ping_service(self):

        self.unregister_with_healthchecker()

        try:
            url = "http://%s:%d%s" % (self.config.host, self.config.port, self.config.shutdown)
            requests.get(url)

        except Exception:
            YLogger.error(None, "Failed to shutdown ping service")

    def register_with_healthchecker(self):

        if self.config.register is not None:
            if self.config.host is not None:
                host = self.config.host

            else:
                host = self._client.configuration.client_configuration.host

            if self.config.host is not None:
                port = self.config.port

            else:
                port = self._client.configuration.client_configuration.port

            try:
                url = "%s?name=%s&host=%s&port=%s&url=%s" % (self.config.register, self._client.id,
                                                             host, port, self.config.url)
                requests.get(url)

            except Exception as e:
                YLogger.exception(None, "Unable to register with healthchecker", e)

    def unregister_with_healthchecker(self):

        if self.config.unregister is not None:
            try:
                url = "%s?name=%s" % (self.config.unregister, self._client.id)
                requests.get(url)
            except Exception as e:
                outputLog(self, e)
                YLogger.error(None, "Unable to unregister with healthchecker")

    @staticmethod
    def init_ping_response(ping_responder):

        if ping_responder.config.host is None:
            YLogger.info(None, "No REST configuration for ping responder")
            outputLog(None, "Healthcheck now running as part of REST Service...")
            return

        outputLog(None, "Healthcheck now running as separate REST Service...")

        ping_app = Flask(ping_responder.config.name)

        if ping_responder.config.url is not None:
            @ping_app.route(ping_responder.config.url, methods=['GET'])
            def ping():  # pylint: disable=unused-variable
                return jsonify(ping_responder.ping())

        if ping_responder.config.shutdown is not None:
            @ping_app.route(ping_responder.config.shutdown, methods=['GET'])
            def shutdown():  # pylint: disable=unused-variable
                ping_responder.stop_ping_service()
                return 'Server shutting down...'

        ping_responder.start_ping_service(ping_app)
