from programy.oob.callmom.dial import DialOutOfBandProcessor


class MockDialOutOfBandProcessor(DialOutOfBandProcessor):

    dialed = None

    def __init__(self):
        DialOutOfBandProcessor.__init__(self)

    def execute_oob_command(self, client_context):
        MockDialOutOfBandProcessor.dialed = self._number
        return ""
