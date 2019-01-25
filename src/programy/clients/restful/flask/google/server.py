
from flask import Flask, request, jsonify

APP = Flask(__name__)


@APP.route('/', methods=['GET', 'POST'])
def ask():

    print(request.json)
    print(request.json['queryResult'])

    return jsonify({"fulfillmentText": "Hello from servusai"})

APP.run()
