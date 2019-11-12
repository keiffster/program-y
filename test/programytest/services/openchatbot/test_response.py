import unittest

from programy.services.openchatbot.response import OpenChatBotMedia
from programy.services.openchatbot.response import OpenChatBotMediaButton
from programy.services.openchatbot.response import OpenChatBotMediaDefaultAction
from programy.services.openchatbot.response import OpenChatBotMeta
from programy.services.openchatbot.response import OpenChatBotResponse
from programy.services.openchatbot.response import OpenChatBotStatus
from programy.services.openchatbot.response import OpenChatBotSuggestion
from programy.services.openchatbot.response import OpenChatBotTTS
from programy.services.openchatbot.response import OpenchatBotReponseObject


class OpenchatBotReponseObjectTests(unittest.TestCase):

    def test_get_parameter(self):

        data = {"key1": "value1"}
        object = OpenchatBotReponseObject.get_parameter(data, "key1")
        self.assertEqual("value1", object)

        object = OpenchatBotReponseObject.get_parameter(data, "key2")
        self.assertIsNone(object)

        object = OpenchatBotReponseObject.get_parameter(data, "key1", defaultValue="value2")
        self.assertEqual("value1", object)

        object = OpenchatBotReponseObject.get_parameter(data, "key2", defaultValue="value2")
        self.assertEqual("value2", object)


class OpenChatBotMediaDefaultActionTests(unittest.TestCase):

    def test_parse(self):
        data = {
                    "type": "web_url",
                    "label":"Go",
                    "payload": "https://www.ikea.com/fr/fr/catalog/products/70392542/"
                }
        object = OpenChatBotMediaDefaultAction.parse(data)
        self.assertIsNotNone(object)

    def test_to_aiml(self):
        data = {
            "type": "web_url",
            "label": "Go",
            "payload": "https://www.ikea.com/fr/fr/catalog/products/70392542/"
        }
        object = OpenChatBotMediaDefaultAction.parse(data)
        self.assertIsNotNone(object)

        text = object.to_aiml()
        self.assertIsNotNone(text)
        self.assertEqual("<link><text>Go</text><url>https://www.ikea.com/fr/fr/catalog/products/70392542/</url></link>", text)


class OpenChatBotMediaButtonTests(unittest.TestCase):

    def test_parse(self):
        data = {
                    "type":"custom",
                    "client": "specific_custom_client_name",
                    "label": "Ajouter au panier",
                    "payload": "DEVELOPER_DEFINED_PAYLOAD"
                }
        object = OpenChatBotMediaButton.parse(data)
        self.assertIsNotNone(object)

        self.assertEqual(object.actiontype, "custom",)
        self.assertEqual(object.client, "specific_custom_client_name")
        self.assertEqual(object.label, "Ajouter au panier")
        self.assertEqual(object.payload, "DEVELOPER_DEFINED_PAYLOAD")

    def test_to_aiml(self):
        data = {
            "type": "web_url",
            "label": "Acheter en ligne",
            "payload": "https://serv-api.target2sell.com/1.1/R/cookie/OFCBMN5RRHSG5L/1200/OFCBMN5RRHSG5L-1200-5/20343224/1/viewTogether-%7BtypeOfContextList%3A%5B%22current%22%2C%22view%22%5D%7D/f082e51f-561d-47f7-c0cb-13735e58bfc1"
        }
        object = OpenChatBotMediaButton.parse(data)
        self.assertIsNotNone(object)

        text = object.to_aiml()
        self.assertIsNotNone(text)
        self.assertEqual("<button><text>Acheter en ligne</text><url>https://serv-api.target2sell.com/1.1/R/cookie/OFCBMN5RRHSG5L/1200/OFCBMN5RRHSG5L-1200-5/20343224/1/viewTogether-%7BtypeOfContextList%3A%5B%22current%22%2C%22view%22%5D%7D/f082e51f-561d-47f7-c0cb-13735e58bfc1</url></button>", text)


