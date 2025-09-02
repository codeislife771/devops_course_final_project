# test_tasks.py
import unittest
import json
import uuid

# Adjust to your actual module name if needed
from app import app, load_tasks, save_tasks


class TestTasksAPI(unittest.TestCase):
    """Unit tests for the Tasks Flask API"""

    def setUp(self):
        """Set up test fixtures before each test method"""
        self.client = app.test_client()
        app.testing = True

        # Clear persistent storage before each test
        save_tasks({})

        # Sample task payload
        self.sample_task = {
            "name": "unit-test-task",
            "author": "unittest"
        }

    def test_post_creates_task_with_uuid_and_persists(self):
        """Test POST /tasks creates a new task, returns uuid, and persists it"""
        # Send POST request
        resp = self.client.post(
            "/tasks",
            data=json.dumps(self.sample_task),
            content_type="application/json",
        )

        # Expect 201 Created (adjust if your API returns 200)
        self.assertEqual(resp.status_code, 201, msg=resp.data)

        # Parse JSON body (expects an object with a 'uuid' field)
        body = json.loads(resp.data)
        self.assertIn("uuid", body, msg=f"Response body: {body}")
        returned_uuid = body["uuid"]

        # Validate UUID format
        uuid_obj = uuid.UUID(returned_uuid)  # raises ValueError if invalid
        self.assertIsInstance(uuid_obj, uuid.UUID)

        # Ensure it was stored in persistent storage (map keyed by uuid)
        all_tasks = load_tasks()
        self.assertIn(returned_uuid, all_tasks, msg=f"Storage: {all_tasks}")

        stored = all_tasks[returned_uuid]
        # Stored fields match what we sent
        self.assertEqual(stored.get("name"), self.sample_task["name"])
        self.assertEqual(stored.get("author"), self.sample_task["author"])
        # If you also store 'uuid' inside the task object, verify consistency:
        if "uuid" in stored:
            self.assertEqual(stored["uuid"], returned_uuid)

    def test_get_tasks_returns_stored_tasks(self):
        """Test GET /tasks returns all stored tasks (map keyed by uuid)"""
        # Create two tasks via POST
        t1 = {"name": "mouse", "author": "ci"}
        t2 = {"name": "keyboard", "author": "ci"}

        r1 = self.client.post("/tasks", data=json.dumps(t1), content_type="application/json")
        r2 = self.client.post("/tasks", data=json.dumps(t2), content_type="application/json")

        self.assertEqual(r1.status_code, 201, msg=r1.data)
        self.assertEqual(r2.status_code, 201, msg=r2.data)

        id1 = r1.get_json()["uuid"]
        id2 = r2.get_json()["uuid"]

        # Now GET /tasks
        resp = self.client.get("/api/tasks")
        self.assertEqual(resp.status_code, 200, msg=resp.data)

        tasks_map = resp.get_json()   # Flask parses JSON safely
        self.assertIsInstance(tasks_map, dict, msg=f"Response type: {type(tasks_map)}")

        # Both tasks should be present
        self.assertIn(id1, tasks_map)
        self.assertIn(id2, tasks_map)

        # And have correct data
        self.assertEqual(tasks_map[id1].get("name"), "mouse")
        self.assertEqual(tasks_map[id1].get("author"), "ci")
        self.assertEqual(tasks_map[id2].get("name"), "keyboard")
        self.assertEqual(tasks_map[id2].get("author"), "ci")

    def tearDown(self):
        """Clean up after each test"""
        save_tasks({})


if __name__ == "__main__":
    # Run the tests
    unittest.main(verbosity=2)
