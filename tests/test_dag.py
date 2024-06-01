import requests
import unittest


class TestHelloWorldDAG(unittest.TestCase):

    def test_dag_status(self):
        auth = ("airflow", "airflow")
        response = requests.get(
            "http://localhost:8080/api/v1/dags/Hello-world", auth=auth
        )
        self.assertEqual(response.status_code, 200)
        dag_info = response.json()
        self.assertEqual(dag_info["dag_id"], "Hello-world")
        self.assertEqual(dag_info["is_paused"], True)
        self.assertEqual(dag_info["is_active"], True)

    def test_task_status(self):
        auth = ("airflow", "airflow")
        response = requests.get(
            "http://localhost:8080/api/v1/dags/Hello-world/dagRuns", auth=auth
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.status_code, 200)
        dag_runs = response.json()["dag_runs"]
        self.assertTrue(len(dag_runs) > 0)
        dag_run_id = dag_runs[0]["dag_run_id"]

        response = requests.get(
            f"http://localhost:8080/api/v1/dags/Hello-world/dagRuns/{dag_run_id}/taskInstances",
            auth=auth,
        )
        self.assertEqual(response.status_code, 200)
        task_instances = response.json()["task_instances"]
        self.assertTrue(len(task_instances) > 0)
        for task_instance in task_instances:
            self.assertEqual(task_instance["state"], "success")


if __name__ == "__main__":
    unittest.main()