class OpenChatBotTTSTests(unittest.TestCase):

    def test_parse(self):
        data =  {
            "type": "plainText",
            "payload": "Je vous envoie plus d\'information sur le Strandmon de chez Ikea"
        }
        object = OpenChatBotTTS.parse(data)
        self.assertIsNotNone(object)

        self.assertEqual(object.actiontype, "plainText")
        self.assertEqual(object.payload, "Je vous envoie plus d\'information sur le Strandmon de chez Ikea")

    def test_to_aiml(self):
        data =  {
            "type": "plainText",
            "payload": "Je vous envoie plus d\'information sur le Strandmon de chez Ikea"
        }
        object = OpenChatBotTTS.parse(data)
        self.assertIsNotNone(object)

        text = object.to_aiml()
        self.assertIsNotNone(text)
        self.assertEqual("<tts><type>plainText</type>Je vous envoie plus d'information sur le Strandmon de chez Ikea</tts>", text)


class OpenChatBotSuggestionTests(unittest.TestCase):

    def test_parse(self):
        data = {
                "type": "web_url",
                "label": "Les magasins Ikea",
                "payload": "https://www.ikea.com/ms/fr_FR/ikny_splash.html"
            }
        object = OpenChatBotSuggestion.parse(data)
        self.assertIsNotNone(object)

        self.assertEqual(object.actiontype, "web_url")
        self.assertEqual(object.label, "Les magasins Ikea")
        self.assertEqual(object.payload, "https://www.ikea.com/ms/fr_FR/ikny_splash.html")

    def test_to_aiml(self):
        data = {
            "type": "web_url",
            "label": "Go",
            "payload": "https://www.ikea.com/fr/fr/catalog/products/70392542/"
        }
        object = OpenChatBotSuggestion.parse(data)
        self.assertIsNotNone(object)

        text = object.to_aiml()
        self.assertIsNotNone(text)
        self.assertEqual("<link><text>Go</text><url>https://www.ikea.com/fr/fr/catalog/products/70392542/</url></link>", text)


