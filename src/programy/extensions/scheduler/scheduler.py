"""
Copyright (c) 2016-2018 Keith Sterling http://www.keithsterling.com

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated
documentation files (the "Software"), to deal in the Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software,
and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions
of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO
THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

"""
from programy.utils.logging.ylogger import YLogger

from programy.extensions.base import Extension


class SchedulerExtension(Extension):

    # execute() is the interface that is called from the <extension> tag in the AIML
    def execute(self, client_context, data):
        YLogger.debug(client_context, "Scheduler - [%s]", data)

        # REDMIND IN|EVERY X SECONDS|MINUTES|HOURS|DAYS|WEEKS MESSAGE|GRAMMAR ...........

        words = data.split()
        if len(words)> 5:
            if words[0].upper() == 'REMIND':
                when = words[1].upper()
                if when in ['IN', 'EVERY']:
                    quantity = int(words[2])
                    period = words[3].upper()
                    if period in ['SECONDS', 'MINUTES', 'HOURS', 'DAYS', 'WEEKS']:
                        action = words[4]
                        if action in ['MESSAGE', 'GRAMMAR']:
                            text = " ".join(words[5:])
                            self.schedule(client_context, when, quantity, period, action, text)
                            return 'OK'
                        else:
                            print ('MESSAGE missing')
                    else:
                        print ("Invalid period %s"% period)
                else:
                    print("Invalid when %s"% when)
            else:
                print ("Invalid command, must start with REMIND")

        return 'ERR'

    def schedule(self, client_context, when, quantity, period, action, text):

        if when == 'IN':
            if period == 'SECONDS':
                client_context.client.scheduler.schedule_in_n_seconds(client_context.userid, client_context.id, action, text, quantity)

        elif when == 'EVERY':
            if period == 'SECONDS':
                client_context.client.scheduler.schedule_every_n_seconds(client_context.userid, client_context.id, action, text, quantity)


