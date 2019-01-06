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


class SchedulerExtension(Extension):

    def execute_schedule(self, client_context, words):
        action = words[1].upper()
        quantity = int(words[2])
        period = words[3].upper()
        if period in ['SECONDS', 'MINUTES', 'HOURS', 'DAYS', 'WEEKS']:
            type = words[4]
            if type in ['TEXT', 'SRAI']:
                text = " ".join(words[5:])
                self.schedule(client_context, action, quantity, period, type, text)
                return 'OK'
            else:
                raise Exception('Scheduler action missing')
        else:
            raise Exception("Scheduler invalid period %s" % period)

    def get_users_jobs(self, client_context):
        user_jobs = []
        jobs = client_context.client.scheduler.list_jobs()
        for id, job in jobs.items():
            if client_context.userid == job.args[1]:
                user_jobs.append(job)
        return user_jobs

    def execute_pause(self, client_context, words):
        which = words[2].upper()
        jobs = self.get_users_jobs(client_context)
        if which == 'ALL':
            for job in jobs:
                client_context.client.scheduler.pause_job(job.id)
            return 'OK'

        else:
            index = int(which) - 1
            if index < len(jobs):
                job = jobs[index]
                client_context.client.scheduler.pause_job(job.id)
                return 'OK'

        return 'ERR'

    def execute_resume(self, client_context, words):
        which = words[2].upper()
        jobs = self.get_users_jobs(client_context)
        if which == 'ALL':
            for job in jobs:
                client_context.client.scheduler.resume_job(job.id)
            return 'OK'

        else:
            index = int(which) - 1
            if index < len(jobs):
                job = jobs[index]
                client_context.client.scheduler.resume_job(job.id)
                return 'OK'

        return 'ERR'

    def execute_stop(self, client_context, words):
        which = words[2].upper()
        jobs = self.get_users_jobs(client_context)
        if which == 'ALL':
            for job in jobs:
                client_context.client.scheduler.stop_job(job.id)
            return 'OK'

        else:
            index = int(which) - 1
            if index < len(jobs):
                job = jobs[index]
                client_context.client.scheduler.stop_job(job.id)
                return 'OK'

        return 'ERR'

    def execute_lists(self, client_context, words):
        jobs = self.get_users_jobs(client_context)
        if jobs:
            str = "OK <olist>"
            for job in jobs:
                if client_context.userid == job.args[1]:
                    str += "<item>" + job.id + "</item>"
            str += "</olist>"
            return str

        return 'ERR'

    # execute() is the interface that is called from the <extension> tag in the AIML
    def execute(self, client_context, data):
        YLogger.debug(client_context, "Scheduler - [%s]", data)

        # SCHEDULE IN|EVERY X SECONDS|MINUTES|HOURS|DAYS|WEEKS TEXT|SRAI ...........

        try:
            words = data.split()
            if words[0].upper() == 'SCHEDULE':
                action = words[1].upper()
                if action in ['IN', 'EVERY']:
                    return self.execute_schedule(client_context, words)

                elif action == 'PAUSE':
                    return self.execute_pause(client_context, words)

                elif action == 'RESUME':
                    return self.execute_resume(client_context, words)

                elif action == 'STOP':
                    return self.execute_stop(client_context, words)

                elif action == 'LIST':
                    return self.execute_lists(client_context, words)

                else:
                    raise Exception ("Scheduler invalid action %s"% action)
            else:
                raise Exception ("Scheduler invalid command, must start with SCHEDULE")

        except Exception as excep:
            YLogger.exception(client_context, "Failed to parse Scheduler command", excep)

        return 'ERR'

    def schedule(self, client_context, when, quantity, period, type, text):

        if when == 'IN':
            if period == 'SECONDS':
                client_context.client.scheduler.schedule_in_n_seconds(client_context.userid, client_context.id, type, text, quantity)
            elif period == 'MINUTES':
                client_context.client.scheduler.schedule_in_n_minutes(client_context.userid, client_context.id, type, text, quantity)
            elif period == 'HOURS':
                client_context.client.scheduler.schedule_in_n_hours(client_context.userid, client_context.id, type, text, quantity)
            elif period == 'DAYS':
                client_context.client.scheduler.schedule_in_n_days(client_context.userid, client_context.id, type, text, quantity)
            elif period == 'WEEKS':
                client_context.client.scheduler.schedule_in_n_weeks(client_context.userid, client_context.id, type, text, quantity)
            else:
                raise Exception("Scheduler invalid period - %s"%period)

        elif when == 'EVERY':
            if period == 'SECONDS':
                client_context.client.scheduler.schedule_every_n_seconds(client_context.userid, client_context.id, type, text, quantity)
            elif period == 'MINUTES':
                client_context.client.scheduler.schedule_every_n_minutes(client_context.userid, client_context.id, type, text, quantity)
            elif period == 'HOURS':
                client_context.client.scheduler.schedule_every_n_hours(client_context.userid, client_context.id, type, text, quantity)
            elif period == 'DAYS':
                client_context.client.scheduler.schedule_every_n_days(client_context.userid, client_context.id, type, text, quantity)
            elif period == 'WEEKS':
                client_context.client.scheduler.schedule_every_n_weeks(client_context.userid, client_context.id, type, text, quantity)
            else:
                raise Exception("Scheduler invalid period - %s"%period)

        else:
            raise Exception("Scheduler invalid repeat - %s"%when)

