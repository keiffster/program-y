"""
Copyright (c) 2016-2020 Keith Sterling http://www.keithsterling.com

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

    def _commands(self):
        return "LIST JOBS, KILL JOB, PAUSE, RESUME"

    def _list(self, commands, client_context):
        if len(commands) == 2:
            if commands[1] == 'JOBS':
                jobs = client_context.client.scheduler.list_jobs()
                if jobs:
                    response = ""
                    for jobid, job in jobs.items():
                        response += "> Job ID:%s, Next Run: %s, Args: %s\n" % (jobid,
                                                                               job.next_run_time,
                                                                               str(job.args))
                    return response

                return "No job information available"

            else:
                return "Unknown LIST sub command [%s]" % commands[1]

        else:
            return "Invalid LIST commands, LIST JOBS"

    def _kill(self, commands, client_context):
        if len(commands) == 3:

            if commands[1] == 'JOB':
                client_context.client.scheduler.remove_existing_job(commands[2])
                return "Job removed"

            else:
                return "Unknown KILL sub command [%s]" % commands[1]

        else:
            return "Invalid KILL commands, LIST JOB JOBID"

    def _pause(self, client_context):
        client_context.client.scheduler.pause()
        return "Scheduler paused"

    def _resume(self, client_context):
        client_context.client.scheduler.resume()
        return "Scheduler resumed"

    # execute() is the interface that is called from the <extension> tag in the AIML
    def execute(self, client_context, data):
        YLogger.debug(client_context, "Scheduler Admin - [%s]", data)

        try:
            commands = [x.upper() for x in data.split()]

            command = commands[0]

            if command == 'COMMANDS':
                return self._commands()

            elif command == 'LIST':
                return self._list(commands, client_context)

            elif command == 'KILL':
                return self._kill(commands, client_context)

            elif command == 'PAUSE':
                return self._pause(client_context)

            elif command == 'RESUME':
                return self._resume(client_context)

            else:
                return "Invalid Scheduler Admin command [%s]" % command

        except Exception as e:
            YLogger.exception(client_context, "Failed to execute scheduler extension", e)

        return "Scheduler Admin Error"
