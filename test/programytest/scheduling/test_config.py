import unittest
from programy.clients.events.console.config import ConsoleConfiguration
from programy.config.file.yaml_file import YamlConfigurationFile
from programy.scheduling.config import SchedulerConfiguration
from programy.scheduling.config import SchedulerJobStoreConfiguration
from programy.scheduling.config import SchedulerThreadPoolConfiguration
from programy.scheduling.config import SchedulerProcessPoolConfiguration
from programy.scheduling.config import SchedulerJobDefaultsConfiguration
from programy.scheduling.config import SchedulerMongoJobStoreConfiguration
from programy.scheduling.config import SchedulerRedisJobStoreConfiguration
from programy.scheduling.config import SchedulerSqlAlchemyJobStoreConfiguration


class SchedulerConfigurationTests(unittest.TestCase):

    def test_with_data(self):
        yaml = YamlConfigurationFile()
        self.assertIsNotNone(yaml)
        yaml.load_from_text("""
        console:
          scheduler:
            name: Scheduler1
            debug_level: 0
            add_listeners: True
            remove_all_jobs: True
            
            jobstore:
                name:   mongo
                
                mongo:
                    collection: example_jobs
    
                redis:
                    jobs_key: example.jobs
                    run_times_key: example.run_times
    
                sqlalchemy:
                    url: sqlite:///jobs.sqlite
    
            threadpool:
                max_workers: 20
        
            processpool:
                max_workers: 5   
        
            job_defaults:
                coalesce: False
                max_instances: 3
          
        """, ConsoleConfiguration(), ".")

        console_config = yaml.get_section("console")

        scheduler_config = SchedulerConfiguration()
        scheduler_config.load_config_section(yaml, console_config, ".")

        self.assertEqual("Scheduler1", scheduler_config.name)
        self.assertEqual(0, scheduler_config.debug_level)
        self.assertTrue(scheduler_config.add_listeners)
        self.assertTrue(scheduler_config.remove_all_jobs)

        self.assertIsNotNone(scheduler_config.jobstore)
        self.assertIsNotNone(scheduler_config.jobstore.storage)
        self.assertEqual("example_jobs", scheduler_config.jobstore.storage.collection)

        self.assertIsNotNone(scheduler_config.threadpool)
        self.assertEqual(20, scheduler_config.threadpool.max_workers)

        self.assertIsNotNone(scheduler_config.processpool)
        self.assertEqual(5, scheduler_config.processpool.max_workers)

        self.assertIsNotNone(scheduler_config.job_defaults)
        self.assertEqual(False, scheduler_config.job_defaults.coalesce)
        self.assertEqual(3, scheduler_config.job_defaults.max_instances)

    def test_without_data(self):
        yaml = YamlConfigurationFile()
        self.assertIsNotNone(yaml)
        yaml.load_from_text("""
        bot:
            scheduler:
        """, ConsoleConfiguration(), ".")

        console_config = yaml.get_section("console")

        scheduler_config = SchedulerConfiguration()
        scheduler_config.load_config_section(yaml, console_config, ".")

        self.assertIsNone(scheduler_config.name)
        self.assertEqual(0, scheduler_config.debug_level)
        self.assertFalse(scheduler_config.add_listeners)
        self.assertFalse(scheduler_config.remove_all_jobs)

        self.assertIsNone(scheduler_config.jobstore)
        self.assertIsNone(scheduler_config.threadpool)
        self.assertIsNone(scheduler_config.processpool)
        self.assertIsNone(scheduler_config.job_defaults)

    def test_with_no_data(self):
        yaml = YamlConfigurationFile()
        self.assertIsNotNone(yaml)
        yaml.load_from_text("""
        bot:
        """, ConsoleConfiguration(), ".")

        console_config = yaml.get_section("console")

        scheduler_config = SchedulerConfiguration()
        scheduler_config.load_config_section(yaml, console_config, ".")

        self.assertIsNone(scheduler_config.name)
        self.assertEqual(0, scheduler_config.debug_level)
        self.assertFalse(scheduler_config.add_listeners)
        self.assertFalse(scheduler_config.remove_all_jobs)

        self.assertIsNone(scheduler_config.jobstore)
        self.assertIsNone(scheduler_config.threadpool)
        self.assertIsNone(scheduler_config.processpool)
        self.assertIsNone(scheduler_config.job_defaults)

    def test_create_scheduler_config_mongo(self):
        yaml = YamlConfigurationFile()
        self.assertIsNotNone(yaml)
        yaml.load_from_text("""
        console:
          scheduler:
            name: Scheduler1
            debug_level: 0
            add_listeners: True
            remove_all_jobs: True

            jobstore:
                name:   mongo

                mongo:
                    collection: example_jobs

            threadpool:
                max_workers: 20

            processpool:
                max_workers: 5   

            job_defaults:
                coalesce: False
                max_instances: 3

        """, ConsoleConfiguration(), ".")

        console_config = yaml.get_section("console")

        scheduler_config = SchedulerConfiguration()
        scheduler_config.load_config_section(yaml, console_config, ".")

        config = scheduler_config.create_scheduler_config()
        self.assertIsNotNone(config)

    def test_create_scheduler_config_redis(self):
        yaml = YamlConfigurationFile()
        self.assertIsNotNone(yaml)
        yaml.load_from_text("""
        console:
          scheduler:
            name: Scheduler1
            debug_level: 0
            add_listeners: True
            remove_all_jobs: True

            jobstore:
                name:   redis

                redis:
                    jobs_key: example.jobs
                    run_times_key: example.run_times

            threadpool:
                max_workers: 20

            processpool:
                max_workers: 5   

            job_defaults:
                coalesce: False
                max_instances: 3

        """, ConsoleConfiguration(), ".")

        console_config = yaml.get_section("console")

        scheduler_config = SchedulerConfiguration()
        scheduler_config.load_config_section(yaml, console_config, ".")

        config = scheduler_config.create_scheduler_config()
        self.assertIsNotNone(config)

    def test_create_scheduler_config_sqlalchemy(self):
        yaml = YamlConfigurationFile()
        self.assertIsNotNone(yaml)
        yaml.load_from_text("""
        console:
          scheduler:
            name: Scheduler1
            debug_level: 0
            add_listeners: True
            remove_all_jobs: True

            jobstore:
                name:   sqlalchemy
                sqlalchemy:
                    url: sqlite:///jobs.sqlite

            threadpool:
                max_workers: 20

            processpool:
                max_workers: 5   

            job_defaults:
                coalesce: False
                max_instances: 3

        """, ConsoleConfiguration(), ".")

        console_config = yaml.get_section("console")

        scheduler_config = SchedulerConfiguration()
        scheduler_config.load_config_section(yaml, console_config, ".")

        config = scheduler_config.create_scheduler_config()
        self.assertIsNotNone(config)

    def test_create_scheduler_config_unknown(self):
        yaml = YamlConfigurationFile()
        self.assertIsNotNone(yaml)
        yaml.load_from_text("""
        console:
          scheduler:
            name: Scheduler1
            debug_level: 0
            add_listeners: True
            remove_all_jobs: True

            jobstore:
                name:   unknown

            threadpool:
                max_workers: 20

            processpool:
                max_workers: 5   

            job_defaults:
                coalesce: False
                max_instances: 3

        """, ConsoleConfiguration(), ".")

        console_config = yaml.get_section("console")

        scheduler_config = SchedulerConfiguration()
        scheduler_config.load_config_section(yaml, console_config, ".")

        config = scheduler_config.create_scheduler_config()
        self.assertIsNotNone(config)

    def test_jobstore_sqlachemy(self):
        yaml = YamlConfigurationFile()
        self.assertIsNotNone(yaml)
        yaml.load_from_text("""
        console:
          scheduler:
            jobstore:
                name:   sqlalchemy
                sqlalchemy:
                    url: sqlite:///jobs.sqlite

        """, ConsoleConfiguration(), ".")

        console_config = yaml.get_section("console")
        self.assertIsNotNone(console_config)

        scheduler_config = yaml.get_section("scheduler", console_config)
        self.assertIsNotNone(scheduler_config)

        jobstore = SchedulerSqlAlchemyJobStoreConfiguration()
        jobstore.load_config_section(yaml, scheduler_config, ".")

    def test_jobstore_mongo(self):
        yaml = YamlConfigurationFile()
        self.assertIsNotNone(yaml)
        yaml.load_from_text("""
        console:
          scheduler:
            jobstore:
                name:   mongo
                mongo:
                    collection: example_jobs

        """, ConsoleConfiguration(), ".")

        console_config = yaml.get_section("console")
        self.assertIsNotNone(console_config)

        scheduler_config = yaml.get_section("scheduler", console_config)
        self.assertIsNotNone(scheduler_config)

        jobstore = SchedulerMongoJobStoreConfiguration()
        jobstore.load_config_section(yaml, scheduler_config, ".")

    def test_jobstore_redis(self):
        yaml = YamlConfigurationFile()
        self.assertIsNotNone(yaml)
        yaml.load_from_text("""
        console:
          scheduler:
            jobstore:
                name:   redis
                redis:
                jobs_key: example.jobs
                run_times_key: example.run_times

        """, ConsoleConfiguration(), ".")

        console_config = yaml.get_section("console")
        self.assertIsNotNone(console_config)

        scheduler_config = yaml.get_section("scheduler", console_config)
        self.assertIsNotNone(scheduler_config)

        jobstore = SchedulerRedisJobStoreConfiguration()
        jobstore.load_config_section(yaml, scheduler_config, ".")

    def test_jobstore_no_jobstore(self):
        yaml = YamlConfigurationFile()
        self.assertIsNotNone(yaml)
        yaml.load_from_text("""
        console:
          scheduler:

        """, ConsoleConfiguration(), ".")

        console_config = yaml.get_section("console")
        self.assertIsNotNone(console_config)

        scheduler_config = yaml.get_section("scheduler", console_config)
        self.assertIsNone(scheduler_config)

    def test_jobstore_unknown(self):
        yaml = YamlConfigurationFile()
        self.assertIsNotNone(yaml)
        yaml.load_from_text("""
        console:
          scheduler:
            jobstore:
                name:   unknown

        """, ConsoleConfiguration(), ".")

        console_config = yaml.get_section("console")
        self.assertIsNotNone(console_config)

        scheduler_config = yaml.get_section("scheduler", console_config)
        self.assertIsNotNone(scheduler_config)

        jobstore = SchedulerRedisJobStoreConfiguration()
        jobstore.load_config_section(yaml, scheduler_config, ".")

    def test_threadpool(self):
        yaml = YamlConfigurationFile()
        self.assertIsNotNone(yaml)
        yaml.load_from_text("""
        console:
          scheduler:
            threadpool:
                max_workers: 20

        """, ConsoleConfiguration(), ".")

        console_config = yaml.get_section("console")
        self.assertIsNotNone(console_config)

        scheduler_config = yaml.get_section("scheduler", console_config)
        self.assertIsNotNone(scheduler_config)

        threadpool = SchedulerThreadPoolConfiguration()
        threadpool.load_config_section(yaml, scheduler_config, ".")

    def test_threadpool_no_threadpool(self):
        yaml = YamlConfigurationFile()
        self.assertIsNotNone(yaml)
        yaml.load_from_text("""
         console:
           scheduler:

         """, ConsoleConfiguration(), ".")

        console_config = yaml.get_section("console")
        self.assertIsNotNone(console_config)

        scheduler_config = yaml.get_section("scheduler", console_config)
        self.assertIsNone(scheduler_config)

    def test_processpool(self):
        yaml = YamlConfigurationFile()
        self.assertIsNotNone(yaml)
        yaml.load_from_text("""
        console:
          scheduler:
            processpool:
                max_workers: 5   

        """, ConsoleConfiguration(), ".")

        console_config = yaml.get_section("console")
        self.assertIsNotNone(console_config)

        scheduler_config = yaml.get_section("scheduler", console_config)
        self.assertIsNotNone(scheduler_config)

        processpool = SchedulerProcessPoolConfiguration()
        processpool.load_config_section(yaml, scheduler_config, ".")

    def test_processpool_no_processpool(self):
        yaml = YamlConfigurationFile()
        self.assertIsNotNone(yaml)
        yaml.load_from_text("""
        console:
          scheduler:

        """, ConsoleConfiguration(), ".")

        console_config = yaml.get_section("console")
        self.assertIsNotNone(console_config)

        scheduler_config = yaml.get_section("scheduler", console_config)
        self.assertIsNone(scheduler_config)

    def test_job_defaults(self):
        yaml = YamlConfigurationFile()
        self.assertIsNotNone(yaml)
        yaml.load_from_text("""
        console:
          scheduler:
            job_defaults:
                coalesce: False
                max_instances: 3

        """, ConsoleConfiguration(), ".")

        console_config = yaml.get_section("console")
        self.assertIsNotNone(console_config)

        scheduler_config = yaml.get_section("scheduler", console_config)
        self.assertIsNotNone(scheduler_config)

        job_defaults = SchedulerJobDefaultsConfiguration()
        job_defaults.load_config_section(yaml, scheduler_config, ".")

    def test_job_defaults_no_defaults(self):
        yaml = YamlConfigurationFile()
        self.assertIsNotNone(yaml)
        yaml.load_from_text("""
        console:
          scheduler:

        """, ConsoleConfiguration(), ".")

        console_config = yaml.get_section("console")
        self.assertIsNotNone(console_config)

        scheduler_config = yaml.get_section("scheduler", console_config)
        self.assertIsNone(scheduler_config)

    def test_create_mongo_jobstore_config(self):
        config = SchedulerConfiguration()
        self.assertIsNotNone(config)

        config._jobstore = SchedulerJobStoreConfiguration()
        config._jobstore._name = "mongo"
        config._jobstore._storage = SchedulerMongoJobStoreConfiguration()
        config._jobstore._storage._collection = "mockcollection"

        data = {}
        config._create_mongo_jobstore_config(data)
        self.assertEquals(data['apscheduler.jobstores.mongo'], {'type': 'mongodb', 'collection': 'mockcollection'})

    def test_create_mongo_jobstore_config_no_jobstore(self):
        config = SchedulerConfiguration()
        self.assertIsNotNone(config)

        data = {}
        config._create_mongo_jobstore_config(data)
        self.assertEquals(data['apscheduler.jobstores.mongo'], {'type': 'mongodb'})

    def test_create_mongo_jobstore_config_no_storage(self):
        config = SchedulerConfiguration()
        self.assertIsNotNone(config)

        config._jobstore = SchedulerJobStoreConfiguration()
        config._jobstore._name = "mongo"

        data = {}
        config._create_mongo_jobstore_config(data)
        self.assertEquals(data['apscheduler.jobstores.mongo'], {'type': 'mongodb'})

    def test_create_mongo_jobstore_config_no_storage_collection(self):
        config = SchedulerConfiguration()
        self.assertIsNotNone(config)

        config._jobstore = SchedulerJobStoreConfiguration()
        config._jobstore._name = "mongo"

        data = {}
        config._create_mongo_jobstore_config(data)
        self.assertEquals(data['apscheduler.jobstores.mongo'], {'type': 'mongodb'})

    def test_create_redis_storage_config(self):
        config = SchedulerConfiguration()
        self.assertIsNotNone(config)

        config._jobstore = SchedulerJobStoreConfiguration()
        config._jobstore._name = "redis"
        config._jobstore._storage = SchedulerRedisJobStoreConfiguration()
        config._jobstore._storage._jobs_key = "job"
        config._jobstore._storage._run_times_key = "runtime"

        data = {}
        config._create_redis_jobstore_config(data)
        self.assertEquals(data['apscheduler.jobstores.redis'], {'jobs_key': 'job', 'run_times_key': 'runtime', 'type': 'redis'})

    def test_create_redis_jobstore_config_no_jobstore(self):
        config = SchedulerConfiguration()
        self.assertIsNotNone(config)

        data = {}
        config._create_redis_jobstore_config(data)
        self.assertEquals(data['apscheduler.jobstores.redis'], {'type': 'redis'})

    def test_create_redis_jobstore_config_no_storage(self):
        config = SchedulerConfiguration()
        self.assertIsNotNone(config)

        config._jobstore = SchedulerJobStoreConfiguration()
        config._jobstore._name = "redis"

        data = {}
        config._create_redis_jobstore_config(data)
        self.assertEquals(data['apscheduler.jobstores.redis'], {'type': 'redis'})

    def test_create_redis_jobstore_config_no_keys(self):
        config = SchedulerConfiguration()
        self.assertIsNotNone(config)

        config._jobstore = SchedulerJobStoreConfiguration()
        config._jobstore._name = "redis"
        config._jobstore._storage = SchedulerRedisJobStoreConfiguration()

        data = {}
        config._create_redis_jobstore_config(data)
        self.assertEquals(data['apscheduler.jobstores.redis'], {'type': 'redis'})

    def test_create_sqlalchemy_storage_config(self):
        config = SchedulerConfiguration()
        self.assertIsNotNone(config)

        config._jobstore = SchedulerJobStoreConfiguration()
        config._jobstore._name = "sqlalchemy"
        config._jobstore._storage = SchedulerSqlAlchemyJobStoreConfiguration()
        config._jobstore._storage._url = "sqlite://programy"

        data = {}
        config._create_sqlalchemy_jobstore_config(data)
        self.assertEquals(data['apscheduler.jobstores.sqlalchemy'], {'type': 'sqlalchemy', 'url': 'sqlite://programy'})

    def test_create_sqlalchemy_jobstore_config_no_jobstore(self):
        config = SchedulerConfiguration()
        self.assertIsNotNone(config)

        data = {}
        config._create_sqlalchemy_jobstore_config(data)
        self.assertEquals(data['apscheduler.jobstores.sqlalchemy'], {'type': 'sqlalchemy'})

    def test_create_sqlalchemy_jobstore_config_no_storage(self):
        config = SchedulerConfiguration()
        self.assertIsNotNone(config)

        config._jobstore = SchedulerJobStoreConfiguration()
        config._jobstore._name = "sqlalchemy"

        data = {}
        config._create_sqlalchemy_jobstore_config(data)
        self.assertEquals(data['apscheduler.jobstores.sqlalchemy'], {'type': 'sqlalchemy'})

    def test_create_sqlalchemy_jobstore_storage_no_url(self):
        config = SchedulerConfiguration()
        self.assertIsNotNone(config)

        config._jobstore = SchedulerJobStoreConfiguration()
        config._jobstore._name = "sqlalchemy"
        config._jobstore._storage = SchedulerSqlAlchemyJobStoreConfiguration()

        data = {}
        config._create_sqlalchemy_jobstore_config(data)
        self.assertEquals(data['apscheduler.jobstores.sqlalchemy'], {'type': 'sqlalchemy'})

    def test_create_threadpool_config(self):
        config = SchedulerConfiguration()
        self.assertIsNotNone(config)

        config._threadpool = SchedulerThreadPoolConfiguration()
        config._threadpool._max_workers = 3

        data = {}
        config._create_threadpool_config(data)
        self.assertEquals(data['apscheduler.executors.default'], {'class': 'apscheduler.executors.pool:ThreadPoolExecutor', 'max_workers': '3'})

    def test_create_threadpool_config_no_config(self):
        config = SchedulerConfiguration()
        self.assertIsNotNone(config)

        data = {}
        config._create_threadpool_config(data)
        self.assertEquals(data['apscheduler.executors.default'], {'class': 'apscheduler.executors.pool:ThreadPoolExecutor'})

    def test_create_threadpool_config_no_maxworkers(self):
        config = SchedulerConfiguration()
        self.assertIsNotNone(config)

        config._threadpool = SchedulerThreadPoolConfiguration()

        data = {}
        config._create_threadpool_config(data)
        self.assertEquals(data['apscheduler.executors.default'], {'class': 'apscheduler.executors.pool:ThreadPoolExecutor'})

    def test_create_processpool_config(self):
        config = SchedulerConfiguration()
        self.assertIsNotNone(config)

        config._processpool = SchedulerProcessPoolConfiguration()
        config._processpool._max_workers = 3

        data = {}
        config._create_processpool_config(data)
        self.assertEquals(data['apscheduler.executors.processpool'],  {'max_workers': '3', 'type': 'processpool'})

    def test_create_processpool_config_no_config(self):
        config = SchedulerConfiguration()
        self.assertIsNotNone(config)

        data = {}
        config._create_processpool_config(data)
        self.assertEquals(data['apscheduler.executors.processpool'],  {'type': 'processpool'})

    def test_create_processpool_config_no_max_workers(self):
        config = SchedulerConfiguration()
        self.assertIsNotNone(config)

        config._processpool = SchedulerProcessPoolConfiguration()

        data = {}
        config._create_processpool_config(data)
        self.assertEquals(data['apscheduler.executors.processpool'],  {'type': 'processpool'})

    def test_create_job_defaults_config(self):
        config = SchedulerConfiguration()
        self.assertIsNotNone(config)

        config._job_defaults = SchedulerJobDefaultsConfiguration()
        config._job_defaults._coalesce = 1
        config._job_defaults._max_instances = 3

        data = {}
        config._create_job_defaults_config(data)
        self.assertEquals(data['apscheduler.job_defaults'],  {'coalesce': '1', 'max_instances': '3'})

    def test_create_job_defaults_config_no_config(self):
        config = SchedulerConfiguration()
        self.assertIsNotNone(config)

        data = {}
        config._create_job_defaults_config(data)
        self.assertEquals(data['apscheduler.job_defaults'],  {})

    def test_create_job_defaults_config_no_values(self):
        config = SchedulerConfiguration()
        self.assertIsNotNone(config)

        config._job_defaults = SchedulerJobDefaultsConfiguration()

        data = {}
        config._create_job_defaults_config(data)
        self.assertEquals(data['apscheduler.job_defaults'],  {})

    def test_defaults(self):
        config = SchedulerConfiguration()
        data = {}
        config.to_yaml(data, True)

        SchedulerConfigurationTests.assert_defaults(self, data)

    @staticmethod
    def assert_defaults(test, data):
        test.assertEqual(data['name'], "scheduler")
        test.assertEqual(data['debug_level'], 0)
        test.assertFalse(data['add_listeners'])
        test.assertFalse(data['remove_all_jobs'])

        test.assertTrue('jobstore' in data)
        SchedulerConfigurationTests.assert_jobstore_defaults(test, data['jobstore'])

        test.assertTrue('threadpool' in data)
        SchedulerConfigurationTests.assert_threadpool_defaults(test, data['threadpool'])

        test.assertTrue('processpool' in data)
        SchedulerConfigurationTests.assert_processpool_defaults(test, data['processpool'])

        test.assertTrue('job_defaults' in data)
        SchedulerConfigurationTests.assert_job_defaults_defaults(test, data['job_defaults'])

    def assert_jobstore_defaults(test, data):
        test.assertEqual(data['name'], "mongo")
        test.assertTrue('mongo' in data)
        test.assertEqual(data['mongo']['collection'], "programy")

    def assert_threadpool_defaults(test, data):
        test.assertEqual(data['max_workers'], 20)

    def assert_processpool_defaults(test, data):
        test.assertEqual(data['max_workers'], 5)

    def assert_job_defaults_defaults(test, data):
        test.assertFalse(data['coalesce'])
        test.assertEqual(data['max_instances'], 3)

