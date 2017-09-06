

class CustomAssertions:
    def assertOneOf(self, value, options):
        for option in options:
            if option == value:
                return
        raise AssertionError("Value %s, not one of %s" % (value, ", ".join(options)))
