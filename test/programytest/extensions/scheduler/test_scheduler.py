import unittest

from programy.extensions.scheduler.scheduler import SchedulerExtension
from programytest.client import TestClient


class SchedulerExtensionClient(TestClient):

    def __init__(self, mock_scheduler=None):
        self._mock_scheduler = mock_scheduler
        TestClient.__init__(self)

    def load_configuration(self, arguments):
        super(SchedulerExtensionClient, self).load_configuration(arguments)

    def load_scheduler(self):
        if self._mock_scheduler  is not None:
            self._scheduler = self._mock_scheduler
        else:
            super(SchedulerExtensionClient, self).load_scheduler()


class MockJob:

    def __init__(self, id, userid):
        self.args = [id, userid]

    @property
    def id(self):
        return self.args[0]


class MockScheduler:

    def __init__(self):
        self._jobs = ()

    def add_jobs(self, jobs):
        self._jobs = jobs

    def list_jobs(self):
        return self._jobs

    def pause_job (self, id):
        pass

    def resume_job (self, id):
        pass

    def stop_job (self, id):
        pass

    def schedule_every_n_seconds(self, userid, clientid, action, text, seconds):
        pass

    def schedule_every_n_minutes(self, userid, clientid, action, text, minutes):
        pass

    def schedule_every_n_hours(self, userid, clientid, action, text, hours):
        pass

    def schedule_every_n_days(self, userid, clientid, action, text, days):
        pass

    def schedule_every_n_weeks(self, userid, clientid, action, text, weeks):
        pass

    def schedule_every_n(self, userid, clientid, action, text, weeks=0, days=0, hours=0, minutes=0, seconds=0):
        pass

    def schedule_in_n_weeks(self, userid, clientid, action, text, weeks):
        pass

    def schedule_in_n_days(self, userid, clientid, action, text, days):
        pass

    def schedule_in_n_hours(self, userid, clientid, action, text, hours):
        pass

    def schedule_in_n_minutes(self, userid, clientid, action, text, minutes):
        pass

    def schedule_in_n_seconds(self, userid, clientid, action, text, seconds):
        pass


