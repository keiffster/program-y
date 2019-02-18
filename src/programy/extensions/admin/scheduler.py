"""
Copyright (c) 2016-2019 Keith Sterling http://www.keithsterling.com

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


class SchedulerAdminExtension(Extension):

    # execute() is the interface that is called from the <extension> tag in the AIML
    def execute(self, client_context, data):
        YLogger.debug(client_context, "Scheduler Admin - [%s]", data)

        try:
            commands = [x.upper() for x in data.split()]

            if commands[0] == 'COMMANDS':

                return "LIST JOBS, KILL JOB, PAUSE, RESUME"

            elif commands[0] == 'LIST':

                if commands[1] == 'JOBS':
                    jobs = client_context.client.scheduler.list_jobs()
                    if jobs:
                        response = ""
                        for id, job in jobs.items():
                            response += "> Job ID:%s, Next Run: %s, Args: %s\n"%(id, job.next_run_time, str(job.args))
                        return response

                    return "No job information available"

            elif commands[0] == 'KILL':

                if commands[1] == 'JOB':
                    id = commands[2]
                    client_context.client.scheduler.remove_existing_job(id)
                    return "Job removed"

            elif commands[0] == 'PAUSE':
                client_context.client.scheduler.pause()
                return "Scheduler paused"

            elif commands[0] == 'RESUME':
                client_context.client.scheduler.resume()
                return "Scheduler resumed"

        except Exception as e:
            YLogger.exception(client_context, "Failed to execute scheduler extension", e)

        return "Scheduler Admin Error"