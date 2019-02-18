import unittest
import unittest.mock
from datetime import datetime

from programy.extensions.admin.scheduler import SchedulerAdminExtension

from programytest.client import TestClient

class MockScheduler(object):

    def __init__(self):
        self._paused = False
        self._removed = None
        self._jobs = {}

    def list_jobs(self):
        return self._jobs

    def remove_existing_job(self, id):
        self._removed = id

    def pause (self):
        self._paused = True

    def resume (self):
        self._paused = False


class SchedulerAdminExtensionClient(TestClient):

    def __init__(self):
        TestClient.__init__(self)

    def load_configuration(self, arguments):
        super(SchedulerAdminExtensionClient, self).load_configuration(arguments)

    def load_scheduler(self):
        self._scheduler = MockScheduler()


class SchedulerAdminExtensionTests(unittest.TestCase):

    def test_scheduler_commands(self):
        client = SchedulerAdminExtensionClient()
        client_context = client.create_client_context("testid")

        extension = SchedulerAdminExtension()
        self.assertEqual("LIST JOBS, KILL JOB, PAUSE, RESUME", extension.execute(client_context, "COMMANDS"))

    def test_scheduler_list_jobs(self):
        client = SchedulerAdminExtensionClient()
        client_context = client.create_client_context("testid")

        extension = SchedulerAdminExtension()

        self.assertEqual("No job information available", extension.execute(client_context, "LIST JOBS"))

        job1 = unittest.mock.Mock()
        job1.next_run_time = datetime.strptime("11/04/18 19:02", "%d/%m/%y %H:%M")
        job1.args = ("Arg1", "Arg2", "Arg3", "Arg4", "Arg5")
        client.scheduler._jobs["1"] = job1

        self.assertEqual("> Job ID:1, Next Run: 2018-04-11 19:02:00, Args: ('Arg1', 'Arg2', 'Arg3', 'Arg4', 'Arg5')\n", extension.execute(client_context, "LIST JOBS"))

    def test_scheduler_kill_job(self):
        client = SchedulerAdminExtensionClient()
        client_context = client.create_client_context("testid")

        extension = SchedulerAdminExtension()

        job1 = unittest.mock.Mock()
        job1.next_run_time = datetime.strptime("11/04/18 19:02", "%d/%m/%y %H:%M")
        job1.args = ("Arg1", "Arg2", "Arg3", "Arg4", "Arg5")
        client.scheduler._jobs["1"] = job1

        self.assertEqual("Job removed", extension.execute(client_context, "KILL JOB 1"))

    def test_scheduler_pause_resume(self):
        client = SchedulerAdminExtensionClient()
        client_context = client.create_client_context("testid")

        extension = SchedulerAdminExtension()

        self.assertEqual("Scheduler paused", extension.execute(client_context, "PAUSE"))
        self.assertTrue(client.scheduler._paused)

        self.assertEqual("Scheduler resumed", extension.execute(client_context, "RESUME"))
        self.assertFalse(client.scheduler._paused)