class SchedulerExtensionTests(unittest.TestCase):

    # SCHEDULE IN|EVERY X SECS|MINS|HOURS|DAYS|WEEKS TEXT|SRAI TEXT ...........
    # PAUSE ALL|JOBID
    # RESUME ALL|JOBID
    # STOP ALL|JOBID
    # LIST

    def test_schedule_invalid(self):
        client = SchedulerExtensionClient()
        client_context = client.create_client_context("testid")
        extension = SchedulerExtension()

        self.assertEquals("ERR", extension.execute(client_context, "OTHER"))
        self.assertEquals("ERR", extension.execute(client_context, "SCHEDULE OTHER"))

    def test_schedule_in_invalid(self):
        client = SchedulerExtensionClient()
        client_context = client.create_client_context("testid")
        extension = SchedulerExtension()

        self.assertEquals("ERR", extension.execute(client_context, "SCHEDULE IN"))
        self.assertEquals("ERR", extension.execute(client_context, "SCHEDULE IN 10"))
        self.assertEquals("ERR", extension.execute(client_context, "SCHEDULE IN 10 OTHER"))
        self.assertEquals("ERR", extension.execute(client_context, "SCHEDULE IN 10 MINUTES OTHER"))
        self.assertEquals("ERR", extension.execute(client_context, "SCHEDULE IN 10 MINUTES TEXT"))
        self.assertEquals("ERR", extension.execute(client_context, "SCHEDULE IN 10 MINUTES SRAI"))

    def test_schedule_every_invalid(self):
        client = SchedulerExtensionClient()
        client_context = client.create_client_context("testid")
        extension = SchedulerExtension()

        self.assertEquals("ERR", extension.execute(client_context, "SCHEDULE EVERY"))
        self.assertEquals("ERR", extension.execute(client_context, "SCHEDULE EVER 10"))
        self.assertEquals("ERR", extension.execute(client_context, "SCHEDULE EVER 10 OTHER"))
        self.assertEquals("ERR", extension.execute(client_context, "SCHEDULE EVER 10 MINUTES OTHER"))
        self.assertEquals("ERR", extension.execute(client_context, "SCHEDULE EVER 10 MINUTES TEXT"))
        self.assertEquals("ERR", extension.execute(client_context, "SCHEDULE EVER 10 MINUTES SRAI"))

    # IN XXXX

    def test_schedule_in_n_seconds(self):
        client = SchedulerExtensionClient()
        client_context = client.create_client_context("testid")
        extension = SchedulerExtension()
        response = extension.execute(client_context, "SCHEDULE IN 10 SECONDS TEXT WAKEY WAKEY")
        self.assertEqual("OK", response)

    def test_schedule_in_n_minutes(self):
        client = SchedulerExtensionClient()
        client_context = client.create_client_context("testid")
        extension = SchedulerExtension()
        response = extension.execute(client_context, "SCHEDULE IN 10 MINUTES TEXT WAKEY WAKEY")
        self.assertEqual("OK", response)

    def test_schedule_in_n_hours(self):
        client = SchedulerExtensionClient()
        client_context = client.create_client_context("testid")
        extension = SchedulerExtension()
        response = extension.execute(client_context, "SCHEDULE IN 10 HOURS TEXT WAKEY WAKEY")
        self.assertEqual("OK", response)

    def test_schedule_in_n_days(self):
        client = SchedulerExtensionClient()
        client_context = client.create_client_context("testid")
        extension = SchedulerExtension()
        response = extension.execute(client_context, "SCHEDULE IN 10 DAYS TEXT WAKEY WAKEY")
        self.assertEqual("OK", response)

    def test_schedule_in_n_weeks(self):
        client = SchedulerExtensionClient()
        client_context = client.create_client_context("testid")
        extension = SchedulerExtension()
        response = extension.execute(client_context, "SCHEDULE IN 10 WEEKS TEXT WAKEY WAKEY")
        self.assertEqual("OK", response)

    # EVERY XXX

    def test_schedule_every_n_seconds(self):
        client = SchedulerExtensionClient()
        client_context = client.create_client_context("testid")
        client_context.client._scheduler = MockScheduler()
        extension = SchedulerExtension()
        response = extension.execute(client_context, "SCHEDULE EVERY 10 SECONDS TEXT WAKEY WAKEY")
        self.assertEqual("OK", response)

    def test_schedule_every_n_minutes(self):
        client = SchedulerExtensionClient()
        client_context = client.create_client_context("testid")
        extension = SchedulerExtension()
        response = extension.execute(client_context, "SCHEDULE EVERY 10 MINUTES TEXT WAKEY WAKEY")
        self.assertEqual("OK", response)

    def test_schedule_every_n_hours(self):
        client = SchedulerExtensionClient()
        client_context = client.create_client_context("testid")
        extension = SchedulerExtension()
        response = extension.execute(client_context, "SCHEDULE EVERY 10 HOURS TEXT WAKEY WAKEY")
        self.assertEqual("OK", response)

    def test_schedule_every_n_days(self):
        client = SchedulerExtensionClient()
        client_context = client.create_client_context("testid")
        extension = SchedulerExtension()
        response = extension.execute(client_context, "SCHEDULE EVERY 10 DAYS TEXT WAKEY WAKEY")
        self.assertEqual("OK", response)

    def test_schedule_every_n_weeks(self):
        client = SchedulerExtensionClient()
        client_context = client.create_client_context("testid")
        extension = SchedulerExtension()
        response = extension.execute(client_context, "SCHEDULE EVERY 10 WEEKS TEXT WAKEY WAKEY")
        self.assertEqual("OK", response)

    # Other commands

    def test_pause_all(self):
        client = SchedulerExtensionClient()
        client_context = client.create_client_context("testid")
        client_context.client._scheduler = MockScheduler()
        client_context.client._scheduler.add_jobs({1: MockJob(1, "testid")})

        extension = SchedulerExtension()
        response = extension.execute(client_context, "SCHEDULE PAUSE ALL")
        self.assertEquals("OK", response)

    def test_pause_all_no_jobs(self):
        client = SchedulerExtensionClient()
        client_context = client.create_client_context("testid")
        client_context.client._scheduler = MockScheduler()

        extension = SchedulerExtension()
        response = extension.execute(client_context, "SCHEDULE PAUSE ALL")
        self.assertEquals("ERR", response)

    def test_pause_job(self):
        client = SchedulerExtensionClient()
        client_context = client.create_client_context("testid")
        client_context.client._scheduler = MockScheduler()
        client_context.client._scheduler.add_jobs({1: MockJob(1, "testid")})

        extension = SchedulerExtension()
        response = extension.execute(client_context, "SCHEDULE PAUSE 1")
        self.assertEquals("OK", response)

    def test_pause_job_diff_id(self):
        client = SchedulerExtensionClient()
        client_context = client.create_client_context("testid")
        client_context.client._scheduler = MockScheduler()
        client_context.client._scheduler.add_jobs({1: MockJob(1, "testid")})

        extension = SchedulerExtension()
        response = extension.execute(client_context, "SCHEDULE PAUSE 2")
        self.assertEquals("ERR", response)

    def test_pause_job_no_userid(self):
        client = SchedulerExtensionClient()
        client_context = client.create_client_context("testid")
        client_context.client._scheduler = MockScheduler()
        client_context.client._scheduler.add_jobs({1: MockJob(1, "testid2")})

        extension = SchedulerExtension()
        response = extension.execute(client_context, "SCHEDULE PAUSE 1")
        self.assertEquals("ERR", response)

    def test_pause_job_no_jobs(self):
        client = SchedulerExtensionClient()
        client_context = client.create_client_context("testid")
        client_context.client._scheduler = MockScheduler()

        extension = SchedulerExtension()
        response = extension.execute(client_context, "SCHEDULE PAUSE 1")
        self.assertEquals("ERR", response)

    def test_resume_all(self):
        client = SchedulerExtensionClient()
        client_context = client.create_client_context("testid")
        client_context.client._scheduler = MockScheduler()
        client_context.client._scheduler.add_jobs({1: MockJob(1, "testid")})

        extension = SchedulerExtension()
        response = extension.execute(client_context, "SCHEDULE RESUME ALL")
        self.assertEquals("OK", response)

    def test_resume_all_no_jobs(self):
        client = SchedulerExtensionClient()
        client_context = client.create_client_context("testid")
        client_context.client._scheduler = MockScheduler()

        extension = SchedulerExtension()
        response = extension.execute(client_context, "SCHEDULE RESUME ALL")
        self.assertEquals("ERR", response)

    def test_resume_job(self):
        client = SchedulerExtensionClient()
        client_context = client.create_client_context("testid")
        client_context.client._scheduler = MockScheduler()
        client_context.client._scheduler.add_jobs({1: MockJob(1, "testid")})

        extension = SchedulerExtension()
        response = extension.execute(client_context, "SCHEDULE RESUME 1")
        self.assertEquals("OK", response)

    def test_resume_job_diff_id(self):
        client = SchedulerExtensionClient()
        client_context = client.create_client_context("testid")
        client_context.client._scheduler = MockScheduler()
        client_context.client._scheduler.add_jobs({1: MockJob(1, "testid")})

        extension = SchedulerExtension()
        response = extension.execute(client_context, "SCHEDULE RESUME 2")
        self.assertEquals("ERR", response)

    def test_resume_job_no_userid(self):
        client = SchedulerExtensionClient()
        client_context = client.create_client_context("testid")
        client_context.client._scheduler = MockScheduler()
        client_context.client._scheduler.add_jobs({1: MockJob(1, "testid2")})

        extension = SchedulerExtension()
        response = extension.execute(client_context, "SCHEDULE RESUME 1")
        self.assertEquals("ERR", response)

    def test_resume_job_no_jobs(self):
        client = SchedulerExtensionClient()
        client_context = client.create_client_context("testid")
        client_context.client._scheduler = MockScheduler()

        extension = SchedulerExtension()
        response = extension.execute(client_context, "SCHEDULE RESUME 1")
        self.assertEquals("ERR", response)

    def test_stop_all(self):
        client = SchedulerExtensionClient()
        client_context = client.create_client_context("testid")
        client_context.client._scheduler = MockScheduler()
        client_context.client._scheduler.add_jobs({1: MockJob(1, "testid")})

        extension = SchedulerExtension()
        response = extension.execute(client_context, "SCHEDULE STOP ALL")
        self.assertEquals("OK", response)

    def test_stop_all_no_jobs(self):
        client = SchedulerExtensionClient()
        client_context = client.create_client_context("testid")
        client_context.client._scheduler = MockScheduler()

        extension = SchedulerExtension()
        response = extension.execute(client_context, "SCHEDULE STOP ALL")
        self.assertEquals("ERR", response)

    def test_stop_job(self):
        client = SchedulerExtensionClient()
        client_context = client.create_client_context("testid")
        client_context.client._scheduler = MockScheduler()
        client_context.client._scheduler.add_jobs({1: MockJob(1, "testid")})

        extension = SchedulerExtension()
        response = extension.execute(client_context, "SCHEDULE STOP 1")
        self.assertEquals("OK", response)

    def test_stop_job_diff_id(self):
        client = SchedulerExtensionClient()
        client_context = client.create_client_context("testid")
        client_context.client._scheduler = MockScheduler()
        client_context.client._scheduler.add_jobs({1: MockJob(1, "testid")})

        extension = SchedulerExtension()
        response = extension.execute(client_context, "SCHEDULE STOP 2")
        self.assertEquals("ERR", response)

    def test_stop_job_no_userid(self):
        client = SchedulerExtensionClient()
        client_context = client.create_client_context("testid")
        client_context.client._scheduler = MockScheduler()
        client_context.client._scheduler.add_jobs({1: MockJob(1, "testid2")})

        extension = SchedulerExtension()
        response = extension.execute(client_context, "SCHEDULE STOP 1")
        self.assertEquals("ERR", response)

    def test_stop_job_no_jobs(self):
        client = SchedulerExtensionClient()
        client_context = client.create_client_context("testid")
        client_context.client._scheduler = MockScheduler()

        extension = SchedulerExtension()
        response = extension.execute(client_context, "SCHEDULE STOP 1")
        self.assertEquals("ERR", response)

    def test_list(self):
        client = SchedulerExtensionClient()
        client_context = client.create_client_context("testid")
        client_context.client._scheduler = MockScheduler()
        client_context.client._scheduler.add_jobs({1: MockJob(1, "testid")})

        extension = SchedulerExtension()
        response = extension.execute(client_context, "SCHEDULE LIST")
        self.assertEquals("OK <olist><item>1</item></olist>", response)

    def test_list_mulit_userids(self):
        client = SchedulerExtensionClient()
        client_context = client.create_client_context("testid")
        client_context.client._scheduler = MockScheduler()
        client_context.client._scheduler.add_jobs({1: MockJob(1, "testid"), 2: MockJob(2, "testid2"), 3: MockJob(3, "testid")})

        extension = SchedulerExtension()
        response = extension.execute(client_context, "SCHEDULE LIST")
        self.assertEquals("OK <olist><item>1</item><item>3</item></olist>", response)

    def test_list_no_userid_jobs(self):
        client = SchedulerExtensionClient()
        client_context = client.create_client_context("testid")
        client_context.client._scheduler = MockScheduler()
        client_context.client._scheduler.add_jobs({1: MockJob(1, "testid2")})

        extension = SchedulerExtension()
        response = extension.execute(client_context, "SCHEDULE LIST")
        self.assertEquals("ERR", response)
