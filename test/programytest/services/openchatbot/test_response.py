import unittest

from programy.services.openchatbot.response import OpenchatBotReponseObject
from programy.services.openchatbot.response import OpenChatBotMediaDefaultAction
from programy.services.openchatbot.response import OpenChatBotMediaButton
from programy.services.openchatbot.response import OpenChatBotMedia
from programy.services.openchatbot.response import OpenChatBotTTS
from programy.services.openchatbot.response import OpenChatBotSuggestion
from programy.services.openchatbot.response import OpenChatBotResponse
from programy.services.openchatbot.response import OpenChatBotStatus
from programy.services.openchatbot.response import OpenChatBotMeta


class OpenchatBotReponseObjectTests(unittest.TestCase):

    def test_get_parameter(self):

        data = {"key1": "value1"}
        object = OpenchatBotReponseObject.get_parameter(data, "key1")
        self.assertEquals("value1", object)

        object = OpenchatBotReponseObject.get_parameter(data, "key2")
        self.assertIsNone(object)

        object = OpenchatBotReponseObject.get_parameter(data, "key1", defaultValue="value2")
        self.assertEquals("value1", object)

        object = OpenchatBotReponseObject.get_parameter(data, "key2", defaultValue="value2")
        self.assertEquals("value2", object)


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

        self.assertEquals(object.type, "custom",)
        self.assertEquals(object.client, "specific_custom_client_name")
        self.assertEquals(object.label, "Ajouter au panier")
        self.assertEquals(object.payload, "DEVELOPER_DEFINED_PAYLOAD")

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

        self.assertEquals(object.type, "plainText")
        self.assertEquals(object.payload, "Je vous envoie plus d\'information sur le Strandmon de chez Ikea")

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

        self.assertEquals(object.type, "web_url")
        self.assertEquals(object.label, "Les magasins Ikea")
        self.assertEquals(object.payload, "https://www.ikea.com/ms/fr_FR/ikny_splash.html")

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

        self.assertEquals(object.shortDesc,  "Fauteuil enfant, Vissle gris")
        self.assertEquals(object.longDesc,  "Quand ils peuvent imiter les adultes, les enfants se sentent spéciaux et importants. C\'est pourquoi nous avons créé une version miniature du fauteuil STRANDMON, l\'un de nos produits favoris.")
        self.assertEquals(object.title,  "STRANDMON")
        self.assertEquals(object.mimeType,  "image/jpeg")
        self.assertEquals(object.src,  "https://www.ikea.com/fr/fr/images/products/strandmon-fauteuil-enfant-gris__0574584_PE668407_S4.JPG")

        self.assertIsNotNone(object.default_action)
        self.assertEquals(object.default_action.type, "web_url")
        self.assertEquals(object.default_action.label, "Go")
        self.assertEquals(object.default_action.payload, "https://www.ikea.com/fr/fr/catalog/products/70392542/")

        self.assertIsNotNone(object.buttons)
        self.assertEquals(3, len(object.buttons))

        self.assertEquals(object.buttons[0].type, "web_url")
        self.assertEquals(object.buttons[0].client, None)
        self.assertEquals(object.buttons[0].label, "Acheter en ligne")
        self.assertEquals(object.buttons[0].payload, "https://serv-api.target2sell.com/1.1/R/cookie/OFCBMN5RRHSG5L/1200/OFCBMN5RRHSG5L-1200-5/20343224/1/viewTogether-%7BtypeOfContextList%3A%5B%22current%22%2C%22view%22%5D%7D/f082e51f-561d-47f7-c0cb-13735e58bfc1")

        self.assertEquals(object.buttons[1].type, "natural_language")
        self.assertEquals(object.buttons[1].client, None)
        self.assertEquals(object.buttons[1].label, "Tous les fauteuils")
        self.assertEquals(object.buttons[1].payload, "Je veux voir tous les fauteuils du magazin Ikea le plus proche")

        self.assertEquals(object.buttons[2].type, "custom")
        self.assertEquals(object.buttons[2].client, "specific_custom_client_name")
        self.assertEquals(object.buttons[2].label, "Ajouter au panier")
        self.assertEquals(object.buttons[2].payload, "DEVELOPER_DEFINED_PAYLOAD")

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

        self.assertEquals(object.query, "je cherche la doc du fauteuil strandmon Ikea")
        self.assertEquals(object.userId, "1234567890")
        self.assertEquals(object.timestamp, 1485358532524)
        self.assertEquals(object.text, "Voilà !")
        self.assertEquals(object.infoURL, "https://www.ikea.com/fr/fr/catalog/products/70392542/")

        self.assertIsNotNone(object.tts)
        self.assertEquals(object.tts.type, "plainText")
        self.assertEquals(object.tts.payload, "Je vous envoie plus d\'information sur le Strandmon de chez Ikea")

        self.assertIsNotNone(object.media)
        self.assertEquals(1, len(object.media))

        self.assertEquals(object.media[0].shortDesc,  "Fauteuil enfant, Vissle gris")
        self.assertEquals(object.media[0].longDesc,  "Quand ils peuvent imiter les adultes, les enfants se sentent spéciaux et importants. C\'est pourquoi nous avons créé une version miniature du fauteuil STRANDMON, l\'un de nos produits favoris.")
        self.assertEquals(object.media[0].title,  "STRANDMON")
        self.assertEquals(object.media[0].mimeType,  "image/jpeg")
        self.assertEquals(object.media[0].src,  "https://www.ikea.com/fr/fr/images/products/strandmon-fauteuil-enfant-gris__0574584_PE668407_S4.JPG")

        self.assertIsNotNone(object.media[0].default_action)
        self.assertEquals(object.media[0].default_action.type, "web_url")
        self.assertEquals(object.media[0].default_action.label, "Go")
        self.assertEquals(object.media[0].default_action.payload, "https://www.ikea.com/fr/fr/catalog/products/70392542/")

        self.assertIsNotNone(object.media[0].buttons)
        self.assertEquals(3, len(object.media[0].buttons))

        self.assertEquals(object.media[0].buttons[0].type, "web_url")
        self.assertEquals(object.media[0].buttons[0].client, None)
        self.assertEquals(object.media[0].buttons[0].label, "Acheter en ligne")
        self.assertEquals(object.media[0].buttons[0].payload, "https://serv-api.target2sell.com/1.1/R/cookie/OFCBMN5RRHSG5L/1200/OFCBMN5RRHSG5L-1200-5/20343224/1/viewTogether-%7BtypeOfContextList%3A%5B%22current%22%2C%22view%22%5D%7D/f082e51f-561d-47f7-c0cb-13735e58bfc1")

        self.assertEquals(object.media[0].buttons[1].type, "natural_language")
        self.assertEquals(object.media[0].buttons[1].client, None)
        self.assertEquals(object.media[0].buttons[1].label, "Tous les fauteuils")
        self.assertEquals(object.media[0].buttons[1].payload, "Je veux voir tous les fauteuils du magazin Ikea le plus proche")

        self.assertEquals(object.media[0].buttons[2].type, "custom")
        self.assertEquals(object.media[0].buttons[2].client, "specific_custom_client_name")
        self.assertEquals(object.media[0].buttons[2].label, "Ajouter au panier")
        self.assertEquals(object.media[0].buttons[2].payload, "DEVELOPER_DEFINED_PAYLOAD")

        self.assertIsNotNone(object.suggestions)
        self.assertEquals(2, len(object.suggestions))
        self.assertEquals(object.suggestions[0].type, "web_url")
        self.assertEquals(object.suggestions[0].label, "Les magasins Ikea")
        self.assertEquals(object.suggestions[0].payload, "https://www.ikea.com/ms/fr_FR/ikny_splash.html")
        self.assertEquals(object.suggestions[1].type, "natural_language")
        self.assertEquals(object.suggestions[1].label, "Politique de confidentialité")
        self.assertEquals(object.suggestions[1].payload, "Je voudrais voir la politique de confidentialité de la société Ikea en France")

        self.assertIsNotNone(object.context)
        self.assertEquals(object.context, [])

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
        self.assertEquals("Voilà ! <tts><type>plainText</type>Je vous envoie plus d'information sur le Strandmon de "
                          "chez Ikea</tts> <card><image>https://www.ikea.com/fr/fr/images/products/strandmon-fauteuil-"
                          "enfant-gris__0574584_PE668407_S4.JPG</image><title>Fauteuil enfant, Vissle gris</title>"
                          "<subtitle>Quand ils peuvent imiter les adultes, les enfants se sentent spéciaux et importants. "
                          "C'est pourquoi nous avons créé une version miniature du fauteuil STRANDMON, l'un de nos produits "
                          "favoris.</subtitle><button><text>Acheter en ligne</text><url>https://serv-api.target2sell.com/1.1/R/"
                          "cookie/OFCBMN5RRHSG5L/1200/OFCBMN5RRHSG5L-1200-5/20343224/1/viewTogether-%7BtypeOfContextList%3A%5B%22c"
                          "urrent%22%2C%22view%22%5D%7D/f082e51f-561d-47f7-c0cb-13735e58bfc1</url></button></card> <card>"
                          "<image>https://www.ikea.com/fr/fr/images/products/strandmon-fauteuil-enfant-gris__0574584_PE668407_S4.JPG"
                          "</image><title>Fauteuil enfant, Vissle gris</title><subtitle>Quand ils peuvent imiter les adultes, les "
                          "enfants se sentent spéciaux et importants. C'est pourquoi nous avons créé une version miniature du "
                          "fauteuil STRANDMON, l'un de nos produits favoris.</subtitle><button><text>Acheter en ligne</text>"
                          "<url>https://serv-api.target2sell.com/1.1/R/cookie/OFCBMN5RRHSG5L/1200/OFCBMN5RRHSG5L-1200-5/20343224/1/"
                          "viewTogether-%7BtypeOfContextList%3A%5B%22current%22%2C%22view%22%5D%7D/f082e51f-561d-47f7-c0cb-13735e58bfc1"
                          "</url></button></card>", text)


class OpenChatBotStatusTests(unittest.TestCase):

    def test_parse(self):
        data = {
            "code": 200,
            "message": "success"
        }
        object = OpenChatBotStatus.parse(data)
        self.assertIsNotNone(object)

        self.assertEquals(object.code, 200)
        self.assertEquals(object.message, 'success')


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

        self.assertEquals(object.botName, "Ikea")
        self.assertEquals(object.botIcon, "https://is4-ssl.mzstatic.com/image/thumb/Purple118/v4/4a/23/cb/4a23cb34-1039-af8d-32f0-c3e3bf313da3/source/256x256bb.jpg")
        self.assertEquals(object.version, "0.1")
        self.assertEquals(object.copyright, "Copyright 2018 Ikea.")
        self.assertEquals(object.authors, ["Jane Doe","John Doe"] )
