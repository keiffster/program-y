"""
Copyright (c) 2016-2020 Keith Sterling http://www.keithsterling.com

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated
documentation files (the "Software"), to deal in the Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software,
and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the
Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO
THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""
import sys
import json
from flask import Flask, request
from programy.utils.logging.ylogger import YLogger
from programy.utils.console.console import outputLog


def handle_trigger(json_data):
    outputLog(None, "\nTrigger received...")
    try:
        outputLog(None, json.dumps(json.loads(json_data), indent=4))

    except Exception as excep:
        YLogger.exception_nostack(None, "Trigger failed", excep)
        outputLog(None, "Trigger failed [%s]" % str(excep))

    return 'OK'


if __name__ == '__main__':                                          # pragma: no cover
    outputLog(None, "Initiating Trigger Receiver...")               # pragma: no cover
    receiver = Flask(__name__)                                      # pragma: no cover

    @receiver.route('/api/rest/v1.0/trigger', methods=['POST'])     # pragma: no cover
    def trigger():                                                  # pragma: no cover
        handle_trigger(request.json)                                # pragma: no cover

    receiver.run(port=sys.argv[1])                                  # pragma: no cover
