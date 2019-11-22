import unittest
import unittest.mock
import logging
import apscheduler.events
from datetime import datetime
from apscheduler.events import SchedulerEvent, JobEvent, JobSubmissionEvent, JobExecutionEvent
from programy.scheduling.scheduler import ProgramyScheduler
from programy.scheduling.scheduler import scheduler_listener
from programy.scheduling.config import SchedulerConfiguration
from programy.scheduling.config import SchedulerJobStoreConfiguration
from programy.scheduling.config import SchedulerSqlAlchemyJobStoreConfiguration
from programy.scheduling.scheduler import scheduled
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.schedulers.blocking import BlockingScheduler
from programytest.client import TestClient


class MockJob:

    def __init__(self, jobid):
        self.id = jobid


class MockScheduler(object):

    def __init__(self):
        self._started = False
        self._emptied = False
        self._paused = False
        self._jobs = {}
        self._status = {}

    def start(self, *args, **kwargs):
        self._started = True

    def shutdown(self, wait=True):
        self._started = False

    def pause(self):
        self._pause = True

    def resume(self):
        self._pause = False

    def add_job(self, func, trigger=None, args=None, kwargs=None, id=None, name=None,
                misfire_grace_time=None, coalesce=None, max_instances=None,
                next_run_time=None, jobstore='default', executor='default',
                replace_existing=False, **trigger_args):
        self._jobs[id] = id
        self._status[id] = "started"

    def get_job(self, job_id, jobstore=None):
        if job_id in self._jobs:
            return self._jobs[job_id]
        return None

    def get_jobs(self):
        return [MockJob(x) for x in self._jobs]

    def remove_job(self, job_id, jobstore=None):
        del self._jobs[job_id]
        del self._status[job_id]

    def remove_all_jobs(self):
        self._emptied = True
        self._jobs.clear()
        self._status.clear()

    def stop_job(self, jobid):
        self._status[jobid] = "stopped"

    def pause_job(self, jobid):
        self._status[jobid] = "paused"

    def resume_job(self, jobid):
        self._status[jobid] = "started"


class MockProgramyScheduler(ProgramyScheduler):

    def __init__(self, client, config):
        self._scheduled = False
        ProgramyScheduler.__init__(self, client, config)

    def _create_scheduler(self, configuration):
        return MockScheduler()

    def scheduled(self, userid, clientid, action, text):
        self._scheduled = True


class MockBot:

    def ask_question(self, client_context, text):
        return "Mock Response"


class MockClientContext:

    def __init__(self):
        self.bot = MockBot()


class MockClient:

    def __init__(self):
        self._response = None

    def render_response(self, client_context, text):
        self._response = text

    def create_client_context(self, userid):
        return MockClientContext()


