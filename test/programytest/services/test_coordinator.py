import unittest
from unittest.mock import Mock
from programy.services.coordinator import RandomResultServiceCoordinator
from programy.services.coordinator import RoundRobinResultServiceCoordinator
from programy.services.coordinator import AllResultsServiceCoordinator


class ServiceRandomResultCoordinatorTests(unittest.TestCase):

    def test_random_coordinator_no_services(self):
        coordinator = RandomResultServiceCoordinator()
        result = coordinator.execute_query("Question")
        self.assertIsNone(result)

    def test_random_coordinator_1_service(self):

        service1 = Mock()
        service1.execite_query.return_value = {"status": "success", "payload": {"answer": "Service1"}} 

        coordinator = RandomResultServiceCoordinator()
        coordinator.add_service(service1)

        result = coordinator.execute_query("Question")
        self.assertIsNotNone(result)
        self.assertEqual(result, {'status': 'success', 'payload': {'answer': 'Service1'}})

        result = coordinator.execute_query("Question")
        self.assertIsNotNone(result)
        self.assertEqual(result, {'status': 'success', 'payload': {'answer': 'Service1'}})

        result = coordinator.execute_query("Question")
        self.assertIsNotNone(result)
        self.assertEqual(result, {'status': 'success', 'payload': {'answer': 'Service1'}})

    def test_random_coordinator_n_services(self):

        service1 = Mock()
        service1.execite_query.return_value = {"status": "success", "payload": {"answer": "Service1"}} 

        service2 = Mock()
        service2.execite_query.return_value = {"status": "success", "payload": {"answer": "Service2"}} 

        service3 = Mock()
        service3.execite_query.return_value = {"status": "success", "payload": {"answer": "Service3"}} 

        coordinator = RandomResultServiceCoordinator()
        coordinator.add_service(service1)
        coordinator.add_service(service2)
        coordinator.add_service(service3)

        result = coordinator.execute_query("Question")
        self.assertIsNotNone(result)
        self.assertTrue(result in [{'status': 'success', 'payload': {'answer': 'Service1'}},
                                   {'status': 'success', 'payload': {'answer': 'Service2'}},
                                   {'status': 'success', 'payload': {'answer': 'Service3'}}])

        result = coordinator.execute_query("Question")
        self.assertIsNotNone(result)
        self.assertTrue(result in [{'status': 'success', 'payload': {'answer': 'Service1'}},
                                   {'status': 'success', 'payload': {'answer': 'Service2'}},
                                   {'status': 'success', 'payload': {'answer': 'Service3'}}])

        result = coordinator.execute_query("Question")
        self.assertIsNotNone(result)
        self.assertTrue(result in [{'status': 'success', 'payload': {'answer': 'Service1'}},
                                   {'status': 'success', 'payload': {'answer': 'Service2'}},
                                   {'status': 'success', 'payload': {'answer': 'Service3'}}])

    def test_random_coordinator_1_services_skip_failure(self):

        service1 = Mock()
        service1.execite_query.return_value = {"status": "failure", "payload": {"answer": "Service1"}}

        coordinator = RandomResultServiceCoordinator()
        coordinator.add_service(service1)

        result = coordinator.execute_query("Question")
        self.assertIsNone(result)

    def test_random_coordinator_1_services_no_skip_failure(self):

        service1 = Mock()
        service1.execite_query.return_value = {"status": "failure", "payload": {}}

        coordinator = RandomResultServiceCoordinator()
        coordinator.add_service(service1)

        result = coordinator.execute_query("Question", skip_failures=False)
        self.assertIsNotNone(result)
        self.assertEqual(result, {"status": "failure", "payload": {}})

    def test_try_next_on_failure_one_succeed(self):

        service1 = Mock()
        service1.execite_query.return_value = {"status": "failure", "payload": {"answer": "Service1"}}
        service1.name = "Service1"

        service2 = Mock()
        service2.execite_query.return_value = {"status": "failure", "payload": {"answer": "Service2"}}
        service2.name = "Service2"

        service3 = Mock()
        service3.execite_query.return_value = {"status": "success", "payload": {"answer": "Service3"}}
        service3.name = "Service3"

        coordinator = RandomResultServiceCoordinator()
        coordinator.add_service(service1)
        coordinator.add_service(service2)
        coordinator.add_service(service3)

        result = coordinator.execute_query("Question", skip_failures=True, try_next_on_failure=True)
        self.assertIsNotNone(result)
        self.assertEqual(result, {'status': 'success', 'payload': {'answer': 'Service3'}})

    def test_try_next_on_failure_all_fail(self):

        service1 = Mock()
        service1.execite_query.return_value = {"status": "failure", "payload": {"answer": "Service1"}}
        service1.name = "Service1"

        service2 = Mock()
        service2.execite_query.return_value = {"status": "failure", "payload": {"answer": "Service2"}}
        service2.name = "Service2"

        service3 = Mock()
        service3.execite_query.return_value = {"status": "failure", "payload": {"answer": "Service3"}}
        service3.name = "Service3"

        coordinator = RandomResultServiceCoordinator()
        coordinator.add_service(service1)
        coordinator.add_service(service2)
        coordinator.add_service(service3)

        result = coordinator.execute_query("Question", skip_failures=True, try_next_on_failure=True)
        self.assertIsNone(result)