class OpenChatBotMediaTests(unittest.TestCase):

    def test_parse(self):
        data = {
                "shortDesc": "Fauteuil enfant, Vissle gris",
                "longDesc": "Quand ils peuvent imiter les adultes, les enfants se sentent spéciaux et importants. C\'est pourquoi nous avons créé une version miniature du fauteuil STRANDMON, l\'un de nos produits favoris.",
                "title": "STRANDMON",
                "mimeType": "image/jpeg",
                "src": "https://www.ikea.com/fr/fr/images/products/strandmon-fauteuil-enfant-gris__0574584_PE668407_S4.JPG",
                "default_action": {
                    "type": "web_url",
                    "label":"Go",
                    "payload": "https://www.ikea.com/fr/fr/catalog/products/70392542/"
                },
                "buttons":[
                    {
                        "type":"web_url",
                        "label":"Acheter en ligne",
                        "payload":"https://serv-api.target2sell.com/1.1/R/cookie/OFCBMN5RRHSG5L/1200/OFCBMN5RRHSG5L-1200-5/20343224/1/viewTogether-%7BtypeOfContextList%3A%5B%22current%22%2C%22view%22%5D%7D/f082e51f-561d-47f7-c0cb-13735e58bfc1"
                    },
                    {
                        "type":"natural_language",
                        "label":"Tous les fauteuils",
                        "payload":"Je veux voir tous les fauteuils du magazin Ikea le plus proche"
                    },
                    {
                        "type":"custom",
                        "client": "specific_custom_client_name",
                        "label":"Ajouter au panier",
                        "payload":"DEVELOPER_DEFINED_PAYLOAD"
                    }
                ]
            }

        object = OpenChatBotMedia.parse(data)
        self.assertIsNotNone(object)

        self.assertEqual(object.shortDesc,  "Fauteuil enfant, Vissle gris")
        self.assertEqual(object.longDesc,  "Quand ils peuvent imiter les adultes, les enfants se sentent spéciaux et importants. C\'est pourquoi nous avons créé une version miniature du fauteuil STRANDMON, l\'un de nos produits favoris.")
        self.assertEqual(object.title,  "STRANDMON")
        self.assertEqual(object.mimeType,  "image/jpeg")
        self.assertEqual(object.src,  "https://www.ikea.com/fr/fr/images/products/strandmon-fauteuil-enfant-gris__0574584_PE668407_S4.JPG")

        self.assertIsNotNone(object.default_action)
        self.assertEqual(object.default_action.actiontype, "web_url")
        self.assertEqual(object.default_action.label, "Go")
        self.assertEqual(object.default_action.payload, "https://www.ikea.com/fr/fr/catalog/products/70392542/")

        self.assertIsNotNone(object.buttons)
        self.assertEqual(3, len(object.buttons))

        self.assertEqual(object.buttons[0].actiontype, "web_url")
        self.assertEqual(object.buttons[0].client, None)
        self.assertEqual(object.buttons[0].label, "Acheter en ligne")
        self.assertEqual(object.buttons[0].payload, "https://serv-api.target2sell.com/1.1/R/cookie/OFCBMN5RRHSG5L/1200/OFCBMN5RRHSG5L-1200-5/20343224/1/viewTogether-%7BtypeOfContextList%3A%5B%22current%22%2C%22view%22%5D%7D/f082e51f-561d-47f7-c0cb-13735e58bfc1")

        self.assertEqual(object.buttons[1].actiontype, "natural_language")
        self.assertEqual(object.buttons[1].client, None)
        self.assertEqual(object.buttons[1].label, "Tous les fauteuils")
        self.assertEqual(object.buttons[1].payload, "Je veux voir tous les fauteuils du magazin Ikea le plus proche")

        self.assertEqual(object.buttons[2].actiontype, "custom")
        self.assertEqual(object.buttons[2].client, "specific_custom_client_name")
        self.assertEqual(object.buttons[2].label, "Ajouter au panier")
        self.assertEqual(object.buttons[2].payload, "DEVELOPER_DEFINED_PAYLOAD")

    def test_to_aiml(self):
        data = {
            "shortDesc": "Fauteuil enfant, Vissle gris",
            "longDesc": "Quand ils peuvent imiter les adultes, les enfants se sentent spéciaux et importants. C\'est pourquoi nous avons créé une version miniature du fauteuil STRANDMON, l\'un de nos produits favoris.",
            "title": "STRANDMON",
            "mimeType": "image/jpeg",
            "src": "https://www.ikea.com/fr/fr/images/products/strandmon-fauteuil-enfant-gris__0574584_PE668407_S4.JPG",
            "default_action": {
                "type": "web_url",
                "label": "Go",
                "payload": "https://www.ikea.com/fr/fr/catalog/products/70392542/"
            },
            "buttons": [
                {
                    "type": "web_url",
                    "label": "Acheter en ligne",
                    "payload": "https://serv-api.target2sell.com/1.1/R/cookie/OFCBMN5RRHSG5L/1200/OFCBMN5RRHSG5L-1200-5/20343224/1/viewTogether-%7BtypeOfContextList%3A%5B%22current%22%2C%22view%22%5D%7D/f082e51f-561d-47f7-c0cb-13735e58bfc1"
                },
                {
                    "type": "natural_language",
                    "label": "Tous les fauteuils",
                    "payload": "Je veux voir tous les fauteuils du magazin Ikea le plus proche"
                },
                {
                    "type": "custom",
                    "client": "specific_custom_client_name",
                    "label": "Ajouter au panier",
                    "payload": "DEVELOPER_DEFINED_PAYLOAD"
                }
            ]
        }

        object = OpenChatBotMedia.parse(data)
        self.assertIsNotNone(object)

        text = object.to_aiml()
        self.assertIsNotNone(text)
        self.assertEqual("<card><image>https://www.ikea.com/fr/fr/images/products/strandmon-fauteuil-enfant-gris__0574584_PE668407_S4.JPG</image><title>Fauteuil enfant, Vissle gris</title><subtitle>Quand ils peuvent imiter les adultes, les enfants se sentent spéciaux et importants. C'est pourquoi nous avons créé une version miniature du fauteuil STRANDMON, l'un de nos produits favoris.</subtitle><button><text>Acheter en ligne</text><url>https://serv-api.target2sell.com/1.1/R/cookie/OFCBMN5RRHSG5L/1200/OFCBMN5RRHSG5L-1200-5/20343224/1/viewTogether-%7BtypeOfContextList%3A%5B%22current%22%2C%22view%22%5D%7D/f082e51f-561d-47f7-c0cb-13735e58bfc1</url></button></card>", text)


