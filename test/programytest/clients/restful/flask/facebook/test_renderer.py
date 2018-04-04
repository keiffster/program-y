import unittest

from programy.clients.restful.flask.facebook.renderer import FacebookBot


class FacebookBotTests(unittest.TestCase):

    def test_render_payload(self):

        bot = FacebookBot("AUTH_TOKEN")
        self.assertIsNotNone(bot)

        message = """
            What do you want for tea?
            <button>
                <text>Chips</text>
                <postback>CHIPS</postback>
            </button>
            <button>
                <text>Mash Potato</text>
                <postback>MASH</postback>
            </button>
        """

        payload = bot.render_payload(message)
        self.assertIsNotNone(payload)