class ServiceRoundRobinResultCoordinatorTests(unittest.TestCase):

    def test_round_robin_coordinator_no_services(self):
        coordinator = RoundRobinResultServiceCoordinator()
        result = coordinator.execute_query("Question")
        self.assertIsNone(result)

    def test_round_robin_coordinator_1_service(self):

        service1 = Mock()
        service1.execite_query.return_value = {"status": "success", "payload": {"answer": "Service1"}} 

        coordinator = RoundRobinResultServiceCoordinator()
        coordinator.add_service(service1)

        result = coordinator.execute_query("Question")
        self.assertIsNotNone(result)
        self.assertEqual(result, {'status': 'success', 'payload': {'answer': 'Service1'}})

        result = coordinator.execute_query("Question")
        self.assertIsNotNone(result)
        self.assertEqual(result, {'status': 'success', 'payload': {'answer': 'Service1'}})

        result = coordinator.execute_query("Question")
        self.assertIsNotNone(result)
        self.assertEqual(result, {'status': 'success', 'payload': {'answer': 'Service1'}})

    def test_round_robin_coordinator_n_services(self):

        service1 = Mock()
        service1.execite_query.return_value = {"status": "success", "payload": {"answer": "Service1"}} 

        service2 = Mock()
        service2.execite_query.return_value = {"status": "success", "payload": {"answer": "Service2"}} 

        service3 = Mock()
        service3.execite_query.return_value = {"status": "success", "payload": {"answer": "Service3"}} 

        coordinator = RoundRobinResultServiceCoordinator()
        coordinator.add_service(service1)
        coordinator.add_service(service2)
        coordinator.add_service(service3)

        result = coordinator.execute_query("Question")
        self.assertIsNotNone(result)
        self.assertEqual(result, {'status': 'success', 'payload': {'answer': 'Service1'}})

        result = coordinator.execute_query("Question")
        self.assertIsNotNone(result)
        self.assertEqual(result, {'status': 'success', 'payload': {'answer': 'Service2'}})

        result = coordinator.execute_query("Question")
        self.assertIsNotNone(result)
        self.assertEqual(result, {'status': 'success', 'payload': {'answer': 'Service3'}})

        result = coordinator.execute_query("Question")
        self.assertIsNotNone(result)
        self.assertEqual(result, {'status': 'success', 'payload': {'answer': 'Service1'}})

    def test_try_next_on_failure_one_succeed(self):

        service1 = Mock()
        service1.execite_query.return_value = {"status": "failure", "payload": {"answer": "Service1"}}
        service1.name = "Service1"

        service2 = Mock()
        service2.execite_query.return_value = {"status": "failure", "payload": {"answer": "Service2"}}
        service2.name = "Service2"

        service3 = Mock()
        service3.execite_query.return_value = {"status": "success", "payload": {"answer": "Service3"}}
        service3.name = "Service3"

        coordinator = RoundRobinResultServiceCoordinator()
        coordinator.add_service(service1)
        coordinator.add_service(service2)
        coordinator.add_service(service3)

        result = coordinator.execute_query("Question", skip_failures=True, try_next_on_failure=True)
        self.assertIsNotNone(result)
        self.assertEqual(result, {'status': 'success', 'payload': {'answer': 'Service3'}})

    def test_try_next_on_failure_all_fail(self):

        service1 = Mock()
        service1.execite_query.return_value = {"status": "failure", "payload": {"answer": "Service1"}}
        service1.name = "Service1"

        service2 = Mock()
        service2.execite_query.return_value = {"status": "failure", "payload": {"answer": "Service2"}}
        service2.name = "Service2"

        service3 = Mock()
        service3.execite_query.return_value = {"status": "failure", "payload": {"answer": "Service3"}}
        service3.name = "Service3"

        coordinator = RoundRobinResultServiceCoordinator()
        coordinator.add_service(service1)
        coordinator.add_service(service2)
        coordinator.add_service(service3)

        result = coordinator.execute_query("Question", skip_failures=True, try_next_on_failure=True)
        self.assertIsNone(result)