class OpenChatBotResponseTests(unittest.TestCase):

    def test_parse(self):
        data = {
            "query": "je cherche la doc du fauteuil strandmon Ikea",
            "userId": "1234567890",
            "timestamp": 1485358532524,
            "text": "Voilà !",
            "tts": {
                "type": "plainText",
                "payload": "Je vous envoie plus d\'information sur le Strandmon de chez Ikea"
            },
            "infoURL": "https://www.ikea.com/fr/fr/catalog/products/70392542/",
            "media": [
                {
                    "shortDesc": "Fauteuil enfant, Vissle gris",
                    "longDesc": "Quand ils peuvent imiter les adultes, les enfants se sentent spéciaux et importants. C\'est pourquoi nous avons créé une version miniature du fauteuil STRANDMON, l\'un de nos produits favoris.",
                    "title": "STRANDMON",
                    "mimeType": "image/jpeg",
                    "src": "https://www.ikea.com/fr/fr/images/products/strandmon-fauteuil-enfant-gris__0574584_PE668407_S4.JPG",
                    "default_action": {
                        "type": "web_url",
                        "label":"Go",
                        "payload": "https://www.ikea.com/fr/fr/catalog/products/70392542/"
                    },
                    "buttons":[
                        {
                            "type":"web_url",
                            "label":"Acheter en ligne",
                            "payload":"https://serv-api.target2sell.com/1.1/R/cookie/OFCBMN5RRHSG5L/1200/OFCBMN5RRHSG5L-1200-5/20343224/1/viewTogether-%7BtypeOfContextList%3A%5B%22current%22%2C%22view%22%5D%7D/f082e51f-561d-47f7-c0cb-13735e58bfc1"
                        },
                        {
                            "type":"natural_language",
                            "label":"Tous les fauteuils",
                            "payload":"Je veux voir tous les fauteuils du magazin Ikea le plus proche"
                        },
                        {
                            "type":"custom",
                            "client": "specific_custom_client_name",
                            "label":"Ajouter au panier",
                            "payload":"DEVELOPER_DEFINED_PAYLOAD"
                        }
                    ]
                }
            ],
            "suggestions": [
                {
                    "type": "web_url",
                    "label": "Les magasins Ikea",
                    "payload": "https://www.ikea.com/ms/fr_FR/ikny_splash.html"
                },
                {
                    "type": "natural_language",
                    "label": "Politique de confidentialité",
                    "payload": "Je voudrais voir la politique de confidentialité de la société Ikea en France"
                }
            ],
            "context": []
        }
        object = OpenChatBotResponse.parse(data)
        self.assertIsNotNone(object)

        self.assertEqual(object.query, "je cherche la doc du fauteuil strandmon Ikea")
        self.assertEqual(object.userId, "1234567890")
        self.assertEqual(object.timestamp, 1485358532524)
        self.assertEqual(object.text, "Voilà !")
        self.assertEqual(object.infoURL, "https://www.ikea.com/fr/fr/catalog/products/70392542/")

        self.assertIsNotNone(object.tts)
        self.assertEqual(object.tts.actiontype, "plainText")
        self.assertEqual(object.tts.payload, "Je vous envoie plus d\'information sur le Strandmon de chez Ikea")

        self.assertIsNotNone(object.media)
        self.assertEqual(1, len(object.media))

        self.assertEqual(object.media[0].shortDesc,  "Fauteuil enfant, Vissle gris")
        self.assertEqual(object.media[0].longDesc,  "Quand ils peuvent imiter les adultes, les enfants se sentent spéciaux et importants. C\'est pourquoi nous avons créé une version miniature du fauteuil STRANDMON, l\'un de nos produits favoris.")
        self.assertEqual(object.media[0].title,  "STRANDMON")
        self.assertEqual(object.media[0].mimeType,  "image/jpeg")
        self.assertEqual(object.media[0].src,  "https://www.ikea.com/fr/fr/images/products/strandmon-fauteuil-enfant-gris__0574584_PE668407_S4.JPG")

        self.assertIsNotNone(object.media[0].default_action)
        self.assertEqual(object.media[0].default_action.actiontype, "web_url")
        self.assertEqual(object.media[0].default_action.label, "Go")
        self.assertEqual(object.media[0].default_action.payload, "https://www.ikea.com/fr/fr/catalog/products/70392542/")

        self.assertIsNotNone(object.media[0].buttons)
        self.assertEqual(3, len(object.media[0].buttons))

        self.assertEqual(object.media[0].buttons[0].actiontype, "web_url")
        self.assertEqual(object.media[0].buttons[0].client, None)
        self.assertEqual(object.media[0].buttons[0].label, "Acheter en ligne")
        self.assertEqual(object.media[0].buttons[0].payload, "https://serv-api.target2sell.com/1.1/R/cookie/OFCBMN5RRHSG5L/1200/OFCBMN5RRHSG5L-1200-5/20343224/1/viewTogether-%7BtypeOfContextList%3A%5B%22current%22%2C%22view%22%5D%7D/f082e51f-561d-47f7-c0cb-13735e58bfc1")

        self.assertEqual(object.media[0].buttons[1].actiontype, "natural_language")
        self.assertEqual(object.media[0].buttons[1].client, None)
        self.assertEqual(object.media[0].buttons[1].label, "Tous les fauteuils")
        self.assertEqual(object.media[0].buttons[1].payload, "Je veux voir tous les fauteuils du magazin Ikea le plus proche")

        self.assertEqual(object.media[0].buttons[2].actiontype, "custom")
        self.assertEqual(object.media[0].buttons[2].client, "specific_custom_client_name")
        self.assertEqual(object.media[0].buttons[2].label, "Ajouter au panier")
        self.assertEqual(object.media[0].buttons[2].payload, "DEVELOPER_DEFINED_PAYLOAD")

        self.assertIsNotNone(object.suggestions)
        self.assertEqual(2, len(object.suggestions))
        self.assertEqual(object.suggestions[0].actiontype, "web_url")
        self.assertEqual(object.suggestions[0].label, "Les magasins Ikea")
        self.assertEqual(object.suggestions[0].payload, "https://www.ikea.com/ms/fr_FR/ikny_splash.html")
        self.assertEqual(object.suggestions[1].actiontype, "natural_language")
        self.assertEqual(object.suggestions[1].label, "Politique de confidentialité")
        self.assertEqual(object.suggestions[1].payload, "Je voudrais voir la politique de confidentialité de la société Ikea en France")

        self.assertIsNotNone(object.context)
        self.assertEqual(object.context, [])

    def test_to_aiml(self):
        data = {
            "query": "je cherche la doc du fauteuil strandmon Ikea",
            "userId": "1234567890",
            "timestamp": 1485358532524,
            "text": "Voilà !",
            "tts": {
                "type": "plainText",
                "payload": "Je vous envoie plus d\'information sur le Strandmon de chez Ikea"
            },
            "infoURL": "https://www.ikea.com/fr/fr/catalog/products/70392542/",
            "media": [
                {
                    "shortDesc": "Fauteuil enfant, Vissle gris",
                    "longDesc": "Quand ils peuvent imiter les adultes, les enfants se sentent spéciaux et importants. C\'est pourquoi nous avons créé une version miniature du fauteuil STRANDMON, l\'un de nos produits favoris.",
                    "title": "STRANDMON",
                    "mimeType": "image/jpeg",
                    "src": "https://www.ikea.com/fr/fr/images/products/strandmon-fauteuil-enfant-gris__0574584_PE668407_S4.JPG",
                    "default_action": {
                        "type": "web_url",
                        "label": "Go",
                        "payload": "https://www.ikea.com/fr/fr/catalog/products/70392542/"
                    },
                    "buttons": [
                        {
                            "type": "web_url",
                            "label": "Acheter en ligne",
                            "payload": "https://serv-api.target2sell.com/1.1/R/cookie/OFCBMN5RRHSG5L/1200/OFCBMN5RRHSG5L-1200-5/20343224/1/viewTogether-%7BtypeOfContextList%3A%5B%22current%22%2C%22view%22%5D%7D/f082e51f-561d-47f7-c0cb-13735e58bfc1"
                        },
                        {
                            "type": "natural_language",
                            "label": "Tous les fauteuils",
                            "payload": "Je veux voir tous les fauteuils du magazin Ikea le plus proche"
                        },
                        {
                            "type": "custom",
                            "client": "specific_custom_client_name",
                            "label": "Ajouter au panier",
                            "payload": "DEVELOPER_DEFINED_PAYLOAD"
                        }
                    ]
                }
            ],
            "suggestions": [
                {
                    "type": "web_url",
                    "label": "Les magasins Ikea",
                    "payload": "https://www.ikea.com/ms/fr_FR/ikny_splash.html"
                },
                {
                    "type": "natural_language",
                    "label": "Politique de confidentialité",
                    "payload": "Je voudrais voir la politique de confidentialité de la société Ikea en France"
                }
            ],
            "context": []
        }
        object = OpenChatBotResponse.parse(data)
        self.assertIsNotNone(object)

        text = object.to_aiml()
        self.assertIsNotNone(text)
        self.assertEqual("Voilà ! <tts><type>plainText</type>Je vous envoie plus d'information sur le Strandmon de "
                         "chez Ikea</tts> <card><image>https://www.ikea.com/fr/fr/images/products/strandmon-"
                         "fauteuil-enfant-gris__0574584_PE668407_S4.JPG</image><title>Fauteuil enfant, Vissle "
                         "gris</title><subtitle>Quand ils peuvent imiter les adultes, les enfants se sentent "
                         "spéciaux et importants. C'est pourquoi nous avons créé une version miniature du fauteuil"
                         " STRANDMON, l'un de nos produits favoris.</subtitle><button><text>Acheter en ligne</text>"
                         "<url>https://serv-api.target2sell.com/1.1/R/cookie/OFCBMN5RRHSG5L/1200/OFCBMN5RRHSG5L-1200"
                         "-5/20343224/1/viewTogether-%7BtypeOfContextList%3A%5B%22current%22%2C%22view%22%5D%7D/"
                         "f082e51f-561d-47f7-c0cb-13735e58bfc1</url></button></card> <link><text>Les magasins "
                         "Ikea</text><url>https://www.ikea.com/ms/fr_FR/ikny_splash.html</url></link>", text)


