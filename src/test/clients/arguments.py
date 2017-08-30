class MockArguments(object):

    def __init__(self, bot_root = ".", logging=None, config=None, cformat="yaml", noloop = False, context=None ):
        self.bot_root = bot_root
        self.logging = logging
        self.config = config
        self.cformat = cformat
        self.noloop = noloop
        self.context = context

class MockArgumentParser(object):

    def __init__(self, bot_root = ".", logging=None, config=None, cformat="yaml", noloop=False):
        self.bot_root = bot_root
        self.logging = logging
        self.config = config
        self.cformat = cformat
        self.noloop = noloop

    def add_argument(self, argument, dest=None, action=None, help=None):
        pass

    def parse_args(self):
        return MockArguments(bot_root=self.bot_root, logging=self.logging, config=self.config, cformat=self.cformat, noloop=self.noloop )
