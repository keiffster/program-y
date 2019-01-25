



from flask import Flask, request, jsonify

APP = Flask(__name__)


@APP.route('/', methods=['GET', 'POST'])
def ask():

    request_type = request.json['request']['type']
    print(request_type)

    if request_type == 'LaunchRequest':

        return jsonify({
            "version": "string",
            "response": {
                "outputSpeech": {
                    "type": "PlainText",
                    "text": "Welcome to Servus AI, please ask me a question",
                    "ssml": "<speak>Welcome to Servus AI, please ask a question</speak>",
                    "playBehavior": "REPLACE_ENQUEUED"
                },
                "shouldEndSession": False
            }
        }
        )

    elif request_type == 'IntentRequest':

        print(request.json['request']['intent'])

        intent = request.json['request']['intent']
        intent_name = intent['name']

        shouldEndSession = False
        if intent_name == 'AskWho':
            response = "You asked a who question"
        elif intent_name == 'LeaveServusai':
            response = "So long and thanks for the fish!"
            shouldEndSession = True
        else:
            response = "You asked another type of question"
        ssml_response = "<speak>%s</speak>"%response

        return jsonify({
            "version": "string",
            "response": {
                "outputSpeech": {
                    "type": "PlainText",
                    "text": response,
                    "ssml": ssml_response,
                    "playBehavior": "REPLACE_ENQUEUED"
                },
                "shouldEndSession": shouldEndSession
            }
        }
        )

    elif request_type == 'SessionEndedRequest':

        return jsonify({
            "version": "string",
            "response": {
                "outputSpeech": {
                    "type": "PlainText",
                    "text": "So long and thanks for the fish!",
                    "ssml": "<speak>So long and thanks for the fish!</speak>",
                    "playBehavior": "REPLACE_ENQUEUED"
                },
                "shouldEndSession": True
            }
        }
        )

    else:

        return jsonify({
            "version": "string",
            "response": {
                "outputSpeech": {
                    "type": "PlainText",
                    "text": "Oopsie there was an error!",
                    "ssml": "<speak>Oopsie there was an error!</speak>",
                    "playBehavior": "REPLACE_ENQUEUED"
                },
                "shouldEndSession": True
            }
        }
        )


APP.run()