class OpenChatBotStatusTests(unittest.TestCase):

    def test_parse(self):
        data = {
            "code": 200,
            "message": "success"
        }
        object = OpenChatBotStatus.parse(data)
        self.assertIsNotNone(object)

        self.assertEqual(object.code, 200)
        self.assertEqual(object.message, 'success')


class OpenChatBotMetaTests(unittest.TestCase):

    def test_parse(self):
        data = {
            "botName": "Ikea",
            "botIcon": "https://is4-ssl.mzstatic.com/image/thumb/Purple118/v4/4a/23/cb/4a23cb34-1039-af8d-32f0-c3e3bf313da3/source/256x256bb.jpg",
            "version": "0.1",
            "copyright": "Copyright 2018 Ikea.",
            "authors": [
                "Jane Doe",
                "John Doe"
            ]
        }
        object = OpenChatBotMeta.parse(data)
        self.assertIsNotNone(object)

        self.assertEqual(object.botName, "Ikea")
        self.assertEqual(object.botIcon, "https://is4-ssl.mzstatic.com/image/thumb/Purple118/v4/4a/23/cb/4a23cb34-1039-af8d-32f0-c3e3bf313da3/source/256x256bb.jpg")
        self.assertEqual(object.version, "0.1")
        self.assertEqual(object.copyr, "Copyright 2018 Ikea.")
        self.assertEqual(object.authors, ["Jane Doe","John Doe"] )
