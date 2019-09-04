import unittest

from programy.services.openchatbot.parser import OpenChatBotResponseParser


class OpenChatBotResponseParserTests(unittest.TestCase):

    def test_parser(self):
        parser = OpenChatBotResponseParser()

        text = """
            {
                "response": {
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
                },
                "status": {
                    "code": 200,
                    "message": "success"
                },
                "meta": {
                    "botName": "Ikea",
                    "botIcon": "https://is4-ssl.mzstatic.com/image/thumb/Purple118/v4/4a/23/cb/4a23cb34-1039-af8d-32f0-c3e3bf313da3/source/256x256bb.jpg",
                    "version": "0.1",
                    "copyright": "Copyright 2018 Ikea.",
                    "authors": [
                        "Jane Doe",
                        "John Doe"
                    ]
                }
            }"""

        response = parser.parse_response(text)
        self.assertTrue(response)

        self.assertIsNotNone(parser.status)
        self.assertIsNotNone(parser.status)
        self.assertIsNotNone(parser.status)
