import json
import os
import unittest.mock

from programy.clients.restful.flask.alexa.client import AlexaBotClient
from programy.clients.restful.flask.alexa.config import AlexaConfiguration
from programy.clients.render.text import TextRenderer
from programytest.clients.arguments import MockArgumentParser


class MockAlexaBotClient(AlexaBotClient):

    def test__init__(self, argument_parser=None):
        AlexaBotClient.__init__(self, argument_parser)

    def _to_json(self, data):
        return data


class MockHttpRequest(object):

    def __init__(self, data):
        self.json = data


class AlexaClientBotClientTests(unittest.TestCase):

    def test_alexa_client_init(self):
        arguments = MockArgumentParser()
        client = MockAlexaBotClient(arguments)
        self.assertIsNotNone(client)

        self.assertIsInstance(client.get_client_configuration(), AlexaConfiguration)
        self.assertEqual('ProgramY AIML2.0 Client', client.get_description())

        self.assertFalse(client._render_callback())
        self.assertIsInstance(client.renderer, TextRenderer)

    def test_load_intent_mappings(self):
        arguments = MockArgumentParser()
        client = MockAlexaBotClient(arguments)
        self.assertIsNotNone(client)

        intents_mapping_file = os.path.dirname(__file__) + os.sep + "intents.maps"
        self.assertTrue(os.path.exists(intents_mapping_file))

        client._load_intent_mappings()
        self.assertIsNotNone(client._intent_mappings)

    def test_client_configuration(self):
        arguments = MockArgumentParser()
        client = MockAlexaBotClient(arguments)
        self.assertIsNotNone(client)
        config = client.get_client_configuration()
        self.assertIsNotNone(config)
        self.assertIsInstance(config, AlexaConfiguration)

    def test_create_response_defaults(self):
        arguments = MockArgumentParser()
        client = MockAlexaBotClient(arguments)
        self.assertIsNotNone(client)

        response = client._create_response("Hello World")
        self.assertIsNotNone(response)

        self.assertTrue('version' in response)
        self.assertEqual("1.0", response['version'])

        self.assertTrue('response' in response)

        self.assertTrue('outputSpeech' in response['response'])
        self.assertTrue('type' in response['response']['outputSpeech'])
        self.assertEqual("PlainText", response['response']['outputSpeech']['type'])
        self.assertTrue('text' in response['response']['outputSpeech'])
        self.assertEqual("Hello World", response['response']['outputSpeech']['text'])
        self.assertTrue('ssml' in response['response']['outputSpeech'])
        self.assertEqual("<speak>Hello World</speak>", response['response']['outputSpeech']['ssml'])
        self.assertTrue('playBehavior' in response['response']['outputSpeech'])
        self.assertEqual("REPLACE_ENQUEUED", response['response']['outputSpeech']['playBehavior'])

        self.assertTrue('shouldEndSession' in response['response'])
        self.assertFalse(response['response']['shouldEndSession'])

    def test_create_response_no_defaults(self):
        arguments = MockArgumentParser()
        client = MockAlexaBotClient(arguments)
        self.assertIsNotNone(client)

        response = client._create_response("Hello World", responsetype="PlainText", playBehavior="REPLACE_ENQUEUED", shouldEndSession=True)
        self.assertIsNotNone(response)

        self.assertTrue('version' in response)
        self.assertEqual("1.0", response['version'])

        self.assertTrue('response' in response)

        self.assertTrue('outputSpeech' in response['response'])
        self.assertTrue('type' in response['response']['outputSpeech'])
        self.assertEqual("PlainText", response['response']['outputSpeech']['type'])
        self.assertTrue('text' in response['response']['outputSpeech'])
        self.assertEqual("Hello World", response['response']['outputSpeech']['text'])
        self.assertTrue('ssml' in response['response']['outputSpeech'])
        self.assertEqual("<speak>Hello World</speak>", response['response']['outputSpeech']['ssml'])
        self.assertTrue('playBehavior' in response['response']['outputSpeech'])
        self.assertEqual("REPLACE_ENQUEUED", response['response']['outputSpeech']['playBehavior'])

        self.assertTrue('shouldEndSession' in response['response'])
        self.assertTrue(response['response']['shouldEndSession'])

    def test_extract_question(self):
        arguments = MockArgumentParser()
        client = MockAlexaBotClient(arguments)
        self.assertIsNotNone(client)

        intent = {'slots': {'text': {'value': 'test question'}}}
        self.assertEqual('test question', client._extract_question(intent))

        intent = {'slots': {'text': {}}}
        self.assertEqual('', client._extract_question(intent))

    def test_add_intent(self):
        arguments = MockArgumentParser()
        client = MockAlexaBotClient(arguments)
        self.assertIsNotNone(client)

        self.assertEqual("nothing", client._add_intent("AskNothing", "nothing"))

        client._intent_mappings["Something"] = "AskSomething"
        self.assertEqual("AskSomething something", client._add_intent("Something", "something"))

    def test_handle_launch_request(self):
        arguments = MockArgumentParser()
        client = MockAlexaBotClient(arguments)
        self.assertIsNotNone(client)

        client_context = client.create_client_context("testid")
        response = client._handle_launch_request(client_context)
        self.assertIsNotNone(response)

    def test_handle_reply_request(self):
        arguments = MockArgumentParser()
        client = MockAlexaBotClient(arguments)
        self.assertIsNotNone(client)

        client_context = client.create_client_context("testid")
        response = client._handle_reply_request(client_context, "hello word")
        self.assertIsNotNone(response)

    def test_handle_leave_request(self):
        arguments = MockArgumentParser()
        client = MockAlexaBotClient(arguments)
        self.assertIsNotNone(client)

        client_context = client.create_client_context("testid")
        response = client._handle_leave_request()
        self.assertIsNotNone(response)

    def test_handle_cancel_request(self):
        arguments = MockArgumentParser()
        client = MockAlexaBotClient(arguments)
        self.assertIsNotNone(client)

        client_context = client.create_client_context("testid")
        response = client._handle_cancel_request(client_context)
        self.assertIsNotNone(response)

    def test_handle_stop_request(self):
        arguments = MockArgumentParser()
        client = MockAlexaBotClient(arguments)
        self.assertIsNotNone(client)

        client_context = client.create_client_context("testid")
        response = client._handle_stop_request(client_context)
        self.assertIsNotNone(response)

    def test_handle_help_request(self):
        arguments = MockArgumentParser()
        client = MockAlexaBotClient(arguments)
        self.assertIsNotNone(client)

        client_context = client.create_client_context("testid")
        response = client._handle_help_request(client_context)
        self.assertIsNotNone(response)

    def test_handle_error(self):
        arguments = MockArgumentParser()
        client = MockAlexaBotClient(arguments)
        self.assertIsNotNone(client)

        client_context = client.create_client_context("testid")
        response = client._handle_error(client_context)
        self.assertIsNotNone(response)

    def test_get_userid(self):
        arguments = MockArgumentParser()
        client = MockAlexaBotClient(arguments)
        self.assertIsNotNone(client)

        request = json.loads(   """
                                {
                                    "version": "1.0",
                                    "session": {
                                        "new": false,
                                        "sessionId": "amzn1.echo-api.session.fe33611a-2bd7-4157-9181-b4fff3017791",
                                        "application": {
                                            "applicationId": "amzn1.ask.skill.93b9463d-3706-4454-830a-aeb0232241d4"
                                        },
                                        "user": {
                                            "userId": "amzn1.ask.account.AGD73QVLBN4YXQ3MNXMQXKHEJIXSXYUF3336QSOVAVOYOLO5V6NR2JML7RJZX5FELAU5I5DWGORWLLRQ4H4V6TKCCHFMMLJJFVYHVF7YO3ROOKGSDCMRZRQ24T7Y6RXSD2UTQMXHIONKCRSX4BZC73EI6R5JPFRTLT3KIXAMBT6RBOAATHIERBJ663GLDR3W5BKU6XSLSTX2N4A"
                                        }
                                    }
                                }
                                """
        )

        self.assertEqual(client._get_userid(request), "amzn1.ask.account.AGD73QVLBN4YXQ3MNXMQXKHEJIXSXYUF3336QSOVAVOYOLO5V6NR2JML7RJZX5FELAU5I5DWGORWLLRQ4H4V6TKCCHFMMLJJFVYHVF7YO3ROOKGSDCMRZRQ24T7Y6RXSD2UTQMXHIONKCRSX4BZC73EI6R5JPFRTLT3KIXAMBT6RBOAATHIERBJ663GLDR3W5BKU6XSLSTX2N4A")

    def test_receive_message(self):
        arguments = MockArgumentParser()
        client = MockAlexaBotClient(arguments)
        self.assertIsNotNone(client)

        request = MockHttpRequest(json.loads("""
        {
            "version": "1.0",
            "session": {
                "new": true,
                "sessionId": "amzn1.echo-api.session.67096ec4-4e1d-454e-a474-72b14f669ebe",
                "application": {
                    "applicationId": "amzn1.ask.skill.93b9463d-3706-4454-830a-aeb0232241d4"
                },
                "user": {
                    "userId": "amzn1.ask.account.AGD73QVLBN4YXQ3MNXMQXKHEJIXSXYUF3336QSOVAVOYOLO5V6NR2JML7RJZX5FELAU5I5DWGORWLLRQ4H4V6TKCCHFMMLJJFVYHVF7YO3ROOKGSDCMRZRQ24T7Y6RXSD2UTQMXHIONKCRSX4BZC73EI6R5JPFRTLT3KIXAMBT6RBOAATHIERBJ663GLDR3W5BKU6XSLSTX2N4A"
                }
            },
            "context": {
                "System": {
                    "application": {
                        "applicationId": "amzn1.ask.skill.93b9463d-3706-4454-830a-aeb0232241d4"
                    },
                    "user": {
                        "userId": "amzn1.ask.account.AGD73QVLBN4YXQ3MNXMQXKHEJIXSXYUF3336QSOVAVOYOLO5V6NR2JML7RJZX5FELAU5I5DWGORWLLRQ4H4V6TKCCHFMMLJJFVYHVF7YO3ROOKGSDCMRZRQ24T7Y6RXSD2UTQMXHIONKCRSX4BZC73EI6R5JPFRTLT3KIXAMBT6RBOAATHIERBJ663GLDR3W5BKU6XSLSTX2N4A"
                    },
                    "device": {
                        "deviceId": "amzn1.ask.device.AGSZB5PHSVBZPBSMJUG3U6BQTHTZE6DW7QPSZ4XMDFIVKW4L7CF2B4EXL464LVS64QJAPLLAJNVMG5MKOLTYDNJY3POVMKNPSQWMXXBCDX3P7B6LDUQB5VA2W4GUEZXJA6URKPOK7SQ5ZA4G7NX24HJTOTFA",
                        "supportedInterfaces": {}
                    },
                    "apiEndpoint": "https://api.eu.amazonalexa.com",
                    "apiAccessToken": "eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsImtpZCI6IjEifQ.eyJhdWQiOiJodHRwczovL2FwaS5hbWF6b25hbGV4YS5jb20iLCJpc3MiOiJBbGV4YVNraWxsS2l0Iiwic3ViIjoiYW16bjEuYXNrLnNraWxsLjkzYjk0NjNkLTM3MDYtNDQ1NC04MzBhLWFlYjAyMzIyNDFkNCIsImV4cCI6MTU0ODk2NjQ1MSwiaWF0IjoxNTQ4OTY2MTUxLCJuYmYiOjE1NDg5NjYxNTEsInByaXZhdGVDbGFpbXMiOnsiY29uc2VudFRva2VuIjpudWxsLCJkZXZpY2VJZCI6ImFtem4xLmFzay5kZXZpY2UuQUdTWkI1UEhTVkJaUEJTTUpVRzNVNkJRVEhUWkU2RFc3UVBTWjRYTURGSVZLVzRMN0NGMkI0RVhMNDY0TFZTNjRRSkFQTExBSk5WTUc1TUtPTFRZRE5KWTNQT1ZNS05QU1FXTVhYQkNEWDNQN0I2TERVUUI1VkEyVzRHVUVaWEpBNlVSS1BPSzdTUTVaQTRHN05YMjRISlRPVEZBIiwidXNlcklkIjoiYW16bjEuYXNrLmFjY291bnQuQUdENzNRVkxCTjRZWFEzTU5YTVFYS0hFSklYU1hZVUYzMzM2UVNPVkFWT1lPTE81VjZOUjJKTUw3UkpaWDVGRUxBVTVJNURXR09SV0xMUlE0SDRWNlRLQ0NIRk1NTEpKRlZZSFZGN1lPM1JPT0tHU0RDTVJaUlEyNFQ3WTZSWFNEMlVUUU1YSElPTktDUlNYNEJaQzczRUk2UjVKUEZSVExUM0tJWEFNQlQ2UkJPQUFUSElFUkJKNjYzR0xEUjNXNUJLVTZYU0xTVFgyTjRBIn19.lDHtmtodBxLvR_EI7GnJeiSX4iNOSZv1RWYCSIoXnvfqbUPfPMefxLmFzD6HXmwFPrC2UG4gpyQoubtaLisNUXQFQzwn1LGsN9z-OIBd_G9egYhroG8JRzm857bMXAqZ-BRZMtM7m7EQmOf2iFyoD5ME1vNFIyujdb0rk21dDhD2-5iE2vIIvWxb5zTJV1b6Ln2v_fMOMZlO9AzgnRs2sVsp3ZkiFxUMzORbJCrEKD8EhDOAVl6ZKWEyfZ19P4NxeFdR352xzI-Rx8eAVbhlKTc8su69rVBwsLV0G_7wSNhHGU0bzBNixFtH4ov6RAtYMP6uEq4hD_lTYolNb915Ng"
                },
                "Viewport": {
                    "experiences": [
                        {
                            "arcMinuteWidth": 246,
                            "arcMinuteHeight": 144,
                            "canRotate": false,
                            "canResize": false
                        }
                    ],
                    "shape": "RECTANGLE",
                    "pixelWidth": 1024,
                    "pixelHeight": 600,
                    "dpi": 160,
                    "currentPixelWidth": 1024,
                    "currentPixelHeight": 600,
                    "touch": [
                        "SINGLE"
                    ]
                }
            },
            "request": {
                "type": "LaunchRequest",
                "requestId": "amzn1.echo-api.request.47858421-cc45-47b7-9df0-41a1d6591065",
                "timestamp": "2019-01-31T20:22:31Z",
                "locale": "en-GB",
                "shouldLinkResultBeReturned": false
            }
        }"""))

        client.receive_message(request)