class ProgramySchedulerTests(unittest.TestCase):

    def setUp(self):
        self._test_client = TestClient()
        ProgramyScheduler.schedulers.clear()
        self.assertEqual(0, len(ProgramyScheduler.schedulers.keys()))

    def create_config(self, remove, debug, listeners, name="Scheduler1"):
        config = unittest.mock.Mock()
        config.remove_all_jobs = remove
        config.debug_level = debug
        config.add_listeners = listeners
        config.name = name
        return config

    def test_init_default_config(self):
        config = SchedulerConfiguration()
        self.assertIsNotNone(config)
        scheduler = ProgramyScheduler(self._test_client, config)
        self.assertIsNotNone(scheduler)
        self.assertIsInstance(scheduler._scheduler, BackgroundScheduler)

    def test_create_scheduler_no_config(self):
        scheduler = ProgramyScheduler(self._test_client, None)
        self.assertIsNotNone(scheduler)
        self.assertIsNone(scheduler._scheduler)

    def test_init_custom_config(self):
        config = SchedulerConfiguration()
        config._debug_level = logging.DEBUG
        config._add_listeners = True

        self.assertIsNotNone(config)
        scheduler = ProgramyScheduler(self._test_client, config)
        self.assertIsNotNone(scheduler)
        self.assertIsInstance(scheduler._scheduler, BackgroundScheduler)

    def test_create_scheduler_blocking_with_jobstore(self):
        config = SchedulerConfiguration()
        config._blocking = True

        config._jobstore = SchedulerJobStoreConfiguration()
        config._jobstore._name = "sqlalchemy"
        config._jobstore._storage = SchedulerSqlAlchemyJobStoreConfiguration()
        config._jobstore._storage._url = "sqlite:///programy.sqlite"

        scheduler = ProgramyScheduler(self._test_client, config)
        self.assertIsNotNone(scheduler)
        self.assertIsInstance(scheduler._scheduler, BlockingScheduler)

    def test_create_scheduler_blocking(self):
        config = SchedulerConfiguration()
        config._blocking = True

        self.assertIsNotNone(config)
        scheduler = ProgramyScheduler(self._test_client, config)
        self.assertIsNotNone(scheduler)
        self.assertIsInstance(scheduler._scheduler, BlockingScheduler)

    def test_create_scheduler_no_blocking(self):
        config = SchedulerConfiguration()
        config._blocking = False

        self.assertIsNotNone(config)
        scheduler = ProgramyScheduler(self._test_client, config)
        self.assertIsNotNone(scheduler)
        self.assertIsInstance(scheduler._scheduler, BackgroundScheduler)

    def test_create_scheduler_no_blocking_with_jobstore(self):
        config = SchedulerConfiguration()
        config._blocking = False

        config._jobstore = SchedulerJobStoreConfiguration()
        config._jobstore._name = "sqlalchemy"
        config._jobstore._storage = SchedulerSqlAlchemyJobStoreConfiguration()
        config._jobstore._storage._url = "sqlite:///programy.sqlite"

        self.assertIsNotNone(config)
        scheduler = ProgramyScheduler(self._test_client, config)
        self.assertIsNotNone(scheduler)
        self.assertIsInstance(scheduler._scheduler, BackgroundScheduler)

    def test_scheduler_listener(self):
        config = SchedulerConfiguration()
        self.assertIsNotNone(config)
        scheduler = ProgramyScheduler(self._test_client, config)
        self.assertIsNotNone(scheduler)

        scheduler_listener(JobExecutionEvent(apscheduler.events.EVENT_SCHEDULER_STARTED, 1, None, None))

    def test_scheduler_listener_unknown_event(self):
        config = SchedulerConfiguration()
        self.assertIsNotNone(config)
        scheduler = ProgramyScheduler(self._test_client, config)
        self.assertIsNotNone(scheduler)

        scheduler_listener(JobExecutionEvent(-1, 1, None, None))

    def test_registration(self):

        scheduler1 = MockProgramyScheduler(self._test_client, self.create_config(False, None, False))
        self.assertIsNotNone(ProgramyScheduler.schedulers)
        self.assertEqual(1, len(ProgramyScheduler.schedulers.keys()))
        self.assertTrue("Scheduler1" in ProgramyScheduler.schedulers)
        self.assertEqual(scheduler1, ProgramyScheduler.schedulers['Scheduler1'])

        MockProgramyScheduler(self._test_client, self.create_config(False, None, False))
        self.assertIsNotNone(ProgramyScheduler.schedulers)
        self.assertEqual(1, len(ProgramyScheduler.schedulers.keys()))
        self.assertTrue("Scheduler1" in ProgramyScheduler.schedulers)
        self.assertEqual(scheduler1, ProgramyScheduler.schedulers['Scheduler1'])

        scheduler3 = MockProgramyScheduler(self._test_client, self.create_config(False, None, False, name="Scheduler3"))
        self.assertIsNotNone(ProgramyScheduler.schedulers)
        self.assertEqual(2, len(ProgramyScheduler.schedulers.keys()))
        self.assertTrue("Scheduler1" in ProgramyScheduler.schedulers)
        self.assertTrue("Scheduler3" in ProgramyScheduler.schedulers)
        self.assertEqual(scheduler1, ProgramyScheduler.schedulers['Scheduler1'])
        self.assertEqual(scheduler3, ProgramyScheduler.schedulers['Scheduler3'])

    def test_start_stop(self):
        scheduler = MockProgramyScheduler(self._test_client, self.create_config(False, None, False))
        self.assertIsNotNone(scheduler)
        self.assertFalse(scheduler._scheduler._started)
        scheduler.start()
        self.assertTrue(scheduler._scheduler._started)
        scheduler.pause()
        self.assertTrue(scheduler._scheduler._started)
        scheduler.resume()
        self.assertTrue(scheduler._scheduler._started)
        scheduler.stop()
        self.assertFalse(scheduler._scheduler._started)

    def test_empty_jobs(self):
        scheduler = MockProgramyScheduler(self._test_client, self.create_config(True, None, False))
        self.assertIsNotNone(scheduler)
        self.assertTrue(scheduler._scheduler._emptied)
        self.assertEqual(0, len(scheduler._scheduler._jobs.keys()))

    def test_not_empty_jobs(self):
        scheduler = MockProgramyScheduler(self._test_client, self.create_config(False, None, False))
        self.assertIsNotNone(scheduler)
        self.assertFalse(scheduler._scheduler._emptied)
        self.assertEqual(0, len(scheduler._scheduler._jobs.keys()))

    def test_add_job_every_seconds(self):
        scheduler = MockProgramyScheduler(self._test_client, self.create_config(False, None, False))
        self.assertIsNotNone(scheduler)
        self.assertEqual(0, len(scheduler._scheduler._jobs.keys()))

        scheduler.schedule_every_n_seconds("testuser", "testclient", "MESSAGE", "REMIND ME", 3)
        self.assertEqual(1, len(scheduler._scheduler._jobs.keys()))

        scheduler.schedule_every_n_seconds("testuser", "testclient", "MESSAGE", "REMIND ME", 3)
        self.assertEqual(1, len(scheduler._scheduler._jobs.keys()))

        scheduler.schedule_every_n_seconds("testuser", "testclient", "MESSAGE", "REMIND ME 2", 3)
        self.assertEqual(2, len(scheduler._scheduler._jobs.keys()))

        jobs = scheduler.list_jobs()
        self.assertIsNotNone(jobs)
        self.assertEquals(2, len(jobs))

    def test_add_job_every_minutes(self):
        scheduler = MockProgramyScheduler(self._test_client, self.create_config(False, None, False))
        self.assertIsNotNone(scheduler)
        self.assertEqual(0, len(scheduler._scheduler._jobs.keys()))

        scheduler.schedule_every_n_minutes("testuser", "testclient", "MESSAGE", "REMIND ME", 3)
        self.assertEqual(1, len(scheduler._scheduler._jobs.keys()))

        scheduler.schedule_every_n_minutes("testuser", "testclient", "MESSAGE", "REMIND ME", 3)
        self.assertEqual(1, len(scheduler._scheduler._jobs.keys()))

        scheduler.schedule_every_n_minutes("testuser", "testclient", "MESSAGE", "REMIND ME 2", 3)
        self.assertEqual(2, len(scheduler._scheduler._jobs.keys()))

        jobs = scheduler.list_jobs()
        self.assertIsNotNone(jobs)
        self.assertEquals(2, len(jobs))

    def test_add_job_every_hours(self):
        scheduler = MockProgramyScheduler(self._test_client, self.create_config(False, None, False))
        self.assertIsNotNone(scheduler)
        self.assertEqual(0, len(scheduler._scheduler._jobs.keys()))

        scheduler.schedule_every_n_hours("testuser", "testclient", "MESSAGE", "REMIND ME", 3)
        self.assertEqual(1, len(scheduler._scheduler._jobs.keys()))

        scheduler.schedule_every_n_hours("testuser", "testclient", "MESSAGE", "REMIND ME", 3)
        self.assertEqual(1, len(scheduler._scheduler._jobs.keys()))

        scheduler.schedule_every_n_hours("testuser", "testclient", "MESSAGE", "REMIND ME 2", 3)
        self.assertEqual(2, len(scheduler._scheduler._jobs.keys()))

        jobs = scheduler.list_jobs()
        self.assertIsNotNone(jobs)
        self.assertEquals(2, len(jobs))

    def test_add_job_every_days(self):
        scheduler = MockProgramyScheduler(self._test_client, self.create_config(False, None, False))
        self.assertIsNotNone(scheduler)
        self.assertEqual(0, len(scheduler._scheduler._jobs.keys()))

        scheduler.schedule_every_n_days("testuser", "testclient", "MESSAGE", "REMIND ME", 3)
        self.assertEqual(1, len(scheduler._scheduler._jobs.keys()))

        scheduler.schedule_every_n_days("testuser", "testclient", "MESSAGE", "REMIND ME", 3)
        self.assertEqual(1, len(scheduler._scheduler._jobs.keys()))

        scheduler.schedule_every_n_days("testuser", "testclient", "MESSAGE", "REMIND ME 2", 3)
        self.assertEqual(2, len(scheduler._scheduler._jobs.keys()))

        jobs = scheduler.list_jobs()
        self.assertIsNotNone(jobs)
        self.assertEquals(2, len(jobs))

    def test_add_job_every_weeks(self):
        scheduler = MockProgramyScheduler(self._test_client, self.create_config(False, None, False))
        self.assertIsNotNone(scheduler)
        self.assertEqual(0, len(scheduler._scheduler._jobs.keys()))

        scheduler.schedule_every_n_weeks("testuser", "testclient", "MESSAGE", "REMIND ME", 3)
        self.assertEqual(1, len(scheduler._scheduler._jobs.keys()))

        scheduler.schedule_every_n_weeks("testuser", "testclient", "MESSAGE", "REMIND ME", 3)
        self.assertEqual(1, len(scheduler._scheduler._jobs.keys()))

        scheduler.schedule_every_n_weeks("testuser", "testclient", "MESSAGE", "REMIND ME 2", 3)
        self.assertEqual(2, len(scheduler._scheduler._jobs.keys()))

        jobs = scheduler.list_jobs()
        self.assertIsNotNone(jobs)
        self.assertEquals(2, len(jobs))

    def test_add_job_every_n(self):
        scheduler = MockProgramyScheduler(self._test_client, self.create_config(False, None, False))
        self.assertIsNotNone(scheduler)
        self.assertEqual(0, len(scheduler._scheduler._jobs.keys()))

        scheduler.schedule_every_n("testuser", "testclient", "MESSAGE", "REMIND ME", weeks=0, days=0, hours=0, minutes=0, seconds=0)
        self.assertEqual(1, len(scheduler._scheduler._jobs.keys()))

        scheduler.schedule_every_n("testuser", "testclient", "MESSAGE", "REMIND ME", weeks=1, days=0, hours=0, minutes=0, seconds=0)
        self.assertEqual(1, len(scheduler._scheduler._jobs.keys()))

        scheduler.schedule_every_n("testuser", "testclient", "MESSAGE", "REMIND ME", weeks=0, days=1, hours=0, minutes=0, seconds=0)
        self.assertEqual(1, len(scheduler._scheduler._jobs.keys()))

        scheduler.schedule_every_n("testuser", "testclient", "MESSAGE", "REMIND ME", weeks=0, days=0, hours=1, minutes=0, seconds=0)
        self.assertEqual(1, len(scheduler._scheduler._jobs.keys()))

        scheduler.schedule_every_n("testuser", "testclient", "MESSAGE", "REMIND ME", weeks=0, days=0, hours=0, minutes=1, seconds=0)
        self.assertEqual(1, len(scheduler._scheduler._jobs.keys()))

        scheduler.schedule_every_n("testuser", "testclient", "MESSAGE", "REMIND ME", weeks=0, days=0, hours=0, minutes=0, seconds=1)
        self.assertEqual(1, len(scheduler._scheduler._jobs.keys()))

        scheduler.schedule_every_n("testuser", "testclient", "MESSAGE", "REMIND ME", weeks=1, days=1, hours=1, minutes=1, seconds=1)
        self.assertEqual(1, len(scheduler._scheduler._jobs.keys()))

        jobs = scheduler.list_jobs()
        self.assertIsNotNone(jobs)
        self.assertEquals(1, len(jobs))

    def test_add_job_in_seconds(self):
        scheduler = MockProgramyScheduler(self._test_client, self.create_config(False, None, False))
        self.assertIsNotNone(scheduler)
        self.assertEqual(0, len(scheduler._scheduler._jobs.keys()))

        scheduler.schedule_in_n_seconds("testuser", "testclient", "MESSAGE", "REMIND ME", 3)
        self.assertEqual(1, len(scheduler._scheduler._jobs.keys()))

        scheduler.schedule_in_n_seconds("testuser", "testclient", "MESSAGE", "REMIND ME", 3)
        self.assertEqual(1, len(scheduler._scheduler._jobs.keys()))

        scheduler.schedule_in_n_seconds("testuser", "testclient", "MESSAGE", "REMIND ME 2", 3)
        self.assertEqual(2, len(scheduler._scheduler._jobs.keys()))

        jobs = scheduler.list_jobs()
        self.assertIsNotNone(jobs)
        self.assertEquals(2, len(jobs))

    def test_add_job_in_minutes(self):
        scheduler = MockProgramyScheduler(self._test_client, self.create_config(False, None, False))
        self.assertIsNotNone(scheduler)
        self.assertEqual(0, len(scheduler._scheduler._jobs.keys()))

        scheduler.schedule_in_n_minutes("testuser", "testclient", "MESSAGE", "REMIND ME", 3)
        self.assertEqual(1, len(scheduler._scheduler._jobs.keys()))

        scheduler.schedule_in_n_minutes("testuser", "testclient", "MESSAGE", "REMIND ME", 3)
        self.assertEqual(1, len(scheduler._scheduler._jobs.keys()))

        scheduler.schedule_in_n_minutes("testuser", "testclient", "MESSAGE", "REMIND ME 2", 3)
        self.assertEqual(2, len(scheduler._scheduler._jobs.keys()))

        jobs = scheduler.list_jobs()
        self.assertIsNotNone(jobs)
        self.assertEquals(2, len(jobs))

    def test_add_job_in_hours(self):
        scheduler = MockProgramyScheduler(self._test_client, self.create_config(False, None, False))
        self.assertIsNotNone(scheduler)
        self.assertEqual(0, len(scheduler._scheduler._jobs.keys()))

        scheduler.schedule_in_n_hours("testuser", "testclient", "MESSAGE", "REMIND ME", 3)
        self.assertEqual(1, len(scheduler._scheduler._jobs.keys()))

        scheduler.schedule_in_n_hours("testuser", "testclient", "MESSAGE", "REMIND ME", 3)
        self.assertEqual(1, len(scheduler._scheduler._jobs.keys()))

        scheduler.schedule_in_n_hours("testuser", "testclient", "MESSAGE", "REMIND ME 2", 3)
        self.assertEqual(2, len(scheduler._scheduler._jobs.keys()))

        jobs = scheduler.list_jobs()
        self.assertIsNotNone(jobs)
        self.assertEquals(2, len(jobs))

    def test_add_job_in_days(self):
        scheduler = MockProgramyScheduler(self._test_client, self.create_config(False, None, False))
        self.assertIsNotNone(scheduler)
        self.assertEqual(0, len(scheduler._scheduler._jobs.keys()))

        scheduler.schedule_in_n_days("testuser", "testclient", "MESSAGE", "REMIND ME", 3)
        self.assertEqual(1, len(scheduler._scheduler._jobs.keys()))

        scheduler.schedule_in_n_days("testuser", "testclient", "MESSAGE", "REMIND ME", 3)
        self.assertEqual(1, len(scheduler._scheduler._jobs.keys()))

        scheduler.schedule_in_n_days("testuser", "testclient", "MESSAGE", "REMIND ME 2", 3)
        self.assertEqual(2, len(scheduler._scheduler._jobs.keys()))

        jobs = scheduler.list_jobs()
        self.assertIsNotNone(jobs)
        self.assertEquals(2, len(jobs))

    def test_add_job_in_weeks(self):
        scheduler = MockProgramyScheduler(self._test_client, self.create_config(False, None, False))
        self.assertIsNotNone(scheduler)
        self.assertEqual(0, len(scheduler._scheduler._jobs.keys()))

        scheduler.schedule_in_n_weeks("testuser", "testclient", "MESSAGE", "REMIND ME", 3)
        self.assertEqual(1, len(scheduler._scheduler._jobs.keys()))

        scheduler.schedule_in_n_weeks("testuser", "testclient", "MESSAGE", "REMIND ME", 3)
        self.assertEqual(1, len(scheduler._scheduler._jobs.keys()))

        scheduler.schedule_in_n_weeks("testuser", "testclient", "MESSAGE", "REMIND ME 2", 3)
        self.assertEqual(2, len(scheduler._scheduler._jobs.keys()))

        jobs = scheduler.list_jobs()
        self.assertIsNotNone(jobs)
        self.assertEquals(2, len(jobs))

    def test_add_job_as_cron(self):
        scheduler = MockProgramyScheduler(self._test_client, self.create_config(False, None, False))
        self.assertIsNotNone(scheduler)
        self.assertEqual(0, len(scheduler._scheduler._jobs.keys()))

        scheduler.schedule_as_cron("testuser", "testclient", "MESSAGE", "REMIND ME", second='*/3')
        self.assertEqual(1, len(scheduler._scheduler._jobs.keys()))

        scheduler.schedule_as_cron("testuser", "testclient", "MESSAGE", "REMIND ME", second='*/3')
        self.assertEqual(1, len(scheduler._scheduler._jobs.keys()))

        scheduler.schedule_as_cron("testuser", "testclient", "MESSAGE", "REMIND ME 2", second='*/3')
        self.assertEqual(2, len(scheduler._scheduler._jobs.keys()))

        jobs = scheduler.list_jobs()
        self.assertIsNotNone(jobs)
        self.assertEquals(2, len(jobs))

    def test_get_event_str_scheduler_event(self):
        event = SchedulerEvent("code", "alias")
        message = ProgramyScheduler.get_event_str(event)
        self.assertIsNotNone(message)
        self.assertEqual("SchedulerEvent [code] [alias]", message)

    def test_get_event_str_job_event(self):
        event = JobEvent ("code", "id", "jobstore")
        message = ProgramyScheduler.get_event_str(event)
        self.assertIsNotNone(message)
        self.assertEqual("JobEvent [code] [id] [jobstore] [None]", message)

    def test_get_event_str_job_submission_event(self):
        event = JobSubmissionEvent ("code", "job_id", "jobstore", [])
        message = ProgramyScheduler.get_event_str(event)
        self.assertIsNotNone(message)
        self.assertEqual("JobSubmissionEvent [code] [job_id] [jobstore] [[]]", message)

    def test_get_event_str_job_execution_event(self):
        scheduled_run_time = datetime.strptime("10/04/18 19:02", "%d/%m/%y %H:%M")
        event = JobExecutionEvent ("code", "job_id", "jobstore", scheduled_run_time, retval=1)
        message = ProgramyScheduler.get_event_str(event)
        self.assertIsNotNone(message)
        self.assertEqual("JobExecutionEvent [code] [job_id] [jobstore] [2018-04-10 19:02:00] [1]", message)

    def test_get_event_str_job_execution_event_with_exception(self):
        scheduled_run_time = datetime.strptime("10/04/18 19:02", "%d/%m/%y %H:%M")
        event = JobExecutionEvent ("code", "job_id", "jobstore", scheduled_run_time, retval=1, exception=Exception("Test Error"))
        message = ProgramyScheduler.get_event_str(event)
        self.assertIsNotNone(message)
        self.assertEqual("JobExecutionEvent [code] [job_id] [jobstore] [2018-04-10 19:02:00] [1] [Test Error]", message)

    def test_get_event_unknown(self):
        event = unittest.mock.Mock()
        message = ProgramyScheduler.get_event_str(event)
        self.assertIsNone(message)

    def test_scheduled(self):
        scheduler1 = MockProgramyScheduler(self._test_client, self.create_config(False, None, False))
        self.assertIsNotNone(ProgramyScheduler.schedulers)
        self.assertEqual(1, len(ProgramyScheduler.schedulers.keys()))
        self.assertTrue("Scheduler1" in ProgramyScheduler.schedulers)
        self.assertEqual(scheduler1, ProgramyScheduler.schedulers['Scheduler1'])

        self.assertFalse(scheduler1._scheduled)
        scheduled("Scheduler1", "User1", "TestClient", "MESSAGE", "REMIND ME")
        self.assertTrue(scheduler1._scheduled)

    def test_scheduled_unknown_scheduler(self):
        scheduler1 = MockProgramyScheduler(self._test_client, self.create_config(False, None, False))
        self.assertIsNotNone(ProgramyScheduler.schedulers)
        self.assertEqual(1, len(ProgramyScheduler.schedulers.keys()))
        self.assertTrue("Scheduler1" in ProgramyScheduler.schedulers)
        self.assertEqual(scheduler1, ProgramyScheduler.schedulers['Scheduler1'])

        self.assertFalse(scheduler1._scheduled)
        scheduled("Scheduler2", "User1", "TestClient", "MESSAGE", "REMIND ME")
        self.assertFalse(scheduler1._scheduled)

    def test_add_pause_resume_stop(self):
        scheduler1 = MockProgramyScheduler(self._test_client, self.create_config(False, None, False))
        job_id = scheduler1.create_job_id("testuser1", "test1", "RUN", "HELLO")
        scheduler1._scheduler.add_job(scheduled, 'interval', [job_id, "testuser1", "test1", "RUN", "HELLO"],
                                      id=job_id, seconds=100)

        self.assertEquals("started", scheduler1._scheduler._status[job_id])

        scheduler1.pause_job(job_id)

        self.assertEquals("paused", scheduler1._scheduler._status[job_id])

        scheduler1.resume_job(job_id)

        self.assertEquals("started", scheduler1._scheduler._status[job_id])

        scheduler1.stop_job(job_id)

        self.assertFalse(job_id in scheduler1._scheduler._status)

    def test_scheduled_text(self):
        client = MockClient()
        scheduler1 = ProgramyScheduler(client, SchedulerConfiguration())
        scheduler1.scheduled("user1", "client1", "TEXT", "Hello")
        self.assertEquals("Hello", client._response)

    def test_scheduled_srai(self):
        client = MockClient()
        scheduler1 = ProgramyScheduler(client, SchedulerConfiguration())
        scheduler1.scheduled("user1", "client1", "SRAI", "Hello")
        self.assertEquals("Mock Response", client._response)

    def test_scheduled_unknown(self):
        client = MockClient()
        scheduler1 = ProgramyScheduler(client, SchedulerConfiguration())
        scheduler1.scheduled("user1", "client1", "UNKNOWN", "Hello")
        self.assertIsNone(client._response)

    def test_listener_event(self):
        event = JobEvent("code1", "id1", "mock")
        ProgramyScheduler.listener_event(event)

    def test_listener_event_none_event(self):
        ProgramyScheduler.listener_event("Mock Event")