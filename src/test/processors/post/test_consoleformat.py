import unittest
from programy.processors.post.consoleformat import ConsoleFormatPostProcessor
from programy.bot import Bot
from programy.brain import Brain
from programy.config.brain import BrainConfiguration
from programy.config.bot import BotConfiguration

class RemoveHTMLTests(unittest.TestCase):

    def setUp(self):
        self.bot = Bot(Brain(BrainConfiguration()), config=BotConfiguration())

    def test_format_console(self):
        processor = ConsoleFormatPostProcessor()

        result = processor.process(self.bot, "testid", "Hello World")
        self.assertIsNotNone(result)
        self.assertEqual("Hello World", result)

        result = processor.process(self.bot, "testid",
"""Lorem ipsum dolor sit amet, consectetur adipiscing elit. Rationis enim perfectio est virtus; Sed quid attinet de rebus tam apertis plura requirere?""")
        self.assertIsNotNone(result)
        self.assertEqual(
"""Lorem ipsum dolor sit amet, consectetur adipiscing elit. Rationis enim perfectio
est virtus; Sed quid attinet de rebus tam apertis plura requirere?""", result)
