import unittest
from unittest.mock import patch

from operationalize.main import app


class TestRateTaskEndpoint(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    @patch("operationalize.main.projects")
    def test_successful_rating_submission(self, mock_projects):
        mock_projects[0].get_task_by_id.return_value = MockTask()
        response = self.app.post("/rate_task/1", json={"rating": 5})
        self.assertEqual(response.status_code, 200)
        self.assertIn("Rating submitted successfully", response.data.decode())

    @patch("operationalize.main.projects")
    def test_error_handling_invalid_task_id(self, mock_projects):
        mock_projects[0].get_task_by_id.return_value = None
        response = self.app.post("/rate_task/999", json={"rating": 5})
        self.assertEqual(response.status_code, 404)
        self.assertIn("Task not found or not rateable", response.data.decode())

    @patch("operationalize.main.projects")
    def test_non_rateable_tasks_cannot_be_rated(self, mock_projects):
        mock_projects[0].get_task_by_id.return_value = MockNonRateableTask()
        response = self.app.post("/rate_task/2", json={"rating": 5})
        self.assertEqual(response.status_code, 404)
        self.assertIn("Task not found or not rateable", response.data.decode())


class MockTask:
    def __init__(self):
        self.ratings = []

    def submit_rating(self, rating):
        self.ratings.append(rating)


class MockNonRateableTask:
    pass