class ServiceAllResultsCoordinatorTests(unittest.TestCase):

    def test_all_coordinator_no_services(self):
        coordinator = AllResultsServiceCoordinator()
        result = coordinator.execute_query("Question")
        self.assertIsNone(result)

    def test_all_coordinator_1_service(self):

        service1 = Mock()
        service1.execite_query.return_value = {"status": "success", "payload": {"answer": "Service1"}} 

        coordinator = AllResultsServiceCoordinator()
        coordinator.add_service(service1)

        result = coordinator.execute_query("Question")
        self.assertIsNotNone(result)
        self.assertEqual(result, [{"status": "success", "payload": {"answer": "Service1"}}])

        result = coordinator.execute_query("Question")
        self.assertIsNotNone(result)
        self.assertEqual(result, [{"status": "success", "payload": {"answer": "Service1"}} ])

    def test_all_coordinator_n_services(self):

        service1 = Mock()
        service1.execite_query.return_value = {"status": "success", "payload": {"answer": "Service1"}}

        service2 = Mock()
        service2.execite_query.return_value = {"status": "success", "payload": {"answer": "Service2"}} 

        service3 = Mock()
        service3.execite_query.return_value = {"status": "success", "payload": {"answer": "Service3"}} 

        coordinator = AllResultsServiceCoordinator()
        coordinator.add_service(service1)
        coordinator.add_service(service2)
        coordinator.add_service(service3)

        result = coordinator.execute_query("Question")
        self.assertIsNotNone(result)
        self.assertEqual(result, [{'status': 'success', 'payload': {'answer': 'Service1'}},
                                  {'status': 'success', 'payload': {'answer': 'Service2'}},
                                  {'status': 'success', 'payload': {'answer': 'Service3'}}])

    def test_all_coordinator_1_service_skip_failures(self):

        service1 = Mock()
        service1.execite_query.return_value = {"status": "failure", "payload": {}}

        coordinator = AllResultsServiceCoordinator()
        coordinator.add_service(service1)

        result = coordinator.execute_query("Question", skip_failures=True)
        self.assertIsNotNone(result)
        self.assertEqual(result, [])

    def test_all_coordinator_1_service_no_skip_failures(self):

        service1 = Mock()
        service1.execite_query.return_value = {"status": "failure", "payload": {}}

        coordinator = AllResultsServiceCoordinator()
        coordinator.add_service(service1)

        result = coordinator.execute_query("Question", skip_failures=False)
        self.assertIsNotNone(result)
        self.assertEqual(result, [{"status": "failure", "payload": {}}])

    def test_all_coordinator_n_services_skip_failures(self):

        service1 = Mock()
        service1.execite_query.return_value = {"status": "failure", "payload": {}}

        service2 = Mock()
        service2.execite_query.return_value = {"status": "success", "payload": {"answer": "Service2"}}

        service3 = Mock()
        service3.execite_query.return_value = {"status": "success", "payload": {"answer": "Service3"}}

        coordinator = AllResultsServiceCoordinator()
        coordinator.add_service(service1)
        coordinator.add_service(service2)
        coordinator.add_service(service3)

        result = coordinator.execute_query("Question", skip_failures=True)
        self.assertIsNotNone(result)
        self.assertEqual(result, [{'status': 'success', 'payload': {'answer': 'Service2'}},
                                  {'status': 'success', 'payload': {'answer': 'Service3'}}])

    def test_all_coordinator_n_services_no_skip_failures(self):

        service1 = Mock()
        service1.execite_query.return_value = {"status": "failure", "payload": {}}

        service2 = Mock()
        service2.execite_query.return_value = {"status": "success", "payload": {"answer": "Service2"}}

        service3 = Mock()
        service3.execite_query.return_value = {"status": "success", "payload": {"answer": "Service3"}}

        coordinator = AllResultsServiceCoordinator()
        coordinator.add_service(service1)
        coordinator.add_service(service2)
        coordinator.add_service(service3)

        result = coordinator.execute_query("Question", skip_failures=False)
        self.assertIsNotNone(result)
        self.assertEqual(result, [{"status": "failure", "payload": {}},
                                  {'status': 'success', 'payload': {'answer': 'Service2'}},
                                  {'status': 'success', 'payload': {'answer': 'Service3'}}])
